from basic_compiler.errors import RunTimeError
class Number:
    def __init__(self, value):
        self.value = value
        self.set_position()
    
    def __repr__(self):
        return f'{self.value}'
        
    def set_position(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(other.value + self.value), None
    
    def subtracted_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value), None
        
    def multiplied_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value), None
    
    def divided_by(self, other):
        if isinstance(other, Number):
            if other.value:
                return Number(self.value / other.value), None
            else: 
                return Number(None), RunTimeError(other.pos_start, other.pos_end, 'Division by Zero')
    