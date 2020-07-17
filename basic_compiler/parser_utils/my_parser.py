from basic_compiler.tokens import token_types, Token
from basic_compiler.parser_utils import nodes
from basic_compiler.errors import InvalidSynatxError


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error:
                self.error = res.error
            return res.node
        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self

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
        self.current_token = self.tokens[self.token_index] if self.token_index < len(
            self.tokens) else None

    def parse(self):
        res = self.expr()
        if not res.error and self.current_token.type != token_types['EOF']:
            return res.failure(InvalidSynatxError(
                self.current_token.pos_start, self.current_token.pos_end, 
                "Expected '+', '-', '*' or '/' "
            ))
        return res 

    ################################
    # implmentation of grammar rules
    ################################

    def factor(self):
        res = ParseResult()

        tok = self.current_token

        if tok.type in (token_types['int'], token_types['float']):
            res.register(self.advance())
            return res.success(nodes.NumberNode(tok))
        return res.failure(InvalidSynatxError(tok.pos_start, tok.pos_end, 'Expected int or float'))

    def bin_op(self, func, token_match):
        res = ParseResult()
        left = res.register(func())
        if res.error:
            return res
        while self.current_token and self.current_token.type in token_match:
            op_token = self.current_token
            res.register(self.advance())
            right = res.register(func())
            if res.error:
                return res
            left = nodes.BinaryOperationNode(op_token, left, right)
        return res.success(left)

    def term(self):
        return self.bin_op(self.factor, [token_types['*'], token_types['/']])

    def expr(self):
        return self.bin_op(self.term, [token_types['+'], token_types['-']])
