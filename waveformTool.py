import ROOT, sys, os, time, math
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

#=================================== FUNCTIONS ========================================================================

def getKey(pair):
    return pair[0]

def plotChannelHits(waveform_data, UnsortedStartEnds, peaks):
    x_min = 99999
    x_max = 0
    startEnds = sorted(UnsortedStartEnds, key=getKey)
    #  grab the smallest and largest values for the hits in the waveform
    for hit in startEnds:
        print(hit[0])
        if hit[0] < x_min:
            x_min = hit[0]
        if hit[1] > x_max:
            x_max = hit[1]

    buf = len(waveform_data) - (x_max - x_min)
    buf = (x_max - x_min) / 2
    x_range = (x_min - int(buf), x_max + int(buf))
    print("START = {}    END = {}".format(x_range[0], x_range[1]))

    #  lets color the hits
    #  NOW COLOR HIT BY HIT SINCE IT HAS BEEN SORTED WE CAN JUST GO HIT BY HIT AND CHANGE COLORINGS
    num_hits = len(startEnds)
    for hit in xrange(num_hits):
        isHit = True
        print(hit)

        if hit == 0:
            print("ZERO")
            print("START {}    STOP {}".format(x_range[0], startEnds[hit][0]))
            waveform_chunk = []
            time_chunk = []
            for number in xrange(x_range[0], startEnds[hit][0] + 1):
                waveform_chunk.append( waveform_data[number] )
                time_chunk.append(number)
            plt.plot(time_chunk, waveform_chunk, color='k')

        if isHit == True:
            print("TRUE")
            print("START {}    STOP {}".format(startEnds[hit][0], startEnds[hit][1]))
            waveform_chunk = []
            time_chunk = []
            for number in xrange(startEnds[hit][0], startEnds[hit][1] + 1):
                waveform_chunk.append( waveform_data[number] )
                time_chunk.append(number)
            plt.plot(time_chunk, waveform_chunk, color='g')
            isHit = False

        if hit > 0 and isHit == False:
            print("FALSE")
            print("START {}    STOP {}".format(startEnds[hit - 1][1], startEnds[hit][0] - 1))
            waveform_chunk = []
            time_chunk = []
            for number in xrange(startEnds[hit - 1][1], startEnds[hit][0]):
                waveform_chunk.append( waveform_data[number] )
                time_chunk.append(number)
            plt.plot(time_chunk, waveform_chunk, color='k')
            isHit = True

    #  Plot the last bit of the waveform now
    waveform_chunk = []
    time_chunk = []
    for number in xrange(startEnds[num_hits - 1][1], x_range[1]):
        waveform_chunk.append( waveform_data[number] )
        time_chunk.append(number)
    plt.plot(time_chunk, waveform_chunk, color='k')

    #  add peaks of the hits and add some titles and eye candy
    pt = []
    pv = []
    nt = []
    nv = []
    for pair in peaks:
        pt.append(pair[0][0])
        pv.append(pair[0][1])
        nt.append(pair[1][0])
        nv.append(pair[1][1])

    plt.scatter(pt, pv, c='r', s=50)
    plt.scatter(nt, nv, c='b', s=50)
    plt.title("YEA")
    plt.xlabel("xXx")
    plt.ylabel("SUP")
    plt.show(block=False)
    time.sleep(15)
    plt.close()
    return

#======================================================================================================================

channel = 156  #Random channel choice just for now - 172 was good too

try:
    wavefile = ROOT.TFile.Open("./pixelHistos_4230022.root")
    hitfile = ROOT.TFile.Open("./event_4230022.root") 
except Exception as e:
    raise e


pixlartree = hitfile.Get('pixlaranatree/pixlartree')
waveform_histos = wavefile.GetListOfKeys()

#  We need to find and store the channel number of our choosing
#    and also we need to store the start/end tick for a given hit
#    that was found and stored in the hitfile

startEnds = []
peaks = []

#for now
ROIhisto = waveform_histos[1].ReadObj()
waveform_data = []
#  Store all of the data in the waveform for this channel
for time_tick in xrange(3072):
    content = ROIhisto.GetBinContent(channel, time_tick)
    waveform_data.append(content)

for event in pixlartree:
    num_hits = len(event.sp_x)

    for hit in xrange(num_hits):  #Loop over all of the hits in an event ( here we only have the one )
        #  We want to find and store unique ROI hit start and end times as well as the center value
        if event.sp_roiID[hit] == channel:
            #  print("===================================================================================================================")
            #  print("**ROI**   Pos: {}   Cross: {}   Neg: {}".format(event.pos_peak_time_roi[hit], event.zero_cross_roi[hit], event.neg_peak_time_roi[hit]))
            #  print("**PIX**   Start: {}   Peak: {}   End: {}".format(event.start_tick_pix[hit], event.pos_peak_time_pix[hit], event.end_tick_pix[hit]))
            boundary_pair = (event.start_tick_roi[hit], event.end_tick_roi[hit])
            posPeak = (event.pos_peak_time_roi[hit], ROIhisto.GetBinContent(channel, event.pos_peak_time_roi[hit]))  # Time then value
            negPeak = (event.neg_peak_time_roi[hit], ROIhisto.GetBinContent(channel, event.neg_peak_time_roi[hit]))
            peak_pair = (posPeak, negPeak)
            if boundary_pair not in startEnds:
                startEnds.append(boundary_pair)
            if peak_pair not in peaks:
                peaks.append(peak_pair)  # Pos then neg
            

#  Now we can plot it boi
plotChannelHits(waveform_data, startEnds, peaks)




ROIhisto.Delete()

wavefile.Close()
hitfile.Close()
