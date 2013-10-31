#!/usr/bin/python
import btceapi

attrs = ('high', 'low', 'avg', 'vol', 'vol_cur', 'last',
         'buy', 'sell', 'updated', 'server_time')

print "Tickers:"
connection = btceapi.BTCEConnection()
for pair in btceapi.all_pairs:
    ticker = btceapi.getTicker(pair, connection)
    print pair
    for a in attrs:
        print "\t%s %s" % (a, getattr(ticker, a))
