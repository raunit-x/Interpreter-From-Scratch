####################################
# CONSTANTS
####################################
DIGITS = '0123456789'
VALID_CHARS = '_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

####################################
# ERRORS
####################################
class Error:
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details
    
    def __repr__(self):
        return f'{self.error_name}:{self.details}'

class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__('Illegal Character', details)

        

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


####################################
# LEXER
####################################

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
    
    def make_number(self):
        period_count = 0
        num_str = ''
        while self.current_char and self.current_char in DIGITS + '.':                    
            if self.current_char == '.':
                if period_count:
                    break
                period_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
        if not period_count:
            return Token(token_types['TT_INT'], int(num_str))
        return Token(token_types['TT_FLOAT'], float(num_str))


    def make_tokens(self):
        tokens = []
        while self.current_char:
            if self.current_char in [' ', '\t']:
                self.advance()
            elif self.current_char in token_types:
                tokens.append(list(token_types[self.current_char].values())[0])
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            else:
                return [], IllegalCharError(f"'{self.current_char}' in line '{self.text}'")
        return tokens, None



#######################
# RUN
#######################

def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()
    return tokens, error
