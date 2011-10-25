#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" ccor

    Checks for a working internet connection. If that fails the 
    router will be restarted.
    
    Pure python implementation without any external libraries.

    Author: marpie (marpie@a12d404.net)

    Last Update:  20111025
    Created:      20111025

"""
import random
import datetime
import urllib2


# Version Information
__version__ = "0.0.1"
__program__ = "ccor v" + __version__
__author__ = "marpie"
__email__ = "marpie+ccor@a12d404.net"
__license__ = "BSD License"
__copyright__ = "Copyright 2011, a12d404.net"
__status__ = "Prototype"  # ("Prototype", "Development", "Testing", "Production")


LOG=True
LOG_FILE=r'ccor.log'
ROUTER_URL = r'http://192.168.100.1/goform/ChannelsSelection'
ROUTER_COMMAND = r'SADownStartingFrequency=570000000'


SITES_WORLD = (
    'https://encrypted.google.com/', 
    'https://mail.google.com/', 
    'https://www.bankofamerica.com/', 
    'http://www.akamai.com/',
    'http://www.google.com', 
    'http://www.facebook.com', 
    'http://www.youtube.com', 
    'http://www.yahoo.com', 
    'http://www.wikipedia.org', 
    'http://www.baidu.com', 
    'http://www.blogspot.com', 
    'http://www.live.com', 
    'http://www.twitter.com', 
    'http://www.qq.com', 
    'http://www.amazon.com', 
    'http://www.msn.com', 
    'http://www.yahoo.co.jp', 
    'http://www.linkedin.com', 
    'http://www.wordpress.com', 
    'http://www.ebay.com', 
    'http://www.apple.com', 
    'http://www.microsoft.com', 
    'http://www.flickr.com', 
    'http://www.craigslist.org', 
    'http://www.imdb.com', 
)

SITES_DE = (
    'http://www.spiegel.de', 
    'http://www.t-online.de', 
    'http://www.gmx.net', 
    'http://www.heise.de', 
    'http://www.web.de', 
    'http://dict.leo.org', 
    'http://www.freenet.de', 
    'http://www.stern.de', 
    'http://www.arcor.de', 
    'http://www.n-tv.de', 
    'http://www.pcwelt.de', 
    'http://www.sueddeutsche.de', 
    'http://www.faz.net', 
    'http://www.idealo.de', 
    'http://www.dpa-plattform.de', 
    'http://www.gutefrage.net', 
)

USE_SITES = list(SITES_DE)


def log(line, init=False):
    if not LOG:
        return
    
    if init:
        f = open(LOG_FILE, 'w')
    else:
        f = open(LOG_FILE, 'a')
    
    f.write(line)
    f.write('\n')
    
    f.close()    


def getHttp(url):
    try:
        return urllib2.urlopen(url).read()
    except:
        return None


def postHttp(post_url, post_data):
    try:
        return urllib2.urlopen(urllib2.Request(url=post_url, data=post_data)).read()
    except:
        return None


def isWebsiteOnline(url):
    return getHttp(url) <> None


def isOnline():
    for url in USE_SITES:
        if isWebsiteOnline(url):
            log('[+] %s online.' % url)
            return True
        else:
            log('[X] %s is offline!!' % url)
    log('[X] all sites are offline!')
    return False


def restartRouter():
    log('[*] Resetting router')
    post_result = postHttp(ROUTER_URL, ROUTER_COMMAND)
    res = post_result.find('The device has been reset...') <> -1
    if not res:
        log('[X] Reset failed!!!')
    return res


# Main
def main(argv):
    log('[*] ccor started -> ' + datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M:%S %p"), True)
    random.shuffle(USE_SITES)
    if not isOnline():
        restartRouter()
    log('[*] done.')
    
    return True


if __name__ == "__main__":
    import sys
    sys.exit( not main( sys.argv ) )
