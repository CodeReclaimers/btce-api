#!/usr/bin/env python
import decimal
import sys
import btceapi

# This sample shows how to place a single trade order for each key in the provided file.

if len(sys.argv) < 4:
    print("Usage: place-order.py <key file> <pair> <order type> <amount> <price>")
    print("    key file - Path to a file containing key/secret/nonce data")
    print("    pair - A currency pair, such as btc_usd")
    print("    order type - Type of orders to process, either 'buy' or 'sell'")
    print("    amount - Amount of currency in order")
    print("    price - Order price")
    sys.exit(1)

key_file = sys.argv[1]
pair = sys.argv[2]
order_type = sys.argv[3]
amount = decimal.Decimal(sys.argv[4])
price = decimal.Decimal(sys.argv[5])

with btceapi.KeyHandler(key_file) as handler:
    if not handler.keys:
        print("No keys in key file.")
    else:
        for key in handler.keys:
            print("Placing order for key {}".format(key))

            with btceapi.BTCEConnection() as connection:
                t = btceapi.TradeAPI(key, handler, connection)

                try:
                    result = t.trade(pair, order_type, price, amount)

                    print("Trade result:")
                    print("   received: {0}".format(result.received))
                    print("    remains: {0}".format(result.remains))
                    print("   order_id: {0}".format(result.order_id))
                    print("      funds:")
                    for c, v in result.funds.items():
                        print("        {} {}".format(c, v))

                except Exception as e:
                    print("  An error occurred: {}".format(e))
