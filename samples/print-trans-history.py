import sys

import btceapi

if len(sys.argv) < 2:
    print "Usage: print-trans-history.py <key file>"
    print "    key file - Path to a file containing key/secret/nonce data"
    sys.exit(1)
    
key_file = sys.argv[1]   
# NOTE: In future versions, resaveOnDeletion will default to True.
handler = btceapi.KeyHandler(key_file, resaveOnDeletion=True)
for key in handler.getKeys():
    print "Printing info for key %s" % key

    # NOTE: In future versions, the handler argument will be required.
    t = btceapi.TradeAPI(key, handler=handler)

    try:
        th = t.transHistory()
        for h in th:
            print "\t\t        id: %r" % h.transaction_id
            print "\t\t      type: %r" % h.type
            print "\t\t    amount: %r" % h.amount
            print "\t\t  currency: %r" % h.currency
            print "\t\t      desc: %s" % h.desc
            print "\t\t    status: %r" % h.status
            print "\t\t timestamp: %r" % h.timestamp
            print
            
    except Exception as e:
        print "  An error occurred: %s" % e
        
