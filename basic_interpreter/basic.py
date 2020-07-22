from basic_interpreter.errors import Error, IllegalCharError
from basic_interpreter.position import Position
from basic_interpreter.lexer import Lexer
from basic_interpreter.parser_utils.my_parser import Parser
from basic_interpreter.interpreter import Interpreter, Context, SymbolTable
from basic_interpreter.number import Number


global_symbol_table = SymbolTable()
global_symbol_table.set("NULL", Number.null)
global_symbol_table.set("TRUE", Number.false)
global_symbol_table.set("FALSE", Number.true)

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
    print(f'AST: {ast.node}')
    if ast.error:
        return None, ast.error
        
    # Run Program
    interpreter = Interpreter()
    context = Context(fn)
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
