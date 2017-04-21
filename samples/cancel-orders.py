#!/usr/bin/env python
import sys
import btceapi

# This sample shows use of a KeyHandler.  For each API key in the file
# passed in as the first argument, all pending orders for the specified
# pair and type will be canceled.

if len(sys.argv) < 4:
    print("Usage: cancel-orders.py <key file> <pair> <order type>")
    print("    key file - Path to a file containing key/secret/nonce data")
    print("    pair - A currency pair, such as btc_usd")
    print("    order type - Type of orders to process, either 'buy' or 'sell'")
    sys.exit(1)

key_file = sys.argv[1]
pair = sys.argv[2]
order_type = sys.argv[3]

with btceapi.KeyHandler(key_file) as handler:
    if not handler.keys:
        print("No keys in key file.")
    else:
        for key in handler.keys:
            print("Canceling orders for key {}".format(key))

            with btceapi.BTCEConnection() as connection:
                t = btceapi.TradeAPI(key, handler, connection)

                try:
                    # Get a list of orders for the given pair, and cancel the ones
                    # with the correct order type.
                    orders = t.activeOrders(pair=pair)
                    for o in orders:
                        if o.type == order_type:
                            print("  Canceling {} {} order for {:f} @ {:f}".format(
                                pair, order_type, o.amount, o.rate))
                            t.cancelOrder(o.order_id)

                    if not orders:
                        print("  There are no {} {} orders".format(pair, order_type))
                except Exception as e:
                    print("  An error occurred: {}".format(e))
