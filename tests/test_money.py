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

    # ===== 补充：覆盖 add/sub/mul/div/cmp/max/min 的 int/float 分支与 TypeError 分支 =====

    def test_add_int(self):
        m = Money(100)
        result = m.add(50)
        assert result.value == Decimal('150.0000')

    def test_add_float(self):
        m = Money(100)
        result = m.add(50.5)
        assert result.value == Decimal('150.5000')

    def test_add_invalid_type(self):
        m = Money(100)
        with pytest.raises(TypeError):
            m.add("100")

    def test_sub_int(self):
        m = Money(100)
        result = m.sub(30)
        assert result.value == Decimal('70.0000')

    def test_sub_float(self):
        m = Money(100)
        result = m.sub(25.5)
        assert result.value == Decimal('74.5000')

    def test_sub_invalid_type(self):
        m = Money(100)
        with pytest.raises(TypeError):
            m.sub("50")

    def test_mul_int(self):
        m = Money(100)
        result = m.mul(2)
        assert result.value == Decimal('200.0000')

    def test_mul_decimal(self):
        m = Money(100)
        result = m.mul(Decimal('0.5'))
        assert result.value == Decimal('50.0000')

    def test_mul_invalid_type(self):
        m = Money(100)
        with pytest.raises(TypeError):
            m.mul("0.5")

    def test_div_float(self):
        m = Money(100)
        result = m.div(2.5)
        assert result.value == Decimal('40.0000')

    def test_div_decimal(self):
        m = Money(100)
        result = m.div(Decimal('4'))
        assert result.value == Decimal('25.0000')

    def test_div_invalid_type(self):
        m = Money(100)
        with pytest.raises(TypeError):
            m.div("2")

    def test_cmp_int(self):
        m = Money(100)
        assert m.cmp(50) == 1
        assert m.cmp(100) == 0
        assert m.cmp(150) == -1

    def test_cmp_float(self):
        m = Money(100.5)
        assert m.cmp(100.0) == 1
        assert m.cmp(100.5) == 0

    def test_cmp_invalid_type(self):
        m = Money(100)
        with pytest.raises(TypeError):
            m.cmp("100")

    def test_max_int(self):
        m = Money(100)
        assert m.max(150).value == Decimal('150.0000')
        assert m.max(50).value == Decimal('100.0000')

    def test_max_float(self):
        m = Money(100)
        assert m.max(150.5).value == Decimal('150.5000')

    def test_max_invalid_type(self):
        m = Money(100)
        with pytest.raises(TypeError):
            m.max("100")

    def test_min_int(self):
        m = Money(100)
        assert m.min(150).value == Decimal('100.0000')
        assert m.min(50).value == Decimal('50.0000')

    def test_min_float(self):
        m = Money(100)
        assert m.min(50.5).value == Decimal('50.5000')

    def test_min_invalid_type(self):
        m = Money(100)
        with pytest.raises(TypeError):
            m.min("100")

    def test_max_min_with_int_float(self):
        m1 = Money(100)
        assert m1.max(50).value == Decimal('100.0000')
        assert m1.min(50.5).value == Decimal('50.5000')

    def test_compare_with_int_float(self):
        m = Money(100)
        # __lt__/__gt__/__le__/__ge__ 通过 cmp 走 int/float 分支
        assert (m > 50) is True
        assert (m < 150) is True
        assert (m >= 100) is True
        assert (m <= 100) is True