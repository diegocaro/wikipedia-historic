#!/usr/bin/env python

from operator import itemgetter
import sys


def printc(edge, timepoints, mintime=0, lastime=-1):
    timepoints = sorted(timepoints)
    
    if len(timepoints) % 2 == 1:
        timepoints.append(lastime)
    
    u,v = edge.split('-')
    
    for a,b in zip(timepoints[0::2], timepoints[1::2]):
    	if (a == b):
    	    print u,v,a-mintime,a+1-mintime
    	else:    
            print u,v,a-mintime,b-mintime
    

current_edge = None
current_time = []
edge = None
mintime = 0
lastime = -1

if len(sys.argv) > 1:
    mintime = int(sys.argv[1])
    lastime = int(sys.argv[2])


# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input
    u, v, time = line.split()

    edge = "-".join([u,v])

    time = int(time)
    
    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_edge == edge:
        current_time.append(time)
    else:
        if current_edge:
            # write result to STDOUT
            #print '%s\t%s' % (current_edge, current_time)
            printc(current_edge, current_time, mintime, lastime)
        del current_time[:]
        
        current_time.append(time)
        current_edge = edge

# do not forget to output the last word if needed!
if current_edge == edge:
    #print '%s\t%s' % (current_edge, current_time)
    printc(current_edge, current_time, mintime, lastime)
