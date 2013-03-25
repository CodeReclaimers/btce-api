import sys
import pylab
import numpy as np

sys.path.insert(0, "F:/btce-api/")
import btceapi

history = btceapi.getTradeHistory(sys.argv[1])

print len(history)

pylab.plot([t.date for t in history if t.trade_type == u'ask'],
           [t.price for t in history if t.trade_type == u'ask'], 'ro')

pylab.plot([t.date for t in history if t.trade_type == u'bid'],
           [t.price for t in history if t.trade_type == u'bid'], 'go')

pylab.grid()          
pylab.show()
