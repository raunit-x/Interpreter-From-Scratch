from basic_interpreter.number import Number
from basic_interpreter.parser_utils.nodes import NumberNode, BinaryOperationNode, UnaryOperationNode
from basic_interpreter.tokens import token_types
from basic_interpreter.errors import RunTimeError


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


class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None



class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None
    
    def get(self, name):
        value = self.symbols.get(name, None)
        if not value and self.parent:
            return self.parent.get(name)
        return value
    
    def set(self, name, value):
        self.symbols[name] = value
    
    def remove(self, name):
        del self.symbols[name]


class Interpreter:
    def visit(self, node, context) -> Number:
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)
    
    def no_visit_method(self, node, context) -> Number:
        raise Exception(f'No visit_{type(node).__name__} method defined')
    
    def visit_NumberNode(self, node: NumberNode, context) -> Number:
        return RTResult().success(
            Number(node.token.value).set_context(context).set_position(node.pos_start, node.pos_start)
        ) 

    def visit_BinaryOperationNode(self, node: BinaryOperationNode, context) -> Number:
        res = RTResult()
        left = res.register(self.visit(node.left, context))
        if res.error:
            return res
        right = res.register(self.visit(node.right, context))
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
        elif node.operator_token.type == token_types['^']:
            result, error = left.exponentiation_by(right)
        if error:
            return res.failure(error)
        return res.success(result.set_position(node.pos_start, node.pos_end))

    
    def visit_UnaryOperationNode(self, node, context) -> Number: 
        res = RTResult()        
        num = res.register(self.visit(node.node, context))
        if res.error:
            return res
        error = None
        if node.operator_token.type == token_types['-']:
            num, error = num.multiplied_by(Number(-1))
        if error:
            return res.failure(error) 
        return res.success(num.set_position(node.pos_start, node.pos_end))
    
    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_token.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(
                RunTimeError(node.pos_start, node.pos_start, 
                f"'{var_name}' is not defined",
                context
            ))
        return res.success(value)
    
    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_token.value
        value = res.register(self.visit(node.value_node, context))
        if res.error:
            return res
        context.symbol_table.set(var_name, value)
        return res.success(value)
