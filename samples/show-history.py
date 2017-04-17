#!/usr/bin/env python
import sys
import pylab
import btceapi

# If an argument is provided to this script, it will be interpreted
# as a currency pair for which history should be displayed. Otherwise
# the BTC/USD history will be displayed.

if len(sys.argv) >= 2:
    pair = sys.argv[1]
    print("Showing history for %s" % pair)
else:
    print("No currency pair provided, defaulting to btc_usd")
    pair = "btc_usd"
    
history = btceapi.getTradeHistory(pair)

print(len(history))

pylab.plot([t.timestamp for t in history if t.type == u'ask'],
           [t.price for t in history if t.type == u'ask'], 'ro')

pylab.plot([t.timestamp for t in history if t.type == u'bid'],
           [t.price for t in history if t.type == u'bid'], 'go')

pylab.grid()          
pylab.show()
