from basic_interpreter.errors import RunTimeError
def fast_exponentiation(a, b):
    if b < 0:
        return 1 / fast_exponentiation(a, -b)
    if not b:
        return 1 if a else 0
    res = fast_exponentiation(a, b // 2) 
    return (res * res) * a if b % 1 else res * res

class Number:
    def __init__(self, value):
        self.value = value
        self.set_position()
        self.set_context()
    
    def __repr__(self):
        return f'{self.value}'
        
    def set_position(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(other.value + self.value).set_context(self.context), None
    
    def subtracted_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        
    def multiplied_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
    
    def divided_by(self, other):
        if isinstance(other, Number):
            if other.value:
                return Number(self.value / other.value).set_context(self.context), None
            else: 
                return None, RunTimeError(other.pos_start, other.pos_end, 'Division by Zero', self.context)
    
    def exponentiation_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
    
    def set_context(self, context=None):
        self.context = context
        return self
    
    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None
    
    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None
    
    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None
        
    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None
    
    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None
    
    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None
    
    def notted(self):
        return Number(int(1 if not self.value else 0)).set_context(self.context), None