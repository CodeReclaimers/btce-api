import random
import unittest

from btceapi.common import *
from btceapi.public import APIInfo


class TestCommon(unittest.TestCase):
    def setUp(self):
        self.connection = BTCEConnection()

    def tearDown(self):
        self.connection.close()
        self.connection = None

    def test_formatCurrency(self):
        self.assertEqual(formatCurrencyDigits(1.123456789, 1), "1.1")
        self.assertEqual(formatCurrencyDigits(1.123456789, 2), "1.12")
        self.assertEqual(formatCurrencyDigits(1.123456789, 3), "1.123")
        self.assertEqual(formatCurrencyDigits(1.123456789, 4), "1.1234")
        self.assertEqual(formatCurrencyDigits(1.123456789, 5), "1.12345")
        self.assertEqual(formatCurrencyDigits(1.123456789, 6), "1.123456")
        self.assertEqual(formatCurrencyDigits(1.123456789, 7), "1.1234567")

        for i in range(2, 8):
            print(i)
            self.assertEqual(formatCurrencyDigits(1.12, i), "1.12")
            self.assertEqual(formatCurrencyDigits(44.0, i), "44.0")

    def test_formatCurrencyByPair(self):
        info = APIInfo(self.connection)
        for i in info.pairs.values():
            d = i.decimal_places
            self.assertEqual(i.format_currency(1.12),
                             formatCurrencyDigits(1.12, d))
            self.assertEqual(i.format_currency(44.0),
                             formatCurrencyDigits(44.0, d))
            self.assertEqual(i.truncate_amount(1.12),
                             truncateAmountDigits(1.12, d))
            self.assertEqual(i.truncate_amount(44.0),
                             truncateAmountDigits(44.0, d))

    def test_truncateAmount(self):
        info = APIInfo(self.connection)
        for i in info.pairs.values():
            d = i.decimal_places
            self.assertEqual(i.truncate_amount(1.12),
                             truncateAmountDigits(1.12, d))
            self.assertEqual(i.truncate_amount(44.0),
                             truncateAmountDigits(44.0, d))

    def test_validatePair(self):
        info = APIInfo(self.connection)
        for pair in info.pair_names:
            info.validate_pair(pair)
        self.assertRaises(InvalidTradePairException,
                          info.validate_pair, "not_a_real_pair")

    def test_validate_pair_suggest(self):
        info = APIInfo(self.connection)
        self.assertRaises(InvalidTradePairException,
                          info.validate_pair, "usd_btc")

    def test_validateOrder(self):
        info = APIInfo(self.connection)
        for pair in info.pair_names:
            t = random.choice(("buy", "sell"))
            a = random.random()
            if pair[4] == "btc":
                info.validate_order(pair, t, a, decimal.Decimal("0.001"))
            else:
                info.validate_order(pair, t, a, decimal.Decimal("0.1"))

            t = random.choice(("buy", "sell"))
            a = decimal.Decimal(str(random.random()))
            if pair[:4] == "btc_":
                self.assertRaises(InvalidTradeAmountException,
                                  info.validate_order, pair, t, a,
                                  decimal.Decimal("0.0009999"))
            else:
                self.assertRaises(InvalidTradeAmountException,
                                  info.validate_order, pair, t, a,
                                  decimal.Decimal("0.009999"))

        self.assertRaises(InvalidTradePairException,
                          info.validate_order, "foo_bar", "buy",
                          decimal.Decimal("1.0"), decimal.Decimal("1.0"))
        self.assertRaises(InvalidTradeTypeException,
                          info.validate_order, "btc_usd", "foo",
                          decimal.Decimal("1.0"), decimal.Decimal("1.0"))

    def test_parseJSONResponse(self):
        json1 = """
                {"asks":[[3.29551,0.5],[3.29584,5]],
                "bids":[[3.29518,15.51461],[3,27.5]]}
                """
        parsed = parseJSONResponse(json1)
        asks = parsed.get("asks")
        self.assertEqual(asks[0], [decimal.Decimal("3.29551"),
                                   decimal.Decimal("0.5")])
        self.assertEqual(asks[1], [decimal.Decimal("3.29584"),
                                   decimal.Decimal("5")])
        bids = parsed.get("bids")
        self.assertEqual(bids[0], [decimal.Decimal("3.29518"),
                                   decimal.Decimal("15.51461")])
        self.assertEqual(bids[1], [decimal.Decimal("3"),
                                   decimal.Decimal("27.5")])

    def test_pair_identity(self):
        info = APIInfo(self.connection)
        self.assertEqual(len(info.pair_names), len(set(info.pair_names)))
        self.assertEqual(set(info.pairs.keys()), set(info.pair_names))

    def test_currency_sets(self):
        currencies_from_pairs = set()
        info = APIInfo(self.connection)
        for pair in info.pair_names:
            c1, c2 = pair.split("_")
            currencies_from_pairs.add(c1)
            currencies_from_pairs.add(c2)

        self.assertEqual(len(info.currencies), len(set(info.currencies)))
        self.assertEqual(currencies_from_pairs, set(info.currencies))


if __name__ == '__main__':
    unittest.main()
