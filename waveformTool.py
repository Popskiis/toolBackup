import ROOT, sys, os, time, math
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

#=================================== FUNCTIONS ========================================================================

def getKey(pair):
    return pair[0]

def plotChannelHits(waveform_data, UnsortedStartEnds, hit_triplet, channel, event, Type):
    x_min = 99999
    x_max = 0
    startEnds = sorted(UnsortedStartEnds, key=getKey)
    #  grab the smallest and largest values for the hits in the waveform
    for hit in startEnds:
        if hit[0] < x_min:
            x_min = hit[0]
        if hit[1] > x_max:
            x_max = hit[1]

    buf = len(waveform_data) - (x_max - x_min)
    buf = (x_max - x_min) / 2
    min_range = x_min - int(2*buf)
    max_range = x_max + int(2*buf)
    if min_range <= 0:
        min_range = 0
    if max_range >= 3072:
        max_range = 3072
    x_range = (min_range, max_range)
    #  print("START = {}    END = {}".format(x_range[0], x_range[1]))

    #  lets color the hits
    #  NOW COLOR HIT BY HIT SINCE IT HAS BEEN SORTED WE CAN JUST GO HIT BY HIT AND CHANGE COLORINGS
    num_hits = len(startEnds)
    for hit in xrange(num_hits):
        isHit = True

        if hit == 0:
            #  print("ZERO")
            #  print("START {}    STOP {}".format(x_range[0], startEnds[hit][0]))
            waveform_chunk = []
            time_chunk = []
            for number in xrange(x_range[0], startEnds[hit][0] + 1):
                waveform_chunk.append( waveform_data[number] )
                time_chunk.append(number)
            plt.plot(time_chunk, waveform_chunk, color='k')

        if isHit == True:
            #  print("TRUE")
            #  print("START {}    STOP {}".format(startEnds[hit][0], startEnds[hit][1]))
            waveform_chunk = []
            time_chunk = []
            for number in xrange(startEnds[hit][0], startEnds[hit][1] + 1):
                waveform_chunk.append( waveform_data[number] )
                time_chunk.append(number)
            plt.plot(time_chunk, waveform_chunk, color='g')
            isHit = False

        if hit > 0 and isHit == False:
            #  print("FALSE")
            #  print("START {}    STOP {}".format(startEnds[hit - 1][1], startEnds[hit][0] - 1))
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
    zt = []
    zv = []
    for triplet in hit_triplet:
        pt.append(triplet[0][0])
        pv.append(triplet[0][1])
        nt.append(triplet[1][0])
        nv.append(triplet[1][1])
        zt.append(triplet[2][0])
        zv.append(triplet[2][1])

    plt.scatter(pt, pv, c='r', s=50)
    plt.scatter(nt, nv, c='b', s=50)
    plt.scatter(zt, zv, c='#9933ff', s=50)
    plt.axhline(0, color="k")
    plt.xlabel("Time Tick")
    plt.ylabel("Signal Value [ADC]")
    plt.text(0.01, 0.02, "Green = ROI Hit\nRed Point = Pos. Peak\nBlue Point = Neg. Peak\nPurple Point = Zero Cross",
             bbox=dict(facecolor='c', alpha=0.5), 
             transform=plt.gca().transAxes)  

    #  plt.show(block=False)
    #  time.sleep(5)
    if Type == "ROI":
        plt.title("ROI Hit Coloring for Channel " + str(channel))
        plt.savefig("./hit_colored_images/hitColor_ev" + str(event) + "_ch" + str(channel) + ".pdf")
    elif Type == "PIX":
        plt.title("Pixel Hit Coloring for Channel " + str(channel))
        plt.savefig("./p_hit_colored_images/hitColor_ev" + str(event) + "_ch" + str(channel) + ".pdf")
    plt.close()
    return

#======================================================================================================================

#  channel = int(sys.argv[2])  #Random channel choice just for now - 172 was good too
event_num = int(sys.argv[1])

try:
    wavefile = ROOT.TFile.Open("./pixelHistos_{}.root".format(event_num))
    hitfile = ROOT.TFile.Open("./event_{}.root".format(event_num)) 
except Exception as e:
    raise e


pixlartree = hitfile.Get('pixlaranatree/pixlartree')
waveform_histos = wavefile.GetListOfKeys()

