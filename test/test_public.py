import unittest

from btceapi.common import BTCEConnection
from btceapi.public import *


class TestPublic(unittest.TestCase):
    def test_getTicker(self):
        connection = BTCEConnection()
        info = APIInfo(connection)
        for pair in info.pair_names:
            getTicker(pair, connection, info)
            getTicker(pair, connection)
            getTicker(pair, info=info)
            getTicker(pair)

    def test_getHistory(self):
        connection = BTCEConnection()
        info = APIInfo(connection)
        for pair in info.pair_names:
            getTradeHistory(pair, connection, info)
            getTradeHistory(pair, connection)
            getTradeHistory(pair, info=info)
            getTradeHistory(pair)

    def test_getDepth(self):
        connection = BTCEConnection()
        info = APIInfo(connection)
        for pair in info.pair_names:
            getDepth(pair, connection, info)
            getDepth(pair, connection)
            getDepth(pair, info=info)
            getDepth(pair)


if __name__ == '__main__':
    unittest.main()
