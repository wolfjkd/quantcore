import pytest
from decimal import Decimal
from quantcore.money import Money


class TestMoney:
    def test_init_float(self):
        m = Money(100.50)
        assert m.value == Decimal('100.5000')
    
    def test_init_int(self):
        m = Money(100)
        assert m.value == Decimal('100.0000')
    
    def test_init_string(self):
        m = Money('100.50')
        assert m.value == Decimal('100.5000')
    
    def test_init_decimal(self):
        m = Money(Decimal('100.50'))
        assert m.value == Decimal('100.5000')
    
    def test_add(self):
        m1 = Money(100)
        m2 = Money(50)
        result = m1.add(m2)
        assert result.value == Decimal('150.0000')
    
    def test_sub(self):
        m1 = Money(100)
        m2 = Money(50)
        result = m1.sub(m2)
        assert result.value == Decimal('50.0000')
    
    def test_mul(self):
        m = Money(100)
        result = m.mul(0.5)
        assert result.value == Decimal('50.0000')
    
    def test_div(self):
        m = Money(100)
        result = m.div(2)
        assert result.value == Decimal('50.0000')
    
    def test_div_zero(self):
        m = Money(100)
        with pytest.raises(ValueError):
            m.div(0)
    
    def test_commission(self):
        m = Money(30000)
        result = m.commission(0.00025, 5.0)
        assert result.value == Decimal('7.5000')
    
    def test_commission_min(self):
        m = Money(1000)
        result = m.commission(0.00025, 5.0)
        assert result.value == Decimal('5.0000')
    
    def test_stamp_tax(self):
        m = Money(10000)
        result = m.stamp_tax(0.0005)
        assert result.value == Decimal('5.0000')
    
    def test_apply_slippage(self):
        m = Money(10000)
        result = m.apply_slippage(10)
        assert result.value == Decimal('10.0000')
    
    def test_compare(self):
        m1 = Money(100)
        m2 = Money(50)
        m3 = Money(100)
        assert m1 > m2
        assert m1 >= m3
        assert m1 == m3
        assert m2 < m1
        assert m2 <= m3
        assert m1 != m2
    
    def test_max_min(self):
        m1 = Money(100)
        m2 = Money(50)
        assert m1.max(m2).value == Decimal('100.0000')
        assert m1.min(m2).value == Decimal('50.0000')
    
    def test_abs(self):
        m = Money(-100)
        assert m.abs().value == Decimal('100.0000')
    
    def test_to_float(self):
        m = Money(100.50)
        assert m.to_float() == 100.5
    
    def test_to_int(self):
        m = Money(100.50)
        assert m.to_int() == 101
    
    def test_invalid_init(self):
        with pytest.raises(TypeError):
            Money([])