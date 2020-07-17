from basic_compiler.tokens import token_types, Token
from basic_compiler.parser_utils import nodes
######################
# PARSER 
######################
class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.token_index = -1
        self.current_token = None
        self.advance()
    
    def advance(self):
        self.token_index += 1
        self.current_token = self.tokens[self.token_index] if self.token_index < len(self.tokens) else None
    
    def parse(self):
        res = self.expr()
        return res


    ################################
    # implmentation of grammar rules
    ################################

    def factor(self):
        tok = self.current_token
        if tok.type in (token_types['int'], token_types['float']):
            self.advance()
            return nodes.NumberNode(tok)
        return None

    def bin_op(self, func, token_match):
        left = func()
        while self.current_token and self.current_token.type in token_match:
            op_token = self.current_token
            self.advance()
            right = func()
            left = nodes.BinaryOperationNode(op_token, left, right)
        return left

    def term(self):
        return self.bin_op(self.factor, [token_types['*'], token_types['/']])
    
    def expr(self):
        return self.bin_op(self.term, [token_types['+'], token_types['-']])
