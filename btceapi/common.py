# Copyright (c) 2013-2015 Alan McIntyre

import decimal
import httplib
import json
import re
import os


class InvalidTradePairException(Exception):
    """ Exception raised when an invalid pair is passed. """
    pass


class InvalidTradeTypeException(Exception):
    """ Exception raise when invalid trade type is passed. """
    pass


class InvalidTradeAmountException(Exception):
    """ Exception raised if trade amount is too much or too little. """
    pass


class APIResponseError(Exception):
    """ Exception raise if the API replies with an HTTP code
    not in the 2xx range. """
    pass


decimal.getcontext().rounding = decimal.ROUND_DOWN
quanta = [decimal.Decimal("1e-%d" % i) for i in range(16)]

btce_domain = "btc-e.com"

all_currencies = ("btc", "ltc", "nmc", "nvc", "ppc", "usd", "rur", "eur")
all_pairs = ("btc_usd", "btc_rur", "btc_eur",
             "ltc_btc", "ltc_usd", "ltc_rur", "ltc_eur",
             "nmc_btc", "nmc_usd",
             "nvc_btc", "nvc_usd",
             "usd_rur", "eur_usd", "eur_rur",
             "ppc_btc", "ppc_usd")

max_digits = {"btc_usd": 3,
              "btc_rur": 5,
              "btc_eur": 5,
              "ltc_btc": 5,
              "ltc_usd": 6,
              "ltc_rur": 5,
              "ltc_eur": 3,
              "nmc_btc": 5,
              "nmc_usd": 3,
              "nvc_btc": 5,
              "nvc_usd": 3,
              "usd_rur": 5,
              "eur_usd": 5,
              "eur_rur": 5,
              "ppc_btc": 5,
              "ppc_usd": 3}

min_orders = {"btc_usd": decimal.Decimal("0.01"),
              "btc_rur": decimal.Decimal("0.01"),
              "btc_eur": decimal.Decimal("0.01"),
              "ltc_btc": decimal.Decimal("0.1"),
              "ltc_usd": decimal.Decimal("0.1"),
              "ltc_rur": decimal.Decimal("0.1"),
              "ltc_eur": decimal.Decimal("0.1"),
              "nmc_btc": decimal.Decimal("0.1"),
              "nmc_usd": decimal.Decimal("0.1"),
              "nvc_btc": decimal.Decimal("0.1"),
              "nvc_usd": decimal.Decimal("0.1"),
              "usd_rur": decimal.Decimal("0.1"),
              "eur_usd": decimal.Decimal("0.1"),
              "eur_rur": decimal.Decimal("0.1"),
              "ppc_btc": decimal.Decimal("0.1"),
              "ppc_usd": decimal.Decimal("0.1")}


def parseJSONResponse(response):
    def parse_decimal(var):
        return decimal.Decimal(var)

    try:
        r = json.loads(response, parse_float=parse_decimal,
                       parse_int=parse_decimal)
    except Exception as e:
        msg = "Error while attempting to parse JSON response:" \
              " %s\nResponse:\n%r" % (e, response)
        raise Exception(msg)

    return r


HEADER_COOKIE_RE = re.compile(r'__cfduid=([a-f0-9]{46})')
BODY_COOKIE_RE = re.compile(r'document\.cookie="a=([a-f0-9]{32});path=/;";')


class BTCEConnection:
    def __init__(self, timeout=30):
        self._timeout = timeout
        self.setup_connection()

    def setup_connection(self):
        if ("HTTPS_PROXY" in os.environ):
          match = re.search(r'http://([\w.]+):(\d+)',os.environ['HTTPS_PROXY'])
          if match:
            self.conn = httplib.HTTPSConnection(match.group(1),
                                                port=match.group(2),
                                                timeout=self._timeout)
          self.conn.set_tunnel(btce_domain)
        else:
          self.conn = httplib.HTTPSConnection(btce_domain, timeout=self._timeout)
        self.cookie = None

    def close(self):
        self.conn.close()

    def getCookie(self):
        self.cookie = ""

        try:
            self.conn.request("GET", '/')
            response = self.conn.getresponse()
        except Exception:
            # reset connection so it doesn't stay in a weird state if we catch
            # the error in some other place
            self.conn.close()
            self.setup_connection()
            raise

        setCookieHeader = response.getheader("Set-Cookie")
        match = HEADER_COOKIE_RE.search(setCookieHeader)
        if match:
            self.cookie = "__cfduid=" + match.group(1)

        match = BODY_COOKIE_RE.search(response.read())
        if match:
            if self.cookie != "":
                self.cookie += '; '
            self.cookie += "a=" + match.group(1)

    def makeRequest(self, url, extra_headers=None, params="", with_cookie=False):
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        if extra_headers is not None:
            headers.update(extra_headers)

        if with_cookie:
            if self.cookie is None:
                self.getCookie()

            headers.update({"Cookie": self.cookie})

        try:
            self.conn.request("POST", url, params, headers)
            response = self.conn.getresponse().read()
        except Exception:
            # reset connection so it doesn't stay in a weird state if we catch
            # the error in some other place
            self.conn.close()
            self.setup_connection()
            raise

        return response

    def makeJSONRequest(self, url, extra_headers=None, params=""):
        response = self.makeRequest(url, extra_headers, params)
        return parseJSONResponse(response)


def validatePair(pair):
    if pair not in all_pairs:
        if "_" in pair:
            a, b = pair.split("_", 1)
            swapped_pair = "%s_%s" % (b, a)
            if swapped_pair in all_pairs:
                msg = "Unrecognized pair: %r (did you mean %s?)"
                msg = msg % (pair, swapped_pair)
                raise InvalidTradePairException(msg)
        raise InvalidTradePairException("Unrecognized pair: %r" % pair)


def validateOrder(pair, trade_type, rate, amount):
    validatePair(pair)
    if trade_type not in ("buy", "sell"):
        raise InvalidTradeTypeException("Unrecognized trade type: %r" % trade_type)

    minimum_amount = min_orders[pair]
    formatted_min_amount = formatCurrency(minimum_amount, pair)
    if amount < minimum_amount:
        msg = "Trade amount %r too small; should be >= %s" % \
              (amount, formatted_min_amount)
        raise InvalidTradeAmountException(msg)


def truncateAmountDigits(value, digits):
    quantum = quanta[int(digits)]
    if type(value) is float:
        value = str(value)
    if type(value) is str:
        value = decimal.Decimal(value)
    return value.quantize(quantum)


def truncateAmount(value, pair):
    return truncateAmountDigits(value, max_digits[pair])


def formatCurrencyDigits(value, digits):
    s = str(truncateAmountDigits(value, digits))
    s = s.rstrip("0")
    if s[-1] == ".":
        s = "%s0" % s

    return s


def formatCurrency(value, pair):
    return formatCurrencyDigits(value, max_digits[pair])
