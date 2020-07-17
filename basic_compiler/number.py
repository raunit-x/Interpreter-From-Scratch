from basic_compiler.errors import RunTimeError
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
    
    def set_context(self, context=None):
        self.context = context
        return self
