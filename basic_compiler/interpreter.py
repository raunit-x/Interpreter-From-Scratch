from basic_compiler.number import Number
from basic_compiler.parser_utils.nodes import NumberNode, BinaryOperationNode, UnaryOperationNode
from basic_compiler.tokens import token_types


########################
# Runtime Result
########################

class RTResult:
    def __init__(self):
        self.value = None
        self.error = None
    
    def __repr__(self):
        return f'{self.value}'
 
    def register(self, res):
        if res.error:
            self.error = res.error
        return res.value
    
    def success(self, value):
        self.value = value
        return self
    
    def failure(self, error):
        self.error = error
        return self



########################
# Context
########################


class Interpreter:
    def visit(self, node) -> Number:
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)
    
    def no_visit_method(self, node) -> Number:
        raise Exception(f'No visit_{type(node).__name__} method defined')
    
    def visit_NumberNode(self, node: NumberNode) -> Number:
        return RTResult().success(Number(node.token.value).set_position(node.pos_start, node.pos_start)) 

    def visit_BinaryOperationNode(self, node: BinaryOperationNode) -> Number:
        res = RTResult()
        left = res.register(self.visit(node.left))
        if res.error:
            return res
        right = res.register(self.visit(node.right))
        if res.error:
            return res
        if node.operator_token.type == token_types['+']:
            result, error = left.added_to(right)
        elif node.operator_token.type == token_types['-']:
            result, error = left.subtracted_by(right)
        elif node.operator_token.type == token_types['*']:
            result, error = left.multiplied_by(right)
        elif node.operator_token.type == token_types['/']:
            result, error = left.divided_by(right)
        if error:
            return res.failure(error)
        return res.success(result.set_position(node.pos_start, node.pos_end))

    
    def visit_UnaryOperationNode(self, node) -> Number: 
        res = RTResult()
        num = res.register(self.visit(node.node))
        if res.error:
            return res
        error = None
        if node.operator_token.type == token_types['-']:
            num, error = num.multiplied_by(Number(-1))
        if error:
            return res.failure(error) 
        return res.success(num.set_position(node.pos_start, node.pos_end))