from basic_compiler.position import Position
from basic_compiler.tokens import Token, token_types
from basic_compiler.errors import IllegalCharError
from basic_compiler.constants import DIGITS
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