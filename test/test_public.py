import unittest

import btceapi


class TestPublic(unittest.TestCase):
    def test_getTicker(self):
        connection = btceapi.BTCEConnection()
        info = btceapi.APIInfo(connection)
        for pair in info.pair_names:
            btceapi.getTicker(pair, connection, info)
            btceapi.getTicker(pair, connection)
            btceapi.getTicker(pair, info=info)
            btceapi.getTicker(pair)

    def test_getHistory(self):
        connection = btceapi.BTCEConnection()
        info = btceapi.APIInfo(connection)
        for pair in info.pair_names:
            btceapi.getTradeHistory(pair, connection, info)
            btceapi.getTradeHistory(pair, connection)
            btceapi.getTradeHistory(pair, info=info)
            btceapi.getTradeHistory(pair)

    def test_getDepth(self):
        connection = btceapi.BTCEConnection()
        info = btceapi.APIInfo(connection)
        for pair in info.pair_names:
            btceapi.getDepth(pair, connection, info)
            btceapi.getDepth(pair, connection)
            btceapi.getDepth(pair, info=info)
            btceapi.getDepth(pair)


if __name__ == '__main__':
    unittest.main()
