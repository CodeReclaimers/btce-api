# Copyright (c) 2013 Alan McIntyre

import httplib
import json
import decimal

decimal.getcontext().rounding = decimal.ROUND_DOWN
exps = [decimal.Decimal("1e-%d" % i) for i in range(16)]

btce_domain = "btc-e.com"

all_currencies = ("btc", "usd", "rur", "ltc", "nmc", "eur", "nvc", 
                  "trc", "ppc", "ftc", "cnc")  
all_pairs = ("btc_usd", "btc_rur", "btc_eur", "ltc_btc", "ltc_usd", 
             "ltc_rur", "nmc_btc", "usd_rur", "eur_usd", "nvc_btc", 
             "trc_btc", "ppc_btc", "ftc_btc", "cnc_btc")
             
max_digits = {"btc_usd":3,
              "btc_rur":4,
              "btc_eur":5,
              "ltc_btc":5, 
              "ltc_usd":6,
              "ltc_rur":5,
              "nmc_btc":5,
              "usd_rur":5,
              "eur_usd":5, 
              "nvc_btc":5,
              "trc_btc":5,
              "ppc_btc":5,
              "ftc_btc":5,
              "cnc_btc":5}
              
min_orders = {"btc_usd":decimal.Decimal("0.1"),
              "btc_rur":decimal.Decimal("0.1"),
              "btc_eur":decimal.Decimal("0.1"),
              "ltc_btc":decimal.Decimal("0.1"), 
              "ltc_usd":decimal.Decimal("0.1"),
              "ltc_rur":decimal.Decimal("0.1"),
              "nmc_btc":decimal.Decimal("0.1"),
              "usd_rur":decimal.Decimal("0.1"),
              "eur_usd":decimal.Decimal("0.1"), 
              "nvc_btc":decimal.Decimal("0.1"),
              "trc_btc":decimal.Decimal("0.1"),
              "ppc_btc":decimal.Decimal("0.1"),
              "ftc_btc":decimal.Decimal("0.1"),
              "cnc_btc":decimal.Decimal("0.1")}

def makeRequest(url, extra_headers = None, params = {}):
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    if extra_headers is not None:
        headers.update(extra_headers)
        
    conn = httplib.HTTPSConnection(btce_domain)
    conn.request("POST", url, params, headers)
    response = conn.getresponse().read()
    conn.close()    

    return response
              
def parseJSONResponse(response):
    def parse_decimal(var):
        return decimal.Decimal(var)

    try:
        r = json.loads(response, parse_float=parse_decimal,
                       parse_int=parse_decimal)
    except Exception as e:
        msg = "Error while attempting to parse JSON response: %s\nResponse:\n%r" % (e, response)
        raise Exception(msg)
    
    return r
                            
def makeJSONRequest(url, extra_headers = None, params = {}):
    response = makeRequest(url, extra_headers, params)
    return parseJSONResponse(response)

def validatePair(pair):
    if pair not in all_pairs:
        if "_" in pair:
            a, b = pair.split("_")
            swapped_pair = "%s_%s" % (b, a)
            if swapped_pair in all_pairs:
                msg = "Unrecognized pair: %r -- did you mean %s?" % (pair, swapped_pair)
                raise Exception(msg)
        raise Exception("Unrecognized pair: %r" % pair)

def truncateAmountDigits(value, digits):
    quantum = exps[digits]
    return decimal.Decimal(value).quantize(quantum)
        
def truncateAmount(value, pair):
    return truncateAmountDigits(value, max_digits[pair])

def formatCurrencyDigits(value, digits):
    s = str(truncateAmountDigits(value, digits))
    dot = s.index(".")
    while s[-1] == "0" and len(s) > dot + 2:
        s = s[:-1]
        
    return s

def formatCurrency(value, pair):
    return formatCurrencyDigits(value, max_digits[pair])

