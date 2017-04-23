btce-api
========

[![Build Status](https://travis-ci.org/CodeReclaimers/btce-api.svg)](https://travis-ci.org/CodeReclaimers/btce-api)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/9d2bd596b16043119953f912c0a46d35/badge.svg)](https://www.quantifiedcode.com/app/project/9d2bd596b16043119953f912c0a46d35)
[![Coverage Status](https://coveralls.io/repos/github/CodeReclaimers/btce-api/badge.svg)](https://coveralls.io/github/CodeReclaimers/btce-api)

This library provides a wrapper (hopefully a convenient one) around the public
and trading APIs of the BTC-e.com exchange site.  So that you don't have to 
spend your time chasing down wacky dependencies, it depends only on the Python 
standard library.

NOTE: Some of the samples use matplotlib and NumPy, so you may need to install
additional packages to run all the samples. 

NOTE: BTC-e is not affiliated with this project; this is a completely 
independent implementation based on the API description.  Use at your own risk.

If you find the library useful and would like to donate (and many thanks to 
those that have donated!), please send some coins here:

    LTC LatrKXtfw66LQUURrxBzCE7cxFc9Sv8FWf
    BTC 16vnh6gwFYLGneBa8JUk7NaXpEt3Qojqs1
    DOGE D5jNqRjwxhDZT4hkG8yoGkseP576smjyNx

The following functions in the btceapi module access the public API and/or 
scrape content from the main page, and do not require any user account 
information:

    getDepth(pair) - Retrieve the depth for the given pair.  Returns a tuple 
    (asks, bids); each of these is a list of (price, volume) tuples.  See the
    example usage in samples/show_depth.py.

    getTicker(pair) - Retrieve the ticker information (high, low, avg, etc.)
    for the given pair.  Returns a Ticker instance, which has members high, low,
    avg, vol, vol_cur, last, buy, sell, updated, and server_time.

    getTradeFee(pair) - Retrieve the fee (in percent) associated with trades
    for a given pair.
    
    getTradeHistory(pair) - Retrieve the trade history for the given pair.  
    Returns a list of Trade instances.  Each Trade instance has members 
    trade_type (either "bid" or "ask"), price, tid (transaction ID?), amount, 
    and date (a datetime object).
    
    scrapeMainPage() - Collect information from the main page and return it in
    a ScraperResults object.  This object has members 'messages' (a list of 
    (message ID, user, time, text) tuples representing the chat messages 
    currently visible on the main page, 'bitInstantReserves' (an integer value
    representing the current BitInstant reserves), and 'aurumXchangeReserves'
    (an integer value representing the current AurumXchange reserves).
    
All of the functions above also take an optional 'connection' argument, which
should be an instance of BTCEConnection.  This will speed up multiple function
calls, as a new connection will not have to be created for every call.   

The TradeAPI class in the btceapi module accesses the trading API, and requires
a KeyHandler object.  The KeyHandler manages your API key and secret values 
(found under "API Keys" on the Profile page), stored in a text file. For 
instructions on creating this text file, please see step 9 here:

    https://github.com/alanmcintyre/btce-bot/wiki/Getting-started

The following methods are available on a TradeAPI instance:

    getInfo - Retrieves basic account information via the server getInfo 
    method, and returns a TradeAccountInfo object with the following members:
        balance_[currency] - Current available balance in the given currency.
        open_orders - Number of open orders.
        server_time - Server time in a datetime object.
        transaction_count - Number of transactions. (?)
        info_rights - True if the API key has info rights.
        withdraw_rights - True if the API key has withdrawal rights.
        trade_rights - True if the API key has trading rights.
        
    transHistory - Retrieves transaction history via the server TransHistory
    method, and returns a list of TransactionHistoryItem objects, which have
    the following members: type, amount, currency, desc, status, and timestamp
    (a datetime object).
    
    tradeHistory - Retrieves trading history via the server TradeHistory 
    method, and returns a list of TradeHistoryItem objects, which have the 
    following members: pair (such as "btc_usd"), type ("buy" or "sell"), 
    amount, rate, order_id, is_your_order, timestamp (a datetime object).

    activeOrders - Retrieves a list of orders via the server ActiveOrders 
    method, and returns a list of OrderItem objects, which have the following
    members:  pair (such as "btc_usd"), type ("buy" or "sell"), amount, rate, 
    timestamp_created (a datetime object) and status.

    trade - Place a trade order via the server Trade method, and return a 
    TradeResult object, which has the following members:
        received - Immediate proceeds from the order.
        remains - Portion of the order that remains unfilled.
        order_id 
        balance_[currency] - Current available balance in the given currency.
        
    cancelOrder - Cancel the specified order via the server CancelOrder method,
    and return a CancelOrderResult object, which has the following members:
        order_id 
        balance_[currency] - Current available balance in the given currency.
    
See the API documentation (https://btc-e.com/api/documentation) for more 
details on arguments to these methods.
