import sys

import btceapi

if len(sys.argv) < 2:
    print "Usage: print-account-info-0.2.py <key file>"
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
        r = t.getInfo()
            
        for currency in btceapi.all_currencies:
            balance = getattr(r, "balance_" + currency)
            print "\t%s balance: %s" % (currency.upper(), balance)
        print "\tInformation rights: %r" % r.info_rights
        print "\tTrading rights: %r" % r.trade_rights
        print "\tWithrawal rights: %r" % r.withdraw_rights
        print "\tServer time: %r" % r.server_time
        print "\tItems in transaction history: %r" % r.transaction_count
        print "\tNumber of open orders: %r" % r.open_orders
        print "\topen orders:"
        orders = t.orderList()
        for o in orders:
            print "\t\torder id: %r" % o.order_id
            print "\t\t    type: %s" % o.type
            print "\t\t    pair: %s" % o.pair
            print "\t\t    rate: %s" % o.rate
            print "\t\t  amount: %s" % o.amount
            print "\t\t created: %r" % o.timestamp_created
            print "\t\t  status: %r" % o.status
            print
            
    except Exception as e:
        print "  An error occurred: %s" % e
        
