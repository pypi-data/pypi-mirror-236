import numpy as np
import os,sys
import math
from sklearn.cluster import KMeans
import uproot
import warnings


#--------------------------------------------------------------------------------------------------------------------------------------------

def getData(fname="", procName="Events"):
    file = uproot.open(fname)
    dq_dict = file[procName].arrays(library="np")
    dq_events = {
        "Hits":{
            "detID": dq_dict["hit_detID"],
            "edep": dq_dict["hit_edep"],
            "elmID": dq_dict["hit_elmID"],
            "hit_pos": dq_dict["hit_pos"]
        },
        "track":{
            "x": dq_dict["track_x_st3"],
            "y": dq_dict["track_y_st3"],
            "Cal_x": dq_dict["track_x_CAL"],
            "Cal_y": dq_dict["track_y_CAL"],
            "ID": dq_dict["eventID"],
            "pz": dq_dict["track_pz_st1"]
        },
        "st23": {
            "ntrack23": dq_dict["n_st23tracklets"],
            "px":   dq_dict["st23tracklet_px_st3"],
            "py":   dq_dict["st23tracklet_py_st3"],
            "pz":   dq_dict["st23tracklet_pz_st3"],
            "x":   dq_dict["st23tracklet_x_st3"],
            "y":   dq_dict["st23tracklet_y_st3"],
            "z":   dq_dict["st23tracklet_z_st3"],
            "Cal_x": dq_dict["st23tracklet_x_CAL"],
            "Cal_y": dq_dict["st23tracklet_y_CAL"]
        },
        "gen":{
            "pz": dq_dict["gpz"]
        },
    }

    return dq_events
#--------------------------------------------------------------------------------------------------------------------------------------------

ntowersx=72
ntowersy=36
sizex=5.53 # in cm
sizey=5.53 # in cm
ecalx=[-200,200] #size in cm
ecaly=[-100,100]
binsx=ecalx[1]- ecalx[0]
binsy=ecaly[1]- ecaly[0]
sfc = 0.1146337964120158 #sampling fraction of emcal
emin=0.0005

#--------------------------------------------------------------------------------------------------------------------------------------------

def emcal_bytuple(dq_events):
    dq_hits = dq_events["Hits"]
    x_pos = []
    y_pos = []
    eve_energy = []
    for i in range(len(dq_events["Hits"]["edep"])):
        output = emcal_byevent(dq_hits, i)
        if len(output[0]) != 0:
            x_pos.append(output[0])
            y_pos.append(output[1])
            eve_energy.append(output[2])
        else:
            x_pos.append(np.array([]))
            y_pos.append(np.array([]))
            eve_energy.append(np.array([]))
            
    return x_pos, y_pos, eve_energy

#--------------------------------------------------------------------------------------------------------------------------------------------

def emcal_byevent(dq_hits, evtNum):
    raw_elmID = dq_hits["elmID"][evtNum]
    raw_edep = dq_hits["edep"][evtNum]
    
    emcal_mask = dq_hits["detID"][evtNum] == 100
    eng_mask = raw_edep[emcal_mask] >= emin
    
    elmID = raw_elmID[emcal_mask][eng_mask]#could also use dstack here to zip (elmID and edep)
    edep = raw_edep[emcal_mask][eng_mask]
    
    emcal_towerx = elmID // ntowersy
    emcal_towery = elmID % ntowersy
    emcal_x = ecalx[0] + emcal_towerx * sizex
    emcal_y = ecaly[0] + emcal_towery * sizey
    emcal_edep = edep / sfc
    
    return emcal_x, emcal_y, emcal_edep

#--------------------------------------------------------------------------------------------------------------------------------------------

