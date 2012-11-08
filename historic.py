#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import re
import sys
import time
import cPickle as pickle
#import string
#table = string.maketrans("","")

class TitleId:
    def __init__(self):
        self.mapping = dict()
        self.newID = 0

    def getId(self, title):
        try:
            ret = self.mapping[title]
        except:
            self.mapping[title] = self.newID
            ret = self.newID
            self.newID = self.newID + 1

        return ret


def date2unixtime(data):
    return int(time.mktime(time.strptime(data, "%Y-%m-%dT%H:%M:%SZ")))

def clean_string(strIN):
    out = strIN
    
    ##badchars = "[^\w%s]+" % (re.escape(string.punctuation))
    badchars = "[^\w_-]+" 
    out = re.sub(badchars,' ', out)
    #out = out.translate(table, string.punctuation)

    #Removing extra spaces and underscores
    out = re.sub('[\s_]+',' ', out)
    out = out.strip()
    
    #Capitalize first letter of namespace and title page
    #out = str.join(':', [a.capitalize() for a in out.split(':')]);
    
    #Change spaces and underscores to underscores
    out = re.sub('[\s_]+','_', out)
    
    return out

def clean_tags(line):
    out = re.sub("<[^>]+>", " ", line)
    return out

def clean_blanks(strIN):
    #fast way :)
    return ' '.join(strIN.split())
# slow way   
#    out = re.sub('[\s]+',' ', strIN)
#    out = out.strip()
#    return out

def main():
    n = 0
    
    inPage = 0
    inRev = 0
    inText = 0
    
    title = ""
    pageID = 0
    timestamp = ""
    content = ""
    

    text = []

    if len(sys.argv) < 2:
        print "Run with %s <filepickle>" % (sys.argv[0])

    filepickle = sys.argv[1]
    try:
        title2id = pickle.load(open(filepickle, "rb"))
    except:
        title2id = TitleId()
    
    fmap = title2id.getId

    
    for line in sys.stdin:
        if n%1000000 == 0:
            sys.stderr.write("tick! id: %s (%s lines)\n" % (pageID, n))
        n = n+1
        
        if not inPage and "<page>" in line:
            inPage = 1
        elif inPage and "</page>" in line:
            inPage = 0
        elif inPage and "<title>" in line:
            title = clean_blanks(clean_tags(line))
            pageID = fmap(title)
#       elif inPage and not inRev and "<id>" in line:
#            pageID = line
        elif inPage and not inRev and "<revision>" in line:
            inRev = 1
        elif inPage and inRev and "</revision>" in line:
            inRev = 0
        elif inPage and inRev and "<timestamp>" in line:
            timestamp = clean_blanks(clean_tags(line))
            timeunix = date2unixtime(timestamp)
        elif inPage and inRev and "<text" in line:
            inText = 1
            text.append(line)
        elif inPage and inRev and "</text" in line:
            inText = 0
            
            text.append(line)

            content = ''.join(text)
            l = re.findall("\[\[([^|\]]*)", content)
            ll = map(clean_blanks, l)
            li = map(fmap, ll)
            li.sort()
            
            #print timeunix, pageID, len(li)#, li
            print "%s\t%s\t%s\t" %( timeunix, pageID, len(li) ),
            print '\t'.join(str(x) for x in li)

            ##print title
            #print pageID
            #print timestamp
            ##print content
            #print len(li)
            #print li
            
            del text[:]
        elif inText:
            text.append(line)

    pickle.dump(title2id, open(filepickle, "wb"))
main()
