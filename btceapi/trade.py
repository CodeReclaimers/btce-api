# Copyright (c) 2013-2017 CodeReclaimers, LLC

# Trade API description: https://btc-e.com/api/documentation

from collections import namedtuple
import hashlib
import hmac
import warnings

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from . import keyhandler
from . import public


class InvalidNonceException(Exception):
    def __init__(self, method, expectedNonce, actualNonce):
        Exception.__init__(self)
        self.method = method
        self.expectedNonce = expectedNonce
        self.actualNonce = actualNonce

    def __str__(self):
        return "Expected a nonce greater than %d" % self.expectedNonce


class InvalidSortOrderException(Exception):
    """ Exception thrown when an invalid sort order is passed """
    pass


class TradeAccountInfo(object):
    """An instance of this class will be returned by
    a successful call to TradeAPI.getInfo."""

    def __init__(self, info):
        self.funds = info.get(u'funds')
        self.open_orders = info.get(u'open_orders')
        self.server_time = info.get(u'server_time')
        self.transaction_count = info.get(u'transaction_count')
        rights = info.get(u'rights')
        self.info_rights = (rights.get(u'info') == 1)
        self.withdraw_rights = (rights.get(u'withdraw') == 1)
        self.trade_rights = (rights.get(u'trade') == 1)


TransactionHistoryItem = namedtuple("TransactionHistoryItem",
    ["transaction_id", "type", "amount", "currency", "desc", "status", "timestamp"])


TradeHistoryItem = namedtuple("TradeHistoryItem",
    ["transaction_id", "pair", "type", "amount", "rate", "order_id", "is_your_order", "timestamp"])


OrderItem = namedtuple("OrderItem",
    ["order_id", "pair", "type", "amount", "rate", "timestamp_created", "status"])


TradeResult = namedtuple("TradeResult",
    ["received", "remains", "order_id", "funds"])


CancelOrderResult = namedtuple("CancelOrderResult",
    ["order_id", "funds"])


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
            raise InvalidSortOrderException("Unexpected order parameter: %r" % order)
        params["order"] = order
    if since is not None:
        params["since"] = "%d" % since
    if end is not None:
        params["end"] = "%d" % end


class TradeAPI(object):
    def __init__(self, key, handler, connection):
        self.key = key
        self.handler = handler
        self.connection = connection
        self.apiInfo = public.APIInfo(self.connection)
        self.raiseIfInvalidNonce = True

        if not isinstance(self.handler, keyhandler.AbstractKeyHandler):
            raise TypeError("The handler argument must be a"
                            " keyhandler.AbstractKeyHandler, such as"
                            " keyhandler.KeyHandler")

        # We depend on the key handler for the secret
        self.secret = handler.getSecret(key)

    def _post(self, params, allowNonceRetry=False):
        params["nonce"] = self.handler.getNextNonce(self.key)
        encoded_params = urlencode(params)

        # Hash the params string to produce the Sign header value
        H = hmac.new(self.secret.encode('utf-8'), digestmod=hashlib.sha512)
        H.update(encoded_params.encode('utf-8'))
        sign = H.hexdigest()

        headers = {"Key": self.key, "Sign": sign}
        result = self.connection.makeJSONRequest("/tapi", headers, encoded_params)

        success = result.get(u'success')
        if not success:
            err_message = result.get(u'error')
            method = params.get("method", "[uknown method]")

            if "invalid nonce" in err_message:
                # If the nonce is out of sync, make one attempt to update to
                # the correct nonce.  This sometimes happens if a bot crashes
                # and the nonce file doesn't get saved, so it's reasonable to
                # attempt a correction.  If multiple threads/processes are
                # attempting to use the same key, this mechanism will
                # eventually fail and the InvalidNonce will be emitted so that
                # you'll end up here reading this comment. :)

                # The assumption is that the invalid nonce message looks like
                # "invalid nonce parameter; on key:4, you sent:3"
                s = err_message.split(",")
                expected = int(s[-2].split(":")[1].strip("'"))
                actual = int(s[-1].split(":")[1].strip("'"))
                if self.raiseIfInvalidNonce and not allowNonceRetry:
                    raise InvalidNonceException(method, expected, actual)

                warnings.warn("The nonce in the key file is out of date;"
                              " attempting to correct.")
                self.handler.setNextNonce(self.key, expected + 1000)
                return self._post(params, True)
            elif "no orders" in err_message and method == "ActiveOrders":
                # ActiveOrders returns failure if there are no orders;
                # intercept this and return an empty dict.
                return {}
            elif "no trades" in err_message and method == "TradeHistory":
                # TradeHistory returns failure if there are no trades;
                # intercept this and return an empty dict.
                return {}

            raise Exception("%s call failed with error: %s"
                            % (method, err_message))

        if u'return' not in result:
            raise Exception("Response does not contain a 'return' item.")

        return result.get(u'return')

    def getInfo(self):
        params = {"method": "getInfo"}
        return TradeAccountInfo(self._post(params))

    def transHistory(self, from_number=None, count_number=None,
                     from_id=None, end_id=None, order="DESC",
                     since=None, end=None):

        params = {"method": "TransHistory"}

        setHistoryParams(params, from_number, count_number, from_id, end_id,
                         order, since, end)

        orders = self._post(params)
        result = []
        for k, v in orders.items():
            result.append(TransactionHistoryItem(int(k), **v))

        # We have to sort items here because the API returns a dict
        if "ASC" == order:
            result.sort(key=lambda a: a.transaction_id, reverse=False)
        elif "DESC" == order:
            result.sort(key=lambda a: a.transaction_id, reverse=True)

        return result

    def tradeHistory(self, from_number=None, count_number=None,
                     from_id=None, end_id=None, order=None,
                     since=None, end=None, pair=None):

        params = {"method": "TradeHistory"}

        setHistoryParams(params, from_number, count_number, from_id, end_id,
                         order, since, end)

        if pair is not None:
            self.apiInfo.validate_pair(pair)
            params["pair"] = pair

        orders = list(self._post(params).items())
        orders.sort(reverse=order != "ASC")
        result = []
        for k, v in orders:
            result.append(TradeHistoryItem(int(k), **v))

        return result

    def activeOrders(self, pair=None):

        params = {"method": "ActiveOrders"}

        if pair is not None:
            pair_info = self.apiInfo.validate_pair(pair)
            params["pair"] = pair

        orders = self._post(params)
        result = []
        for k, v in orders.items():
            result.append(OrderItem(int(k), **v))

        return result

    def trade(self, pair, trade_type, rate, amount):
        pair_info = self.apiInfo.get_pair_info(pair)
        pair_info.validate_order(trade_type, rate, amount)
        params = {"method": "Trade",
                  "pair": pair,
                  "type": trade_type,
                  "rate": pair_info.format_currency(rate),
                  "amount": pair_info.format_currency(amount)}

        return TradeResult(**self._post(params))

    def cancelOrder(self, order_id):
        params = {"method": "CancelOrder",
                  "order_id": order_id}
        return CancelOrderResult(**self._post(params))
