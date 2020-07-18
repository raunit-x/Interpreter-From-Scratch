from basic_interpreter.position import Position
from basic_interpreter.tokens import Token, token_types
from basic_interpreter.errors import IllegalCharError, ExpectedCharError
from basic_interpreter.constants import DIGITS, LETTERS, LETTERS_DIGITS, KEYWORDS


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
        pos_start = self.pos.copy()
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
            return Token(token_types['int'], int(num_str), pos_start, self.pos)
        return Token(token_types['float'], float(num_str), pos_start, self.pos)
    
    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()
        while self.current_char  and self.current_char in LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()
        tok_type = token_types['keyword'] if id_str in KEYWORDS else token_types['identifier']
        return Token(tok_type, id_str, pos_start, self.pos.copy())
    
    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '=':
            self.advance()
            return Token(type=token_types['TT_NE'], pos_start=pos_start, pos_end=self.pos.copy()), None
        return [], ExpectedCharError(pos_start, self.pos.copy(), "Expected '=' after '!'")
    
    def make_equals(self):
        token_type = token_types['=']
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '=':
            self.advance()
            token_type = token_types['==']
        return Token(type=token_type, pos_start=pos_start, pos_end=self.pos.copy())

    def make_tokens(self):
        tokens = []
        while self.current_char:
            if self.current_char in [' ', '\t', '\n']:
                self.advance()
            elif self.current_char == '=':
                tokens.append(self.make_equals())
            elif self.current_char in token_types:
                tokens.append(Token(type=token_types[self.current_char], pos_start=self.pos))
                self.advance()
            elif self.current_char == '!':
                tok, error = self.make_not_equals()
                if error:
                    return [], error
                tokens.append(tok)
            elif self.current_char == '<':
                tokens.append(self.make_less_than())
            elif self.current_char == '>':
                tokens.append(self.make_greater_than())
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, f"'{char}'")
        tokens.append(Token(token_types['EOF'], pos_start=self.pos))
        return tokens, None