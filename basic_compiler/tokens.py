
####################################
# TOKENS
####################################

token_types = {
    '+': 'PLUS',
    'float': 'FLOAT',
    'int': 'INT',
    '*': 'MUL',
    '-': 'MINUS',
    '/': 'DIV',
    '(': 'LPAREN',
    ')': 'RPAREN',
    'EOF': 'EOF'
}

class Token:
    def __init__(self, type, value=None, pos_start=None, pos_end=None):
        self.type = type
        self.value = value
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()
            
        if pos_end:
            self.pos_end = pos_end.copy()
        

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'    
        return f'{self.type}'