def find_energy_seeds(x, y, energy, min_energy=0.2, seed_radius=30):
    high_energy_mask =energy >min_energy
    high_energy_points = np.column_stack((x[high_energy_mask], y[high_energy_mask], energy[high_energy_mask]))
    seeds = []
    indices = []
    for i, (x_val, y_val, energy_val) in enumerate(high_energy_points):
        distances = np.array(np.sqrt((high_energy_points[:, 0] - x_val)**2 + (high_energy_points[:, 1] - y_val)**2))
        distances[i] = seed_radius + 1
        points_within_radius_mask = distances < seed_radius
        points_within_radius = high_energy_points[points_within_radius_mask]
        if len(points_within_radius) == 0 or energy_val > np.max(points_within_radius[:, 2], initial=0):
            seeds.append([x_val, y_val])
            indices.append(np.where(high_energy_mask)[0][i])
            
    return np.array(seeds), indices
    
#--------------------------------------------------------------------------------------------------------------------------------------------
def multi_clusters(dq_events):
    (x, y, eng)=emcal_bytuple(dq_events)
    labels=[]
    seeds=[]
    labels_decrease=[]
    seed_labels = []
    for i in range(len(eng)):#evt level
        (seed, index)=find_energy_seeds(x[i], y[i], eng[i])
        points=np.column_stack((x[i],y[i]))
        try:
            warnings.simplefilter("ignore")
            kmeans = KMeans(n_clusters=len(seed), init=seed , random_state=0, max_iter=1).fit(points)#since center given to grow, n_init==1
            evt_seed_labels = kmeans.labels_[index]

            if len(np.unique(evt_seed_labels))!= len(seed):#if rare case, iteration change center
                dup, mis = find_duplicate_missing(evt_seed_labels)
                dp_indices = np.where(evt_seed_labels == dup)[0]
                distances = np.linalg.norm(seed[dp_indices], axis=1)
                further_index = dp_indices[np.argmax(distances)]
                seed[further_index] = kmeans.cluster_centers_[mis]
                evt_seed_labels[further_index] = mis


            labels.append(kmeans.labels_)
            label_decr = label_clus_eng(kmeans.labels_, eng[i])
            labels_decrease.append(label_decr)
            seed_labels.append(evt_seed_labels)
            seeds.append(seed)#since new seed may be added by clustering

        except:
            labels.append([])
            labels_decrease.append([])
            seed_labels.append([])
            seeds.append([])

       

    return x, y, eng, labels, labels_decrease, seeds, seed_labels
#--------------------------------------------------------------------------------------------------------------------------------------------

def label_clus_eng(label, eng_eve):#return sorted labels by decreasing order of energy
    unique_labels = np.unique(label)
    cluster_energy = np.zeros(len(unique_labels), dtype=np.int64)
    for i in range(len(label)):
        cluster_energy[label[i]] += eng_eve[i]
    sorted_labels = unique_labels[np.argsort(cluster_energy)[::-1]]
    return sorted_labels

#--------------------------------------------------------------------------------------------------------------------------------------------

def h4_bytuple(dq_events):
    dq_hits = dq_events["Hits"]
    hits = np.squeeze(np.dstack((dq_hits["detID"], dq_hits["hit_pos"])), axis=0)

    h4x = []
    h4y = []

    for index, item in enumerate(hits):
        h4y_mask = (41 <= item[0]) & (item[0] <= 44)
        h4x_mask = (45 <= item[0]) & (item[0] <= 46)
        ID_pos = np.squeeze(np.dstack((hits[index][0],hits[index][1])), axis=0)
        h4x.append(ID_pos[h4x_mask])
        h4y.append(ID_pos[h4y_mask])
    return h4x, h4y

#--------------------------------------------------------------------------------------------------------------------------------------------
def gen_wew(x_eve, y_eve, eng_eve):
    eng_tot = np.sum(eng_eve)
    x_bar = np.dot(x_eve, eng_eve) / eng_tot
    y_bar = np.dot(y_eve, eng_eve) / eng_tot

    x_sq_eve = eng_eve * (x_eve - x_bar) ** 2
    y_sq_eve = eng_eve * (y_eve - y_bar) ** 2

    try:
        wew_x = np.sqrt(np.sum(x_sq_eve) / eng_tot)
    except ZeroDivisionError:
        wew_x = -1

    try:
        wew_y = np.sqrt(np.sum(y_sq_eve) / eng_tot)
    except ZeroDivisionError:
        wew_y = -1

    return [wew_x, wew_y]
