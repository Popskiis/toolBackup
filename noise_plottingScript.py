import ROOT,sys,os,time
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import math

#  Open the file and read line by line splitting the z and y coordinates
with open("./elJefe.txt", "r") as coordFile:
    with open("./meanRMS_ROIchannels.txt") as rmsFile:

        z_ax = []
        y_ax = []
        rms = []

        #  Get lists with each line split without newlines
        clist = coordFile.read().splitlines()
        rmslist = rmsFile.read().splitlines()

        for increment in xrange(240): 
            cline = clist[increment]
            mean_rms = rmslist[increment]
            y_coord, z_coord = cline.split(",")
            z_ax.append(z_coord)
            y_ax.append(y_coord)
            rms.append(mean_rms)
            #  print("{}, {}   {}".format(y_coord, z_coord, mean_rms))

        #  Now we make the contour plot
        plt.scatter(z_ax, y_ax, c=rms, marker='s', s=50)
        plt.title("Average ROI Waveform RMS in Y-Z Plane")
        plt.xlabel("Z Position [cm]")
        plt.ylabel("Y Position [cm]")
        plt.colorbar()
        plt.show(block=False)
        time.sleep(5)
        plt.savefig("zy_rmsPlot.pdf")
        plt.close()
