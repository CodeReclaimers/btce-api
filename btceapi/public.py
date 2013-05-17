# Copyright (c) 2013 Alan McIntyre

import datetime
import decimal

import common

def getDepth(pair):
    '''Retrieve the depth for the given pair.  Returns a tuple (asks, bids);
    each of these is a list of (price, volume) tuples.'''
    
    common.validatePair(pair)
    
    depth = common.makeJSONRequest("/api/2/%s/depth" % pair)
    if type(depth) is not dict:
        raise Exception("The response is not a dict.")
    
    asks = depth.get(u'asks')
    if type(asks) is not list:
        raise Exception("The response does not contain an asks list.")
        
    bids = depth.get(u'bids') 
    if type(bids) is not list:
        raise Exception("The response does not contain a bids list.")
    
    return asks, bids
    
   
class Trade(object):
    __slots__ = ('pair', 'trade_type', 'price', 'tid', 'amount', 'date')
    
    def __init__(self, **kwargs):
        for s in Trade.__slots__:
            u = unicode(s)
            setattr(self, s, kwargs.get(s))
        
        if type(self.date) in (int, float, decimal.Decimal):
            self.date = datetime.datetime.fromtimestamp(self.date)
        elif type(self.date) in (str, unicode):
            if "." in self.date:
                self.date = datetime.datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S.%f")
            else:
                self.date = datetime.datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S")
    
def getTradeHistory(pair):
    '''Retrieve the trade history for the given pair.  Returns a list of 
    Trade instances.'''
    
    common.validatePair(pair)
    
    history = common.makeJSONRequest("/api/2/%s/trades" % pair)
    
    if type(history) is not list:
        raise Exception("The response is a %r, not a list." % type(history))
        
    result = []
    for h in history:
        h["pair"] = pair
        t = Trade(**h)
        result.append(t)
    return result
    
    
