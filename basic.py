####################################
# CONSTANTS
####################################
DIGITS = '0123456789'
VALID_CHARS = '_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

####################################
# ERRORS
####################################
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    
    def __repr__(self):
        return f'{self.error_name}:{self.details}\nFile: {self.pos_start.file_name}, Line Number: {self.pos_start.line + 1}'

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


####################################
# POSITION
####################################
class Position:
    def __init__(self, index, line, column, file_name=None, file_text=None):
        self.index = index
        self.line = line
        self.column = column
        self.file_name = file_name
        self.file_text = file_text
    
    def advance(self, current_char):
        self.index += 1
        self.column += 1
        if current_char == '\n':
            self.line += 1
            self.column = 0
        
    def copy(self):
        return Position(self.index, self.line, self.column, self.file_name, self.file_text)

    def __repr__(self):
        return f'{self.line}:{self.column}'
        
        

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
    def __init__(self, file_name, text):
        self.file_name = file_name
        self.text = text
        self.pos = Position(-1, 0, -1, self.file_name, self.text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None
    
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
            if self.current_char in [' ', '\t', '\n']:
                self.advance()
            elif self.current_char in token_types:
                tokens.append(list(token_types[self.current_char].values())[0])
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, f"'{char}'")
        return tokens, None



#######################
# RUN
#######################

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    return tokens, error
