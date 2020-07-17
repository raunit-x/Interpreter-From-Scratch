from basic_compiler.errors import Error, IllegalCharError
from basic_compiler.position import Position
from basic_compiler.lexer import Lexer
from basic_compiler.parser_utils.my_parser import Parser

#######################
# RUN
#######################

def run(fn, text):
    # Generate Tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    print(tokens)
    if error:
        return None, error
    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    return ast, error
