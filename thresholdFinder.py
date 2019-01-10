import ROOT,sys,os,time
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import math


#==================================== FUNCTIONS ========================================================================================================================
#  Actually finds the std deviation
def findRMS(waveform_data):
    if len(waveform_data) == 0:
        return 0.0
    data_sum = 0
    sq_data_sum = 0
    for entry in waveform_data:
        data_sum += entry
        sq_data_sum += entry*entry
    mean = data_sum/len(waveform_data)
    variance = (sq_data_sum/len(waveform_data)) - (mean*mean)
    return math.sqrt(variance)

def plotDistribution(distribution_values, Type):
        mean_rms = np.mean(distribution_values)
        SDev = np.std(distribution_values)
        # Text box to show the mean rms, made to have a red text box and transform allows relative scaling for the postion
        plt.hist(distribution_values,97)
        plt.text(0.2, 0.8, 'Mean = {}\nStd. Dev. = {}'.format(mean_rms,SDev), 
                 bbox=dict(facecolor='red', alpha=0.5), 
                 transform=plt.gca().transAxes)  
        if Type == "ROI":
            plt.title("Mean RMS for all ROI")
            plt.xlabel("Mean RMS Value")
            plt.ylabel("Count")
            plt.show(block=False)  #block=False is to stop the plot from interruptin the script
            time.sleep(15)
            plt.savefig(Type + "_Noise.pdf")
        elif Type == "PIX":
            plt.title("Mean RMS for all Pixels")
            plt.xlabel("Mean RMS Value")
            plt.ylabel("Count")
            plt.show(block=False)  #block=False is to stop the plot from interruptin the script
            time.sleep(15)
            plt.savefig(Type + "_Noise.pdf")
        plt.close()
        return

def plotCvRMS(channels, meanRMS_values, Type):
        mean_rms = np.mean(meanRMS_values)
        SDev = np.std(meanRMS_values)
        # Text box to show the mean rms, made to have a red text box and transform allows relative scaling for the postion
        plt.scatter(channels, meanRMS_values)
        plt.text(0.3, 0.1, 'Mean = {}\nStd. Dev. = {}'.format(mean_rms,SDev), 
                 bbox=dict(facecolor='red', alpha=0.5), 
                 transform=plt.gca().transAxes)  
        if Type == "ROI":
            plt.title("Channel vs. ROI Mean RMS")
            plt.xlabel("Channel Number")
            plt.ylabel("Mean RMS Value")
            plt.show(block=False)  #block=False is to stop the plot from interruptin the script
            time.sleep(15)
            plt.savefig(Type + "channel_vs_meanRMS.pdf")
        elif Type == "PIX":
            plt.title("Channel vs. Pixel Mean RMS")
            plt.xlabel("Channel Number")
            plt.ylabel("Mean RMS Value")
            plt.show(block=False)  #block=False is to stop the plot from interruptin the script
            time.sleep(15)
            plt.savefig(Type + "channel_vs_meanRMS.pdf")
        plt.close()
        return
    



#==================================== MAIN FUNCTION ====================================================================================================================

#  open our empty event waveforms.
try:
    empty_events = ROOT.TFile.Open("./emptyEvents.root")
    ofile = open("meanRMS_ROIchannels.txt", "w")
except IOError as io:
    raise io

#  Now we can access a TList of TObjects from the root file.
waveform_histos = empty_events.GetListOfKeys()

#  Some initialized arrays used for mean RMS distribution plotting
pix_channel_meanRMS = []
roi_channel_meanRMS = []
channel_index = np.arange(240)

#  Loop over all channels in the histogram, there are 240 channels
#    Then loop over all of the events by accessing a histo from a new object in the list
#    Then loop over all time ticks in the waveform for a given channel
for channel in xrange(240):
    #  Some initializations
    temp_ROI_rms = []
    temp_PIX_rms = []

    for histo in waveform_histos:
        realHisto = histo.ReadObj()           #Get the real histogram - type TH2D from the object list so we can have member functions
        histoType = realHisto.GetName()[:3]   #First three letters of the histogram name to distiguish roi from pixel waveforms
        waveform_data = []

        for time_tick in xrange(3072):
            content = realHisto.GetBinContent(channel, time_tick)
            waveform_data.append(content)

        if histoType == "ROI":
            temp_ROI_rms.append( findRMS(waveform_data) )
        elif histoType == "Pix":
            temp_PIX_rms.append( findRMS(waveform_data) )
        #  Delete the histograms so it doesn't waste memory - it doesnt delete itself
        realHisto.Delete()

    #  Add channel mean RMS values to their respective arrays after we have looped over all waveforms for a channel
    roi_channel_meanRMS.append( np.mean(temp_ROI_rms) )
    pix_channel_meanRMS.append( np.mean(temp_PIX_rms) )
    ofile.write( str(np.mean(temp_ROI_rms)) + "\n" )

#  Now we can plot distributions and take a look
plotDistribution(roi_channel_meanRMS, "ROI")
plotDistribution(pix_channel_meanRMS, "PIX")
plotCvRMS(channel_index, roi_channel_meanRMS, "ROI")
plotCvRMS(channel_index, pix_channel_meanRMS, "PIX")

#  Close our files
empty_events.Close()
ofile.close()
