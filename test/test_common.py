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

        for i in range(2,8):
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
        self.assertRaises(Exception, validatePair, "not_a_real_pair")
        
if __name__ == '__main__':
    unittest.main()        