#  We need to find and store the channel number of our choosing
#    and also we need to store the start/end tick for a given hit
#    that was found and stored in the hitfile


#for now
ROIhisto = waveform_histos[1].ReadObj()
PIXhisto = waveform_histos[0].ReadObj()


for event in pixlartree:
    num_hits = len(event.sp_x)
    gooberList = []
    pbooberList = []

    for channel in event.sp_roiID:
        if channel not in gooberList:
            gooberList.append(channel)
            #  print("========================================\n")
            #  print "channel ", channel
            #  print("\n========================================\n")
        else:
            continue


        startEnds = []
        zipples = []
        waveform_data = []

        #  Store all of the data in the waveform for this channel
        for time_tick in xrange(1,3073):
            content = ROIhisto.GetBinContent(channel, time_tick)
            waveform_data.append(content)

        for hit in xrange(num_hits):  #Loop over all of the hits in an event ( here we only have the one )
            #  We want to find and store unique ROI hit start and end times as well as the center value
            if event.sp_roiID[hit] == channel:
                #  print("===================================================================================================================")
                if channel == 40:
                    print("**ROI**   Pos: {}   Cross: {}   Neg: {}".format(event.pos_peak_time_roi[hit], event.zero_cross_roi[hit], event.neg_peak_time_roi[hit]))
                #  print("**PIX**   Start: {}   Peak: {}   End: {}".format(event.start_tick_pix[hit], event.pos_peak_time_pix[hit], event.end_tick_pix[hit]))
                boundary_pair = (event.start_tick_roi[hit], event.end_tick_roi[hit])
                posPeak = (event.pos_peak_time_roi[hit], ROIhisto.GetBinContent(channel, event.pos_peak_time_roi[hit]+1))  # Time then value
                negPeak = (event.neg_peak_time_roi[hit], ROIhisto.GetBinContent(channel, event.neg_peak_time_roi[hit]+1))
                zeroCross = (event.zero_cross_roi[hit], ROIhisto.GetBinContent(channel, event.zero_cross_roi[hit]+1))
                hit_triplet = (posPeak, negPeak, zeroCross)
                if boundary_pair not in startEnds:
                    startEnds.append(boundary_pair)
                if hit_triplet not in zipples:
                    zipples.append(hit_triplet)  # Pos then neg

        #  plotChannelHits(waveform_data, startEnds, zipples, channel, event_num, "ROI")


###########################################################################################################################################################################################


    for pchannel in event.sp_pixelID:
        if pchannel not in pbooberList:
            pbooberList.append(pchannel)
            #  print("========================================\n")
            #  print "pchannel ", pchannel
            #  print("\n========================================\n")
        else:
            continue

        p_startEnds = []
        p_zipples = []
        p_waveform_data = []

        #  Store all of the data in the waveform for this pixel channel
        for time_tick in xrange(1,3073):
            content = PIXhisto.GetBinContent(pchannel, time_tick)
            p_waveform_data.append(content)
            
        for p_hit in xrange(num_hits):
            if event.sp_pixelID[p_hit] == pchannel:
                p_boundary_pair = (event.start_tick_pix[p_hit], event.end_tick_pix[p_hit])
                p_posPeak = (event.pos_peak_time_pix[p_hit], PIXhisto.GetBinContent(pchannel, event.pos_peak_time_pix[p_hit]+1))  # Time then value
                pixStart = (p_boundary_pair[0], PIXhisto.GetBinContent(pchannel, p_boundary_pair[0]+1))
                pixEnd = (p_boundary_pair[1], PIXhisto.GetBinContent(pchannel, p_boundary_pair[1]+1))
                p_hit_triplet = (pixStart, pixEnd, p_posPeak)
                if p_boundary_pair not in p_startEnds:
                    p_startEnds.append(p_boundary_pair)
                if p_hit_triplet not in p_zipples:
                    p_zipples.append(p_hit_triplet)  # Pos then neg

        #  Now we can plot it boi
        #  plotChannelHits(p_waveform_data, p_startEnds, p_zipples, pchannel, event_num, "PIX")




ROIhisto.Delete()
PIXhisto.Delete()

wavefile.Close()
hitfile.Close()
