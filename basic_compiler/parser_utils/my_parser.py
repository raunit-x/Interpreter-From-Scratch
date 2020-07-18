from basic_compiler.tokens import token_types, Token
from basic_compiler.parser_utils import nodes
from basic_compiler.errors import InvalidSynatxError


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    def register_advancement(self):
        self.advance_count += 1
    
    def register(self, res):
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or not self.advance_count:
            self.error = error
        return self

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
 
    # implmentation of grammar rules
    def atom(self):
        res = ParseResult()
        tok = self.current_token

        if tok.type in (token_types['int'], token_types['float']):
            res.register_advancement()
            self.advance()
            return res.success(nodes.NumberNode(tok))
        elif tok.type == token_types['identifier']:
            res.register_advancement()
            self.advance()
            return res.success(nodes.VarAccessNode(tok))
        elif tok.type == token_types['(']:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_token.type == token_types[')']:
                res.register_advancement()
                self.advance()
                if res.error:
                    return res
                return res.success(expr)
            else:
                res.failure(InvalidSynatxError(
                    self.current_token.pos_start, self.current_token.pos_end, "Expected ')'"))
        return res.failure(
            InvalidSynatxError(self.current_token.pos_start, self.current_token.pos_end, 
            "Expected float, identifier, int, '-', '+' or '('"
        ))
    
    def power(self):
        return self.bin_op(self.atom, [token_types['^']], self.factor)

    def factor(self):
        res = ParseResult()
        tok = self.current_token
        if tok.type in (token_types['+'], token_types['-']):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(nodes.UnaryOperationNode(tok, factor))
        return self.power()

    def bin_op(self, func_left, token_match, func_right):
        res = ParseResult()
        left = res.register(func_left())
        if res.error:
            return res
        while self.current_token and self.current_token.type in token_match:
            op_token = self.current_token
            res.register_advancement()
            self.advance()
            right = res.register(func_right())
            if res.error:
                return res
            left = nodes.BinaryOperationNode(op_token, left, right)
        return res.success(left)

    def term(self):
        return self.bin_op(self.factor, [token_types['*'], token_types['/']], self.factor)

    def expr(self):
        res = ParseResult()
        if self.current_token.matches(token_types['keyword'], 'var'):
            res.register_advancement()
            self.advance()
            if self.current_token.type != token_types['identifier']:
                return res.failure(InvalidSynatxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Expected an identifier"
                ))
            var_name = self.current_token
            res.register_advancement()
            self.advance()
            if self.current_token.type != token_types['=']:
                return res.failure(InvalidSynatxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Expected an '='"
                ))
            res.register_advancement()
            self.advance()
            temp_expr = res.register(self.expr())
            if res.error:
                return res
            return res.success(nodes.VarAssignNode(var_name, temp_expr))
        
        node = res.register(self.bin_op(self.term, [token_types['+'], token_types['-']], self.term))
        if res.error:
            return res.failure(
            InvalidSynatxError(self.current_token.pos_start, self.current_token.pos_end, 
            "Expected float, identifier, int, 'var', '-', '+' or '('"
        ))
        return res.success(node)
