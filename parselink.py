import re
from util import *

class ParseLink:
    rem_links = re.compile("\[\[([^|\]]*)")


    def __init__(self):
        pass

    def run(self):
        n = 0
    
        inPage = 0
        inRev = 0
        inText = 0
    
        title = ""
        pageID = 0
        timestamp = ""
        content = ""
    

        text = []
    
        fclean = lambda x: x != None
    
        #for line in self.runProcess( self.cmdp7zip.split() ):
        for line in sys.stdin:
            line = line.decode('utf-8')
            n = n+1
            if n%1000000 == 0:
                sys.stderr.write("tick! title=%s (readlines=%s)\n" % (title.encode('utf8'), n))
        
            if not inPage and "<page>" in line:
                inPage = 1
            elif inPage and "</page>" in line:
                inPage = 0
            elif inPage and "<title>" in line:
                title = clean_string(clean_tags(line))
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
                l = self.rem_links.findall(content)
                ll = map(clean_string, l)
                #li = map(fmap, ll)
                ll = filter(fclean, ll)
                ll = list(set(ll)) #uniq elements
                            
                print "%s\t%s\t" %( title.encode('utf8'), timeunix),
                print '\t'.join(x.encode('utf8') for x in ll)
            
                del text[:]
            elif inText:
                text.append(line)


def profile(function, *args, **kwargs):
    """ Returns performance statistics (as a string) for the given function.
    """
    def _run():
        function(*args, **kwargs)
    import cProfile as profile
    import pstats
    import os
    import sys; sys.modules['__main__'].__profile_run__ = _run
    id = function.__name__ + '()'
    profile.run('__profile_run__()', id)
    p = pstats.Stats(id)
    p.stream = open(id, 'w')
    p.sort_stats('time').print_stats(20)
    p.stream.close()
    s = open(id).read()
    os.remove(id)
    return s

def run():
    p = ParseLink()
    p.run()
    
if __name__ == "__main__":
    import sys
    p = ParseLink()
    p.run()
    #print >> sys.stderr,  profile(run)