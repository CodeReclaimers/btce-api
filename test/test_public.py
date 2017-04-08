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

    def test_constructTrade(self):
        d = {"pair": "btc_usd",
             "trade_type": "bid",
             "price": decimal.Decimal("1.234"),
             "tid": 1,
             "amount": decimal.Decimal("3.2"),
             "date": 1368805684.878004}

        t = Trade(**d)
        self.assertEqual(t.pair, d.get("pair"))
        self.assertEqual(t.trade_type, d.get("trade_type"))
        self.assertEqual(t.price, d.get("price"))
        self.assertEqual(t.tid, d.get("tid"))
        self.assertEqual(t.amount, d.get("amount"))
        assert type(t.date) is datetime
        test_date = datetime.fromtimestamp(1368805684.878004)
        self.assertEqual(t.date, test_date)

        # check conversion of decimal dates
        d["date"] = decimal.Decimal("1368805684.878004")
        t = Trade(**d)
        assert type(t.date) is datetime
        self.assertEqual(t.date, test_date)

        # check conversion of integer dates
        d["date"] = 1368805684
        test_date = datetime.fromtimestamp(1368805684)
        t = Trade(**d)
        assert type(t.date) is datetime
        self.assertEqual(t.date, test_date)

        # check conversion of string dates with no fractional seconds
        d["date"] = "2013-05-17 08:48:04"
        t = Trade(**d)
        assert type(t.date) is datetime
        self.assertEqual(t.date, datetime(2013, 5, 17, 8, 48, 4, 0))

        # check conversion of string dates with fractional seconds
        d["date"] = "2013-05-17 08:48:04.878004"
        t = Trade(**d)
        assert type(t.date) is datetime
        self.assertEqual(t.date,
                         datetime(2013, 5, 17, 8, 48, 4, 878004))

        # check conversion of unicode dates with no fractional seconds
        d["date"] = u"2013-05-17 08:48:04"
        t = Trade(**d)
        assert type(t.date) is datetime
        self.assertEqual(t.date, datetime(2013, 5, 17, 8, 48, 4, 0))

        # check conversion of string dates with fractional seconds
        d["date"] = u"2013-05-17 08:48:04.878004"
        t = Trade(**d)
        assert type(t.date) is datetime
        self.assertEqual(t.date,
                         datetime(2013, 5, 17, 8, 48, 4, 878004))


if __name__ == '__main__':
    unittest.main()
