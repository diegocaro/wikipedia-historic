#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# Some rules on wikipedia articles name:
# 1. Capitalizacion matters, except in the first letter
# 2. White spaces are converted to "_"
# 3. White spaces at the end are removed
# 4. Spacenames and entry title are separated by ":"
# 5. Accents matters!
# More info at http://en.wikipedia.org/wiki/Wikipedia:Page_name
#


import re
import time
import sys

rem_tags = re.compile("<[^>]+>")
rem_badchars = re.compile("[^\w:_-]+")
rem_spaces = re.compile("[\s_]+")

import HTMLParser
h = HTMLParser.HTMLParser()
def unescape(s):
    global h
    try:
        return h.unescape(s)
    except:
        print >> sys.stderr, "Error with string: '", s, "'"
        return s

## This is slower than unescape
from htmlentitydefs import name2codepoint
def htmlentitydecode(s):
    return re.sub('&(%s);' % '|'.join(name2codepoint),
            lambda m: unichr(name2codepoint[m.group(1)]), s)


import unicodedata
def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
def clean_tags(line):
    out = rem_tags.sub(" ", line)
    return out

def clean_blanks(strIN):
    #fast way :)
    return ' '.join(strIN.split())
# slow way   
#    out = re.sub('[\s]+',' ', strIN)
#    out = out.strip()
#    return out

def date2unixtime(data):
    return int(time.mktime(time.strptime(data, "%Y-%m-%dT%H:%M:%SZ")))


def clean_string(strIN):
    #out = strip_accents(unescape(unescape(strIN)))
    out = unescape(unescape(strIN))

    ##badchars = "[^\w%s]+" % (re.escape(string.punctuation))
    ##badchars = "[^\w_-]+" 
    ##out = rem_badchars.sub(' ', out)
    #out = out.translate(table, string.punctuation)

    #Removing extra spaces and underscores
    #out = rem_spaces.sub(' ', out)
    #out = out.strip()
    out = ' '.join(out.split()) ##fast way than using re
    
    #Change spaces and underscores to underscores
    out = rem_spaces.sub('_', out)

    #out = out[0].upper() + out[1:]
    if (len(out) == 1): out = out[0].upper()
    elif (len(out) > 1): out = out[0].upper() + out[1:]

    return out