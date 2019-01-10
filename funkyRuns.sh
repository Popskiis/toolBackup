#!/bin/bash

# Open our text file with the event numbers & the outgoing runs file
INFILE=./emptyEvents.txt
OUTFILE=./emptyRuns.txt

# loop over the events and find their respective run and subrun numbers
while read LINE; do
	echo $LINE

done < $INFILE
