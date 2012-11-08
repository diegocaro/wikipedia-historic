#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ElementTree
import re
import string
import sys

table = string.maketrans("","")

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


def clean_blanks(strIN):
    out = re.sub('[\s]+',' ', strIN)
    out = out.strip()
    return out

def main():

    context = ElementTree.iterparse(sys.stdin, events=("start", "end"))
    context = iter(context)
    event, root = context.next() # get the root element of the XML doc

    
    article = ""
    artid = ""
    timestamp = ""
    
    inrev = False
    #revid = ""
    
    ns = "{http://www.mediawiki.org/xml/export-0.6/}"

    for event, elem in context:
        if event == "start":            
            if elem.tag == ns+"revision":
                inrev = True
                #revid = ""
            elif elem.tag == ns+"page":
                inrev = False
            
                
        if event == "end":
            if elem.tag == ns+"title":
                article = clean_blanks(elem.text)
            elif inrev == False and elem.tag == ns+"id":
                artid = elem.text
            #elif inrev == True and revid == "" and elem.tag == ns+"id":
            #    revid = elem.text
            elif elem.tag == ns+"timestamp":
                timestamp = elem.text
            elif inrev == True and elem.tag == ns+"text":
                #print article, artid, timestamp, "link"
               
                l = re.findall("\[\[([^|\]]*)", elem.text)
                ll = map(clean_blanks,l)
                #for k in ll: print "%s\t%s\t%s\t%s\t%s" % (article,artid,timestamp,revid,k)
                #for k in ll: print "%s\t%s\t%s\t%s" % (timestamp,article,artid,k.encode('utf-8'))
                print "%s\t%s\t%s\t%s" % (timestamp, artid, article, len(ll)),
                for k in ll: print "\t%s" % (k.encode('utf-8')),
                print
    #inpage = False
    # 
    # for event, elem in context:
    #     if event == "start":
    #         if elem.tag == ns+"title":
    #             try:
    #                 if re.match("Category:", elem.text, flags=re.IGNORECASE ) :
    #                     cat = elem.text
    #                     subcat = cat[9:len(cat)].encode('utf-8')
    #                     inpage = True
    #             except:
    #                 pass
    # 
    # 
    #     if event == "end":        
    #         if elem.tag == ns+"page": # i want to write out all <page> entries
    #             elem.tail = None  
    #             inpage = False
    #             #print cElementTree.tostring( elem  )
    #             npage = npage + 1
    #             printProgress(npage)
    # 
    #         if elem.tag == ns+"text" and inpage:
    #             parentcats = []
    #     
    #             try:
    #                 parentcats = re.findall("\[\[Category:([^|\]]*)", elem.text, flags=re.IGNORECASE )
    #             except:
    #                 pass
    #             
    #     if elem.tag in [ns+"page"]:
    #         root.clear()  # when done parsing a section clear the tree to safe memory
    # 


main()
