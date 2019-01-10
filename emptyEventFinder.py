import sys, ROOT, math, os
import matplotlib as mpl

#  open in and out files
infile = ROOT.TFile.Open("./anaTree_updated_histo.root")
outfile = open("emptyEvents.txt","w")
pixlartree = infile.Get('pixlaranatree/pixlartree')

#  Random stuffs to make sure outfile works
#  print "File name: ", outfile.name
#  print "File status: ", outfile.closed
#  print "File mode: ", outfile.mode

num_entries = 0
every_tenth = 0
#  Loop over events in anaTree
for row in pixlartree:
    #  Iterate every tenth entry and skip if we are in between
    every_tenth += 1
    if (every_tenth % 10) != 0:
        continue
    #  Only look for empty events
    if len(row.sp_x) == 0:
        print('Event: {}   ||   Run: {}   ||   Subrun: {}'.format(row.event,row.run,row.subrun))
        #  Parse writing into to cases based on zeroes for lookup in lar raw files
        #  if len(str(row.subrun)) == 3:
        #      outfile.write( "{},0{},0{}\n".format(row.event,row.run,row.subrun) )
        #  elif len(str(row.subrun)) == 2:
        #      outfile.write( "{},0{},00{}\n".format(row.event,row.run,row.subrun) )
        num_entries += 1
        if num_entries == 100:
            break
print "Num Entries: ", num_entries

infile.Close
outfile.close
