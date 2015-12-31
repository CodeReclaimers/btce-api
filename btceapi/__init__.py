# Copyright (c) 2013-2015 Alan McIntyre

from public import getDepth, getTicker, getTradeFee, getTradeHistory
from trade import TradeAPI
from scraping import scrapeMainPage
from keyhandler import AbstractKeyHandler, KeyHandler
from common import all_currencies, all_pairs, max_digits, min_orders, \
    formatCurrency, formatCurrencyDigits, \
    truncateAmount, truncateAmountDigits, \
    validatePair, validateOrder, \
    BTCEConnection

__version__ = "0.3.1"