#--------------------------------------------------------------------------------------------------------------------------------------------
def gen_wid(x_eve, y_eve):
    x_bar = np.mean(x_eve)
    y_bar = np.mean(y_eve)

    x_sq_eve = (x_eve - x_bar) ** 2
    y_sq_eve = (y_eve - y_bar) ** 2

    try:
        wid_x = np.sqrt(np.mean(x_sq_eve))
    except ZeroDivisionError:
        wid_x = -1

    try:
        wid_y = np.sqrt(np.mean(y_sq_eve))
    except ZeroDivisionError:
        wid_y = -1

    return [wid_x, wid_y]
#--------------------------------------------------------------------------------------------------------------------------------------------

def extp_trkl(trkl_coord):
    x_z = np.array([2251.71, 2234.29])
    y_z = np.array([2130.27, 2146.45, 2200.44, 2216.62])
    # Calculate the common term for h4x and h4y
    common_term = (trkl_coord[4] / trkl_coord[5])[:, np.newaxis]

    h4x = trkl_coord[0][:, np.newaxis] + common_term * (x_z - trkl_coord[2][:, np.newaxis])
    h4y = trkl_coord[1][:, np.newaxis] + common_term * (y_z - trkl_coord[2][:, np.newaxis])
    
    return h4x, h4y

#--------------------------------------------------------------------------------------------------------------------------------------------

def h4_matchup(ref, h4_expr):
    results = []
    reference = ref[0]
    for b_val in h4_expr:
        if len(b_val) > 0:
            index = np.abs(b_val[:, 1] - reference).argmin()
            results.append(b_val[index][1])
            reference = b_val[index][1]
        else:
            results.append(-9999)
    return results

