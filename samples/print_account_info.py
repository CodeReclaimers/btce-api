import time
import sys
import pylab
import numpy as np
import random

import btceapi

#NOTE: This is the original version of this script; it still runs with
#version 0.2 of the API, but will produce lots of warnings.  Please 
#see print-account-info-0.2.py to see recommended usage for that version.

if len(sys.argv) < 2:
    print "Usage: print_account_info.py <key file>"
    print "    key file - Path to a file containing key/secret/nonce data"
    sys.exit(1)
    
key_file = sys.argv[1]   
handler = btceapi.KeyHandler(key_file)
for key, (secret, nonce) in handler.keys.items():
    print "Printing info for key %s" % key

    t = btceapi.TradeAPI(key, secret, nonce)

    try:
        r = t.getInfo()
        for d in dir(r):
            if d[:2] == '__':
                continue
            
            print "    %s: %r" % (d, getattr(r, d))
    except Exception as e:
        print "  An error occurred: %s" % e
        
    # Give the next nonce to the handler so it can update the key file.
    handler.setNextNonce(key, t.next_nonce())
    
handler.save(key_file)            
