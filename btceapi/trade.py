import urllib
import hashlib
import hmac
from datetime import datetime

import common

class TradeAccountInfo:
    '''An instance of this class will be returned by 
    a successful call to TradeAPI.getInfo.'''
    
    def __init__(self, info):
        funds = info.get(u'funds')
        for c in common.all_currencies:
            setattr(self, "balance_%s" % c, funds.get(unicode(c), 0))
            
        self.open_orders = info.get(u'open_orders')
        self.server_time = datetime.fromtimestamp(info.get(u'server_time'))
        
        self.transaction_count = info.get(u'transaction_count')
        rights = info.get(u'rights')
        self.info_rights = (rights.get(u'info') == 1)
        self.withdraw_rights = (rights.get(u'withdraw') == 1)
        self.trade_rights = (rights.get(u'trade') == 1)   
            

class TransactionHistoryItem:
    '''A list of instances of this class will be returned by 
    a successful call to TradeAPI.transHistory.'''
    
    def __init__(self, transaction_id, info):
        self.transaction_id = transaction_id
        items = ("type", "amount", "currency", "desc",
                 "status", "timestamp")
        for n in items:
            setattr(self, n, info.get(n))
        self.timestamp = datetime.fromtimestamp(self.timestamp)

        
class TradeHistoryItem:
    '''A list of instances of this class will be returned by 
    a successful call to TradeAPI.tradeHistory.'''
    
    def __init__(self, transaction_id, info):
        self.transaction_id = transaction_id
        items = ("pair", "type", "amount", "rate", "order_id",
                 "is_your_order", "timestamp")
        for n in items:
            setattr(self, n, info.get(n))
        self.timestamp = datetime.fromtimestamp(self.timestamp)

        
class OrderItem:
    '''A list of instances of this class will be returned by 
    a successful call to TradeAPI.orderList.'''
    
    def __init__(self, order_id, info):
        self.order_id = order_id
        for n in ("pair", "type", "amount", "rate", "timestamp_created", "status"):
            setattr(self, n, info.get(n))
        self.timestamp_created = datetime.fromtimestamp(self.timestamp_created)

        
class TradeResult:
    '''An instance of this class will be returned by 
    a successful call to TradeAPI.trade.'''
    
    def __init__(self, info):
        self.received = info.get(u"received")
        self.remains = info.get(u"remains")
        self.order_id = info.get(u"order_id")
        funds = info.get(u'funds')
        for c in common.all_currencies:
            setattr(self, "balance_%s" % c, funds.get(unicode(c), 0))
            
   
class CancelOrderResult:
    '''An instance of this class will be returned by 
    a successful call to TradeAPI.cancelOrder.'''
    
    def __init__(self, info):
        self.order_id = info.get(u"order_id")
        funds = info.get(u'funds')
        for c in common.all_currencies:
            setattr(self, "balance_%s" % c, funds.get(unicode(c), 0))   
        
        
def setHistoryParams(params, from_number, count_number, from_id, end_id,
            order, since, end):
    if from_number is not None:
        params["from"] = "%d" % from_number
    if count_number is not None:
        params["count"] = "%d" % count_number
    if from_id is not None:
        params["from_id"] = "%d" % from_id
    if end_id is not None:
        params["end_id"] = "%d" % end_id 
    if order is not None:
        if order not in ("ASC", "DESC"):
            raise Exception("Unexpected order parameter: %r" % order)
        params["order"] = order
    if since is not None:
        params["since"] = "%d" % since
    if end is not None:
        params["end"] = "%d" % end
            
class TradeAPI:    
    def __init__(self, key, secret, nonce = 1):
        self.key = key
        self.secret = secret
        self.nonce = nonce
       
    def next_nonce(self):
        n = self.nonce
        self.nonce += 1
        return n
        
    def _post(self, params):
        params["nonce"] = self.next_nonce()
        encoded_params = urllib.urlencode(params)

        # Hash the params string to produce the Sign header value
        H = hmac.new(self.secret, digestmod=hashlib.sha512)
        H.update(encoded_params)
        sign = H.hexdigest()
        
        headers = {"Key":self.key, "Sign":sign}
        result = common.makeJSONRequest("/tapi", headers, encoded_params)
        
        success = result.get(u'success')
        if not success:
            if "method" in params:
                raise Exception("%s call failed with error: %s" \
                    % (params["method"], result.get(u'error')))
            
            raise Exception("Call failed with error: %s" % result.get(u'error'))
            
        if u'return' not in result:
            raise Exception("Response does not contain a 'return' item.")
            
        return result.get(u'return')        
        
    def getInfo(self):
        params = {"method":"getInfo"}
        return TradeAccountInfo(self._post(params))
        
    def transHistory(self, from_number = None, count_number = None,
                  from_id = None, end_id = None, order = None,
                  since = None, end = None):

        params = {"method":"TradeHistory"}
        
        setHistoryParams(params, from_number, count_number, from_id, end_id,
            order, since, end)
            
        orders = self._post(params)
        result = []
        for k, v in orders.items():
            result.append(TransactionHistoryItem(k, v))
            
        return result        
        
    def tradeHistory(self, from_number = None, count_number = None,
                  from_id = None, end_id = None, order = None,
                  since = None, end = None, pair = None):

        params = {"method":"TradeHistory"}
        
        setHistoryParams(params, from_number, count_number, from_id, end_id,
            order, since, end)

        if pair is not None:
            common.validatePair(pair)
            params["pair"] = pair

        orders = self._post(params)
        result = []
        for k, v in orders.items():
            result.append(TradeHistoryItem(k, v))
            
        return result
        
    def orderList(self, from_number = None, count_number = None,
                  from_id = None, end_id = None, order = None,
                  since = None, end = None, pair = None, active = None):

        params = {"method":"OrderList"}

        setHistoryParams(params, from_number, count_number, from_id, end_id,
            order, since, end)
        
        if pair is not None:
            common.validatePair(pair)
            params["pair"] = pair
        if active is not None:
            if active not in (0, 1, True, False):
                raise Exception("Unexpected active parameter: %r" % active)
            params["active"] = int(active)

        orders = self._post(params)
        result = []
        for k, v in orders.items():
            result.append(OrderItem(k, v))
            
        return result
           
    def trade(self, pair, trade_type, rate, amount):
        common.validatePair(pair)
        if trade_type not in ("buy", "sell"):
            raise Exception("Unrecognized trade type: %r" % trade_type)
       
        maxdigits = common.max_digits.get(pair)
        
        params = {"method":"Trade",
                  "pair":pair,
                  "type":trade_type,
                  "rate":common.formatCurrency(rate, maxdigits),
                  "amount":common.formatCurrency(amount, maxdigits)}
        
        return TradeResult(self._post(params))
        
    def cancelOrder(self, order_id):
        params = {"method":"CancelOrder", 
                  "order_id":order_id}
        return CancelOrderResult(self._post(params))
        
        
        
