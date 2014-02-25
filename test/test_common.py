import decimal
import random
import unittest
from btceapi.common import *


class TestCommon(unittest.TestCase):
    def test_formatCurrency(self):
        self.assertEqual(formatCurrencyDigits(1.123456789, 1), "1.1")
        self.assertEqual(formatCurrencyDigits(1.123456789, 2), "1.12")
        self.assertEqual(formatCurrencyDigits(1.123456789, 3), "1.123")
        self.assertEqual(formatCurrencyDigits(1.123456789, 4), "1.1234")
        self.assertEqual(formatCurrencyDigits(1.123456789, 5), "1.12345")
        self.assertEqual(formatCurrencyDigits(1.123456789, 6), "1.123456")
        self.assertEqual(formatCurrencyDigits(1.123456789, 7), "1.1234567")

        for i in range(2, 8):
            print i
            self.assertEqual(formatCurrencyDigits(1.12, i), "1.12")
            self.assertEqual(formatCurrencyDigits(44.0, i), "44.0")

    def test_formatCurrencyByPair(self):
        for p, d in max_digits.items():
            self.assertEqual(formatCurrency(1.12, p),
                             formatCurrencyDigits(1.12, d))
            self.assertEqual(formatCurrency(44.0, p),
                             formatCurrencyDigits(44.0, d))
            self.assertEqual(truncateAmount(1.12, p),
                             truncateAmountDigits(1.12, d))
            self.assertEqual(truncateAmount(44.0, p),
                             truncateAmountDigits(44.0, d))

    def test_truncateAmount(self):
        for p, d in max_digits.items():
            self.assertEqual(truncateAmount(1.12, p),
                             truncateAmountDigits(1.12, d))
            self.assertEqual(truncateAmount(44.0, p),
                             truncateAmountDigits(44.0, d))

    def test_validatePair(self):
        for pair in all_pairs:
            validatePair(pair)
        self.assertRaises(InvalidTradePairException,
                          validatePair, "not_a_real_pair")

    def test_validateOrder(self):
        for pair in all_pairs:
            t = random.choice(("buy", "sell"))
            a = random.random()
            if pair[4] == "btc":
                validateOrder(pair, t, a, decimal.Decimal("0.01"))
            else:
                validateOrder(pair, t, a, decimal.Decimal("0.1"))

            t = random.choice(("buy", "sell"))
            a = decimal.Decimal(str(random.random()))
            if pair[:4] == "btc_":
                self.assertRaises(InvalidTradeAmountException,
                                  validateOrder, pair, t, a,
                                  decimal.Decimal("0.009999"))
            else:
                self.assertRaises(InvalidTradeAmountException,
                                  validateOrder, pair, t, a,
                                  decimal.Decimal("0.09999"))

        self.assertRaises(InvalidTradePairException,
                          validateOrder, "foo_bar", "buy",
                          decimal.Decimal("1.0"), decimal.Decimal("1.0"))
        self.assertRaises(InvalidTradeTypeException,
                          validateOrder, "btc_usd", "foo",
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
        self.assertEqual(set(max_digits.keys()), set(min_orders.keys()))
        self.assertEqual(set(max_digits.keys()), set(all_pairs))

    def test_currency_sets(self):
        currencies_from_pairs = set()
        for p in all_pairs:
            c1, c2 = p.split("_")
            currencies_from_pairs.add(c1)
            currencies_from_pairs.add(c2)

        self.assertEqual(currencies_from_pairs, set(all_currencies))

if __name__ == '__main__':
    unittest.main()
