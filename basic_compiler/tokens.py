
####################################
# TOKENS
####################################

token_types = {
    '+': {'TT_PLUS': 'PLUS'},
    'TT_FLOAT': 'FLOAT',
    'TT_INT': 'INT',
    '*': {'TT_MUL': 'MUL'},
    '-': {'TT_MINUS': 'MINUS'},
    '/': {'TT_DIV': 'DIV'},
    '(': {'TT_LPAREN': 'LPAREN'},
    ')': {'TT_RPAREN': 'RPAREN'}
}

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        return f'{self.type}' + f':{self.value}' if self.value else ''