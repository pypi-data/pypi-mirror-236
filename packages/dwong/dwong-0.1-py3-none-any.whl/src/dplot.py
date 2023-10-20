import dwong
import os
import matplotlib.pyplot as plt
from scipy.stats import binned_statistic_2d
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np



def emcal_evt(x, y, eng):
    x_bins = np.linspace(-150, 150, 50)
    y_bins = np.linspace(-150, 150, 50)
    bin_means = binned_statistic_2d(x, y, eng, statistic='mean', bins=[x_bins, y_bins])
    
    fig, ax = plt.subplots()
    im = ax.imshow(np.flip(bin_means.statistic.T, 0), extent=(-150, 150, -150, 150), aspect='auto')
    plt.colorbar(im, ax=ax, label='Energy Deposit/GeV')
    ax.set_xlabel('EMCal x Position/cm')
    ax.set_ylabel('EMCal y Position/cm')
    
    return fig

def emcal_pdf(ntuple_name, fname, absolute_path):
    print("Please put absolute path for n-tuple input")
    dq_events = dwong.getData(ntuple_name, "Events")
    x, y, eng = dwong.emcal_bytuple(dq_events)
    os.chdir(absolute_path)
    pdf_filename =  '%s.pdf' % fname
    pdf_pages = PdfPages(pdf_filename)
    for i in range(len(x)):
        try:
            fig = emcal_evt(x[i], y[i], eng[i])
            pdf_pages.savefig(fig)
            plt.close(fig)
        except:
            fig, ax = plt.subplots()  # Create a new figure and axis
            ax.set_title("Empty plot")
            pdf_pages.savefig(fig)
            plt.close(fig)
            
          
    pdf_pages.close()