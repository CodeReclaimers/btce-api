#!/usr/bin/python
import sys

import btceapi

if len(sys.argv) < 2:
    print "Usage: compute-account-value.py <key file>"
    print "    key file - Path to a file containing key/secret/nonce data"
    sys.exit(1)

key_file = sys.argv[1]
with btceapi.KeyHandler(key_file, resaveOnDeletion=True) as handler:
    for key in handler.getKeys():
        print "Computing value for key %s" % key

        # NOTE: In future versions, the handler argument will be required.
        conn = btceapi.BTCEConnection()
        t = btceapi.TradeAPI(key, handler=handler)

        try:
            r = t.getInfo(connection = conn)

            exchange_rates = {}
            for pair in btceapi.all_pairs:
                asks, bids = btceapi.getDepth(pair)
                exchange_rates[pair] = bids[0][0]

            btc_total = 0
            for currency in btceapi.all_currencies:
                balance = getattr(r, "balance_" + currency)
                if currency == "btc":
                    print "\t%s balance: %s" % (currency.upper(), balance)
                    btc_total += balance
                else:
                    pair = "%s_btc" % currency
                    if pair in btceapi.all_pairs:
                        btc_equiv = balance * exchange_rates[pair]
                    else:
                        pair = "btc_%s" % currency
                        btc_equiv = balance / exchange_rates[pair]

                    bal_str = btceapi.formatCurrency(balance, pair)
                    btc_str = btceapi.formatCurrency(btc_equiv, "btc_usd")
                    print "\t%s balance: %s (~%s BTC)" % (currency.upper(), bal_str, btc_str)
                    btc_total += btc_equiv

            print "\tCurrent value of open orders:"
            orders = t.activeOrders(connection = conn)
            if orders:
                for o in orders:
                    # TODO: handle pairs that don't involve BTC
                    btc_equiv = o.amount * exchange_rates[o.pair]
                    btc_str = btceapi.formatCurrency(btc_equiv, pair)
                    print "\t\t%s %s %s @ %s (~%s BTC)" % (o.type, o.amount, o.pair, o.rate, btc_str)
                    btc_total += btc_equiv
            else:
                print "\t\tThere are no open orders."

            btc_str = btceapi.formatCurrency(btc_total, "btc_usd")
            print "\n\tTotal estimated value: %s BTC" % btc_str
            for fiat in ("usd", "eur", "rur"):
                fiat_pair = "btc_%s" % fiat
                fiat_total = btc_total * exchange_rates[fiat_pair]
                fiat_str = btceapi.formatCurrencyDigits(fiat_total, 2)
                print "\t                       %s %s" % (fiat_str, fiat.upper())

        except Exception as e:
            print "  An error occurred: %s" % e
            raise e

