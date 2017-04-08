#!/usr/bin/python
import btceapi

attrs = ('high', 'low', 'avg', 'vol', 'vol_cur', 'last',
         'buy', 'sell', 'updated')

print "Tickers:"
connection = btceapi.BTCEConnection()
info = btceapi.APIInfo(connection)
for pair in info.pair_names:
    ticker = btceapi.getTicker(pair, connection)
    print pair
    for a in attrs:
        print "\t%s %s" % (a, getattr(ticker, a))
