from basic_compiler.errors import Error, IllegalCharError
from basic_compiler.position import Position
from basic_compiler.lexer import Lexer
from basic_compiler.parser_utils.my_parser import Parser
from basic_compiler.interpreter import Interpreter, Context, SymbolTable
from basic_compiler.number import Number

#######################
# RUN
#######################
global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number(0))

def run(fn, text):
    # Generate Tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    # print(f'Tokens: {tokens}')
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
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
