from basic_compiler.errors import Error, IllegalCharError
from basic_compiler.position import Position
from basic_compiler.lexer import Lexer
from basic_compiler.parser_utils.my_parser import Parser
from basic_compiler.interpreter import Interpreter, Context

#######################
# RUN
#######################

def run(fn, text):
    # Generate Tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    print(f'Tokens: {tokens}')
    if error:
        return None, error
    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse() 
    if ast.error:
        return None, ast.error
    print(f'AST Tree: {ast.node}')
    # Run Program
    interpreter = Interpreter()
    context = Context(fn)
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
