btce-api
========

This library provides a wrapper (hopefully a convenient one) around the public
and trading APIs of the BTC-e.com exchange site.  So that you don't have to 
spend your time chasing down wacky dependencies, it depends only on the
following standard libraries that are "batteries included" with a Python 2.7
installation: 

    datetime, hashlib, hmac, HTMLParser, httplib, json, urllib, warnings

Some of the samples use matplotlib and NumPy, and the tests use unittest
(although I find it easier to run them with nose), but these are not used 
in the library itself.

NOTE: BTC-e is not affiliated with this project; this is a completely independent 
implementation based on the API description.  Use at your own risk.

If you find the library useful and would like to donate (and many thanks to 
those that have donated!), please send some coins here:

    LTC LatrKXtfw66LQUURrxBzCE7cxFc9Sv8FWf
    BTC 16vnh6gwFYLGneBa8JUk7NaXpEt3Qojqs1

The following functions in the btceapi module access the public API and/or 
scrape content from the main page, and do not require any user account 
information:

    getDepth(pair) - Retrieve the depth for the given pair.  Returns a tuple 
    (asks, bids); each of these is a list of (price, volume) tuples.  See the
    example usage in samples/show_depth.py.

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

The TradeAPI class in the btceapi module accesses the trading API, and requires
the key and secret values (found under "API Keys" on the Profile page).  The 
constructor also takes an optional third argument (default value of 1) which 
specifies the starting nonce; this is an integer value that is incremented
on each subsequent API call.  While the TradeAPI object will take care of 
incrementing this number during its lifetime, it is the user's responsibility 
to remember this number (retrieved by the next_nonce method) before destroying 
the TradeAPI object, and to provide it to the next TradeAPI instance that uses 
the same key/secret.

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

    orderList - Retrieves a list of orders via the server OrderList method, and
    returns a list of OrderItem objects, which have the following members: 
    pair (such as "btc_usd"), type ("buy" or "sell"), amount, rate, 
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
