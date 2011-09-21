#!/usr/bin/env python
import urllib2
from kannel_utils.settings import KANNEL_RESTART

def reload_whitelists():

    try:
        response=urllib2.urlopen(KANNEL_RESTART)
        print "restarting...."

    except urllib2.URLError, e:
        if not hasattr(e, "code"):
            raise
        print e


if __name__=='__main__':
    reload_whitelists()

    
    

