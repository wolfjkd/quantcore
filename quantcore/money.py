from decimal import Decimal, ROUND_HALF_UP


class Money:
    def __init__(self, value=0.0):
        if isinstance(value, Decimal):
            self.value = value
        elif isinstance(value, (int, float)):
            self.value = Decimal(str(value)).quantize(Decimal('0.0000'), rounding=ROUND_HALF_UP)
        elif isinstance(value, str):
            self.value = Decimal(value).quantize(Decimal('0.0000'), rounding=ROUND_HALF_UP)
        else:
            raise TypeError(f"Unsupported type: {type(value)}")
    
    def add(self, other):
        if isinstance(other, Money):
            result = self.value + other.value
        elif isinstance(other, (int, float)):
            result = self.value + Decimal(str(other))
        else:
            raise TypeError(f"Unsupported type: {type(other)}")
        return Money(result)
    
    def sub(self, other):
        if isinstance(other, Money):
            result = self.value - other.value
        elif isinstance(other, (int, float)):
            result = self.value - Decimal(str(other))
        else:
            raise TypeError(f"Unsupported type: {type(other)}")
        return Money(result)
    
    def mul(self, ratio):
        if isinstance(ratio, (int, float)):
            result = self.value * Decimal(str(ratio))
        elif isinstance(ratio, Decimal):
            result = self.value * ratio
        else:
            raise TypeError(f"Unsupported type: {type(ratio)}")
        return Money(result)
    
    def div(self, ratio):
        if ratio == 0:
            raise ValueError("Division by zero")
        if isinstance(ratio, (int, float)):
            result = self.value / Decimal(str(ratio))
        elif isinstance(ratio, Decimal):
            result = self.value / ratio
        else:
            raise TypeError(f"Unsupported type: {type(ratio)}")
        return Money(result)
    
    def cmp(self, other):
        if isinstance(other, Money):
            return self.value.compare(other.value)
        elif isinstance(other, (int, float)):
            return self.value.compare(Decimal(str(other)))
        else:
            raise TypeError(f"Unsupported type: {type(other)}")
    
    def max(self, other):
        if isinstance(other, Money):
            return Money(max(self.value, other.value))
        elif isinstance(other, (int, float)):
            return Money(max(self.value, Decimal(str(other))))
        else:
            raise TypeError(f"Unsupported type: {type(other)}")
    
    def min(self, other):
        if isinstance(other, Money):
            return Money(min(self.value, other.value))
        elif isinstance(other, (int, float)):
            return Money(min(self.value, Decimal(str(other))))
        else:
            raise TypeError(f"Unsupported type: {type(other)}")
    
    def abs(self):
        return Money(abs(self.value))
    
    def commission(self, rate=0.00025, min_commission=5.0):
        commission = self.value * Decimal(str(rate))
        if commission < Decimal(str(min_commission)):
            commission = Decimal(str(min_commission))
        return Money(commission)
    
    def stamp_tax(self, rate=0.0005):
        return Money(self.value * Decimal(str(rate)))
    
    def apply_slippage(self, bps=10):
        slippage = self.value * Decimal(str(bps)) / Decimal('10000')
        return Money(slippage)
    
    def to_float(self):
        return float(self.value)
    
    def to_int(self):
        return int(self.value.quantize(Decimal('0'), rounding=ROUND_HALF_UP))
    
    def __repr__(self):
        return f"Money({self.value})"
    
    def __str__(self):
        return str(self.value)
    
    def __eq__(self, other):
        if isinstance(other, Money):
            return self.value == other.value
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        return self.cmp(other) < 0
    
    def __le__(self, other):
        return self.cmp(other) <= 0
    
    def __gt__(self, other):
        return self.cmp(other) > 0
    
    def __ge__(self, other):
        return self.cmp(other) >= 0