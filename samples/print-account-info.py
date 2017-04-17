#!/usr/bin/env python
import sys
import btceapi

if len(sys.argv) < 2:
    print("Usage: print-account-info.py <key file>")
    print("    key file - Path to a file containing key/secret/nonce data")
    sys.exit(1)

key_file = sys.argv[1]
with btceapi.KeyHandler(key_file) as handler:
    if not handler.keys:
        print("No keys in key file.")
    else:
        for key in handler.keys:
            print("Printing info for key {}".format(key))

            with btceapi.BTCEConnection() as connection:
                t = btceapi.TradeAPI(key, handler, connection)

                try:
                    r = t.getInfo()
                    currencies = list(r.funds.keys())
                    currencies.sort()
                    for currency in currencies:
                        balance = r.funds[currency]
                        print("\t{} balance: {}".format(currency.upper(), balance))
                    print("\tInformation rights: {}".format(r.info_rights))
                    print("\tTrading rights: {}".format(r.trade_rights))
                    print("\tWithrawal rights: {}".format(r.withdraw_rights))
                    print("\tServer time: {}".format(r.server_time))
                    print("\tItems in transaction history: {}".format(r.transaction_count))
                    print("\tNumber of open orders: {}".format(r.open_orders))
                    print("\topen orders:")
                    orders = t.activeOrders()
                    if orders:
                        for o in orders:
                            print("\t\torder id: {}".format(o.order_id))
                            print("\t\t    type: {}".format(o.type))
                            print("\t\t    pair: {}".format(o.pair))
                            print("\t\t    rate: {}".format(o.rate))
                            print("\t\t  amount: {}".format(o.amount))
                            print("\t\t created: {}".format(o.timestamp_created))
                            print("\t\t  status: {}".format(o.status))
                            print()
                    else:
                        print("\t\tno orders")

                    print("\tTrade history:")
                    trade_history = t.tradeHistory()
                    if trade_history:
                        for th in trade_history:
                            print("\t\ttransaction_id: {}".format(th.transaction_id))
                            print("\t\t          pair: {}".format(th.pair))
                            print("\t\t          type: {}".format(th.type))
                            print("\t\t        amount: {}".format(th.amount))
                            print("\t\t          rate: {}".format(th.rate))
                            print("\t\t      order_id: {}".format(th.order_id))
                            print("\t\t is_your_order: {}".format(th.is_your_order))
                            print("\t\t     timestamp: {}".format(th.timestamp))
                            print()
                    else:
                        print("\t\tno items in trade history")

                except Exception as e:
                    print("  An error occurred: {}".format(e))
                    raise e
