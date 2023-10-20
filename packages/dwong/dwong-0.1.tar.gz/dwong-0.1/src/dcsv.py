
import dwong
import csv
def gen_csv(filename):
    folded_list=dwong.prepare_data_bytuple(filename)
    
    flat_list = [particle for event in folded_list for particle in event]
    labels = [0] * len(flat_list)
    labeled_flat_list = [[label, *particle] for label, particle in zip(labels, flat_list)]

    file_name = filename.split("/")[-1]

    particle_name = file_name.split("_")[0]
    file_path = 'p5_80_%s_0_10000.csv'%particle_name

    # Headers
    headers = ["Label", "gpz", "wid_x", "wid_y", "wew_x", "wew_y", "seed_x", "seed_y",
               "trkl_x", "trkl_y", "trkl_z", "trkl_px", "trkl_py", "trkl_pz", "E/p",
               "h4_41", "h4_42", "h4_43", "h4_44", "h4_45", "h4_46"]

    # Writing to csv file
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)

        # Writing the headers
        writer.writerow(headers)

        # Writing the data
        writer.writerows(labeled_flat_list)
