from basic_interpreter.errors import RunTimeError

def fast_exponentiation(a, b):
    if b < 0:
        return 1 / fast_exponentiation(a, -b)
    if not b:
        return 1 if a else 0
    res = fast_exponentiation(a, b // 2) 
    return (res * res) * a if b % 1 else res * res

class Value:
    def __init__(self):
        self.set_position()
        self.set_context()
    
    def set_position(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    
    def set_context(self, context=None):
        self.context = context
        return self
    
    def added_to(self, other):
        return None, self.illegal_operation()
    
    def subtracted_by(self, other):
        return None, self.illegal_operation()
        
    def multiplied_by(self, other):
        return None, self.illegal_operation()
    
    def divided_by(self, other):
        return None, self.illegal_operation()
    
    def exponentiation_by(self, other):
        return None, self.illegal_operation()
    
    def set_context(self, context=None):
        return None, self.illegal_operation()
    
    def get_comparison_eq(self, other):
        return None, self.illegal_operation()
    
    def get_comparison_lt(self, other):
        return None, self.illegal_operation()

    def get_comparison_lte(self, other):
        return None, self.illegal_operation()
    
    def get_comparison_gt(self, other):
        return None, self.illegal_operation()

    def get_comparison_gte(self, other):
        return None, self.illegal_operation()
        
    def get_comparison_ne(self, other):
        return None, self.illegal_operation()
    
    def anded_by(self, other):
        return None, self.illegal_operation()

    def ored_by(self, other):
        return None, self.illegal_operation()
    
    def notted(self):
        return None, self.illegal_operation()
    
    def is_true(self):
        return False

    def execute(self, args):
        return None, self.illegal_operation()

    def copy(self):
        raise Exception('No copy method defined!')

    def illegal_operation(self, other=None):
        if not other:
            other = self
        return RunTimeError(
            self.pos_start, 
            other.pos_end, 
            'Illegal Operation',
            self.context
        )
    

class Number(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value
    
    def set_position(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    
    def set_context(self, context=None):
        self.context = context
        return self
    
    def __repr__(self):
        return f'{self.value}'
        
    def copy(self):
        copy = Number(self.value)
        copy.set_position(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(other.value + self.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(other)
    
    def subtracted_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(other)
        
    def multiplied_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(other)
    
    def divided_by(self, other):
        if isinstance(other, Number):
            if other.value:
                return Number(self.value / other.value).set_context(self.context), None
            else: 
                return None, RunTimeError(other.pos_start, other.pos_end, 'Division by Zero', self.context)
        else:
            return None, Value.illegal_operation(other)
    
    def exponentiation_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(other)
    
    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(other)
    
    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(other)

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(other)
    
    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(other)

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(other)
        
    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(other)
    
    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(other)
    
    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(other)
    
    def notted(self):
        return Number(int(1 if not self.value else 0)).set_context(self.context), None
    
    def is_true(self):
        return self.value