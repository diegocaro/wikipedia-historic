import sys


def usage():
    print >> sys.stderr, "Error: file with titles is missing..."
    print >> sys.stderr, "%s <filetitles>" % (sys.argv[0])



titles = dict()
try:
    it = 0
    for line in open(sys.argv[1]):
        titles[line.strip()] = it
        it += 1
    
except:
    usage()
    exit(-1)
    

tget = titles.get
curr_title = None
curr_links = set()
title = None
time = 0
links = set()



for line in sys.stdin:
    line = line.strip()
    items = line.split("\t")
    
    title = tget(items[0])
    time = items[1]
    
    links = map(tget,items[2:])
    links = filter(lambda x: x != None, links)
    links = set(links)
    
    if title != curr_title:
        curr_links = set()
        
    #print title, time, links
    
    diff = curr_links.symmetric_difference(links)
    for l in diff:
        print title, l, time
    
    curr_title = title
    curr_links = links
    
    