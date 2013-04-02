import sys
import btceapi

# This sample shows use of a KeyHandler.  For each API key in the file
# passed in as the first argument, all pending orders for the specified
# pair and type will be canceled. 

if len(sys.argv) < 4:
    print "Usage: cancel_orders.py <key file> <pair> <order type>"
    print "    key file - Path to a file containing key/secret/nonce data"
    print "    pair - A currency pair, such as btc_usd"
    print "    order type - Type of orders to process, either 'buy' or 'sell'"
    sys.exit(1)
    
key_file = sys.argv[1]   
pair = sys.argv[2]
order_type = unicode(sys.argv[3])

handler = btceapi.KeyHandler(key_file)
for key, (secret, nonce) in handler.keys.items():
    print "Canceling orders for key %s" % key
    
    t = btceapi.TradeAPI(key, secret, nonce)

    try:
        # Get a list of orders for the given pair, and cancel the ones
        # with the correct order type.
        orders = t.orderList(pair = pair)
        for o in orders:
            if o.type == order_type:
                print "  Canceling %s %s order for %f @ %f" % (pair, order_type,
                    o.amount, o.rate)
                t.cancelOrder(o.order_id)
                
        if not orders:
            print "  There are no %s %s orders" % (pair, order_type)
    except Exception as e:
        print "  An error occurred: %s" % e
        
    # Give the next nonce to the handler so it can update the key file.
    handler.setNextNonce(key, t.next_nonce())
    
handler.save(key_file)    