#--------------------------------------------------------------------------------------------------------------------------------------------
def find_duplicate_missing(seeds_label):
    n = len(seeds_label)
    expected_sum = n * (n - 1) // 2
    expected_sum_sq = (n * (n - 1) * (2*n - 1)) // 6
    actual_sum = sum(seeds_label)
    actual_sum_sq = sum(x*x for x in seeds_label)
    diff_sum = expected_sum - actual_sum
    diff_sum_sq = expected_sum_sq - actual_sum_sq
    mis = (diff_sum + (diff_sum_sq // diff_sum)) // 2
    dup = mis - diff_sum
    return dup, mis
#--------------------------------------------------------------------------------------------------------------------------------------------
def flatten(item):
    # Base case: if the item is a simple numeric type
    if isinstance(item, (int, float, np.number)):
        yield item
        return

    # If it's a list or a numpy array
    if isinstance(item, (list, np.ndarray)):
        for subitem in item:
            yield from flatten(subitem)
        return

    raise ValueError(f"Unsupported data type: {type(item)}")
#--------------------------------------------------------------------------------------------------------------------------------------------
def unfold_output(folded_result):
    flat_list = []
    stack = [folded_result]

    while stack:
        current = stack.pop()
        if isinstance(current, (list, tuple)):
            stack.extend(reversed(current))
        elif isinstance(current, np.ndarray):
            stack.extend(current[::-1])
        else:
            flat_list.append(current)

   
    return flat_list
#--------------------------------------------------------------------------------------------------------------------------------------------
def compute_energy_ratio(trkl, track, energy, max_distance=3):

    # Check if track is empty.
    if track.size == 0:
        return -9999
    
    # Ensure trkl and energy are 1D arrays and track is a 2D array.
    trkl = np.squeeze(np.asarray(trkl, dtype=np.float32))
    track = np.asarray(track, dtype=np.float32)
    energy = np.squeeze(np.asarray(energy, dtype=np.float32))

    # Get the reference point from trkl.
    ref_point = trkl[:2]
    
    # Calculate squared distances directly without sqrt for comparison to avoid sqrt computations.
    squared_distances = np.sum((track[:, :2] - ref_point)**2, axis=1)
    
    # Find the index of the closest point and the respective squared distance.
    closest_idx = np.argmin(squared_distances)
    closest_squared_distance = squared_distances[closest_idx]
    
    # Compare with squared max_distance to avoid sqrt computation in common cases.
    if closest_squared_distance < max_distance**2:
        # Get the momentum from the closest point in track.
        momentum_closest_point = track[closest_idx, 2]
        # Return the total energy divided by the momentum of the closest point.
        return np.sum(energy) / momentum_closest_point
    else:
        # Return the dummy variable.
        return -9999

#--------------------------------------------------------------------------------------------------------------------------------------------

def prepare_data_bytuple(filename):
    dq_events = getData(filename, "Events")

    (x, y, eng, labels, labels_decrease, seeds, seed_labels) = multi_clusters(dq_events)#here performed clustering
    (h4x, h4y) = h4_bytuple(dq_events)

    dq_st23 = dq_events["st23"]
    dq_track = dq_events["track"]
    gpz = dq_events["gen"]["pz"]
    trkls_coord = np.stack((dq_st23["x"], dq_st23["y"], dq_st23["z"], dq_st23["px"], dq_st23["py"], dq_st23["pz"]), axis=1)
    trkls_cal = np.stack((dq_st23["Cal_x"], dq_st23["Cal_y"]), axis=1)
    track_st3 = np.stack((dq_track["x"], dq_track["y"], dq_track["pz"]), axis=1)
    whole_tuple_result = []
    for i in range(len(eng)):
        evt_result=[]
        if len(seeds[i])==0:
            whole_tuple_result.append([np.full(20, -9999)])
            continue

        trkl_coord = np.array(trkls_coord[i].tolist()).T
        trkl_cal = np.array(trkls_cal[i].tolist()).T
        evt_h4x = np.unique(h4x[i], axis=0)
        evt_h4y = np.unique(h4y[i], axis=0)

        if len(h4x) or len(h4y):#prepare evt_h4
            ext_h4x, ext_h4y = extp_trkl(trkls_coord[i])
            evt_h4 = []
            for val in range(41, 47):#get the experiment value of h4
                if val <= 44:
                    evt_h4.append(evt_h4y[evt_h4y[:, 0] == float(val)])
                else:
                    evt_h4.append(evt_h4x[evt_h4x[:, 0] == float(val)])

        for label in labels_decrease[i]:
            hits_mask = (labels[i] == label)
            cluster_info = [
                gpz[i][0],
                gen_wid(x[i][hits_mask], y[i][hits_mask]),
                gen_wew(x[i][hits_mask], y[i][hits_mask], eng[i][hits_mask]),
                seeds[i][seed_labels[i] == label]
            ]
            if len(trkl_cal)==0:
                cluster_info.append(np.full(13, -9999))
                evt_result.append(unfold_output(cluster_info))
                continue
            #then if do have trkl, we matchup with cluster and track, to get E/p

            distances = np.linalg.norm(trkl_cal - cluster_info[2], axis=1)
            idx = distances.argmin()

            if distances[idx] <= 8:
                cluster_info.extend([trkl_coord[idx],#append st3 trkl xyzpxpypz, h4 info
                                     compute_energy_ratio(trkl_coord[idx], np.array(track_st3[i].tolist()).T, eng[i][hits_mask]),
                                     h4_matchup(ext_h4y[idx], evt_h4[:4]),
                                     h4_matchup(ext_h4x[idx], evt_h4[4:])])

                trkl_coord = np.delete(trkl_coord, idx, axis=0)
                trkl_cal = np.delete(trkl_cal, idx, axis=0)
            else:
                cluster_info.append(np.full(13, -9999))
            evt_result.append(unfold_output(cluster_info))
        whole_tuple_result.append(evt_result)
    return whole_tuple_result

#--------------------------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------------------------------------





