import sys
import pylab
import numpy as np

import btceapi

pair = sys.argv[1]

asks, bids = btceapi.getDepth(pair)

print len(asks), len(bids)

ask_prices, ask_volumes = zip(*asks)
bid_prices, bid_volumes = zip(*bids)

pylab.plot(ask_prices, np.cumsum(ask_volumes), 'r-')
pylab.plot(bid_prices, np.cumsum(bid_volumes), 'g-')
pylab.grid()
pylab.title("%s depth" % pair)
pylab.show()
