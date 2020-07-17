from basic_compiler.errors import Error, IllegalCharError
from basic_compiler.position import Position
from basic_compiler.lexer import Lexer


#######################
# RUN
#######################

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    return tokens, error
