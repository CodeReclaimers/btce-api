# Copyright (c) 2013-2015 Alan McIntyre

import decimal
import httplib
import json
import re
import os


class InvalidTradePairException(Exception):
    """ Raised when an invalid pair is passed. """
    pass


class InvalidTradeTypeException(Exception):
    """ Raised when invalid trade type is passed. """
    pass


class InvalidTradeAmountException(Exception):
    """ Raised if trade amount is too much or too little. """
    pass


class APIResponseError(Exception):
    """ Raised if the API replies with an HTTP code
    not in the 2xx range. """
    pass


decimal.getcontext().rounding = decimal.ROUND_DOWN
quanta = [decimal.Decimal("1e-%d" % i) for i in range(16)]

btce_domain = "btc-e.com"


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
        self.conn = None
        self.cookie = None
        self._timeout = timeout
        self.setup_connection()

    def setup_connection(self):
        if "HTTPS_PROXY" in os.environ:
            match = re.search(r'http://([\w.]+):(\d+)', os.environ['HTTPS_PROXY'])
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
            response = self.conn.getresponse()
        except Exception:
            # reset connection so it doesn't stay in a weird state if we catch
            # the error in some other place
            self.conn.close()
            self.setup_connection()
            raise

        if response.status != 200:
            raise httplib.HTTPException
        else:
            return response.read()

    def makeJSONRequest(self, url, extra_headers=None, params=""):
        response = self.makeRequest(url, extra_headers, params)
        return parseJSONResponse(response)


def truncateAmountDigits(value, digits):
    quantum = quanta[int(digits)]
    if type(value) is float:
        value = str(value)
    if type(value) is str:
        value = decimal.Decimal(value)
    return value.quantize(quantum)


def formatCurrencyDigits(value, digits):
    s = str(truncateAmountDigits(value, digits))
    s = s.rstrip("0")
    if s[-1] == ".":
        s = "%s0" % s

    return s
