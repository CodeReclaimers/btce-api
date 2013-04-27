from btceapi.common import *

def test_formatCurrency():
    assert formatCurrency(1.123456789, 1) == "1.1"
    assert formatCurrency(1.123456789, 2) == "1.12"
    assert formatCurrency(1.123456789, 3) == "1.123"
    assert formatCurrency(1.123456789, 4) == "1.1234"
    assert formatCurrency(1.123456789, 5) == "1.12345"
    assert formatCurrency(1.123456789, 6) == "1.123456"
    assert formatCurrency(1.123456789, 7) == "1.1234567"
    assert formatCurrency(1.123456789, 8) == "1.12345678"
    
    for i in range(3,9):
        assert formatCurrency(1.12, i) == "1.12"
    