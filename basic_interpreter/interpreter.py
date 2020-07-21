from basic_interpreter.number import Number, Value
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

class Function(Value):
    def __init__(self, name, body_node, arg_names):
        super().__init__()
        self.name = name or 'anonymous'
        self.body_node = body_node
        self.arg_names = arg_names
    
    def __repr__(self):
        return f"<function {self.name}>"
    
    def set_context(self, context=None):
        self.context = context
        return self
    
    def set_position(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def execute(self, args):
        res = RTResult()
        interpreter = Interpreter()
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)

        if len(args) > len(self.arg_names):
            return res.failure(RunTimeError(
                self.pos_start,
                self.pos_end, 
                f"{len(args) - len(self.arg_names)} too many args passed into '{self.name}'",
                self.context
            ))
        
        if len(args) < len(self.arg_names):
            return res.failure(RunTimeError(
                self.pos_start,
                self.pos_end, 
                f"{len(self.arg_names) - len(args)} too few args passed into '{self.name}'",
                self.context
            ))
        for i, arg_val in enumerate(args):
             arg_name = self.arg_names[i]
             arg_val.set_context(new_context)
             new_context.symbol_table.set(arg_name, arg_val)
        value = res.register(interpreter.visit(self.body_node, new_context))
        if res.error:
            return res
        return res.success(value)
    
    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names)
        copy.set_context(self.context)
        copy.set_position(self.pos_start, self.pos_end)
        return copy


class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value
    
    def set_context(self, context=None):
        self.context = context
        return self
    
    def set_position(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    
    def added_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        return None, Value.illegal_operation(self, other)        

    def multiplied_by(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        return None, Value.illegal_operation(self, other)
    
    def is_true(self):
        return len(self.value)
    
    def copy(self):
        copy = String(self.value)
        copy.set_position(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f"'{self.value}'"


class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None



class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent
    
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
        elif node.operator_token.type == token_types['==']:
            result, error = left.get_comparison_eq(right)
        elif node.operator_token.type == token_types['<']:
            result, error = left.get_comparison_lt(right)
        elif node.operator_token.type == token_types['>']:
            result, error = left.get_comparison_gt(right)
        elif node.operator_token.type == token_types['<=']:
            result, error = left.get_comparison_lte(right)
        elif node.operator_token.type == token_types['>=']:
            result, error = left.get_comparison_gte(right)
        elif node.operator_token.type == token_types['TT_NE']:
            result, error = left.get_comparison_ne(right)
        elif node.operator_token.matches(token_types['keyword'], "AND"):
            result, error = left.anded_by(right)
        elif node.operator_token.matches(token_types['keyword'], "OR"):
            result, error = left.ored_by(right)
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
        elif node.operator_token.matches(token_types['keyword'], "NOT"):
            num, error = num.notted()
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
    
    def visit_IFNode(self, node, context):
        res = RTResult()

        for condition, expr in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.error:
                return res
            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.error:
                    return res
                return res.success(expr_value)
        if node.else_case:
            else_value = res.register(self.visit(node.else_case, context))
            if res.error:
                return res
            return res.success(else_value)
        return res.success(None)
    
    def visit_ForNode(self, node, context):
        res = RTResult()
        start_value = res.register(self.visit(node.start_value_node, context))
        if res.error:
            return res
        end_value = res.register(self.visit(node.end_value_node, context))
        if res.error:
            return res
        step_value = Number(1)
        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node, context))
            if res.error:
                return res
        i = start_value.value

        if step_value.value >= 0:
            condition = lambda: i < end_value.value
        else:
            condition = lambda: i > end_value.value
        
        while condition():
            context.symbol_table.set(node.var_name_token.value, Number(i))
            i += step_value.value
            res.register(self.visit(node.body_node, context))
            if res.error:
                return res
        return res.success(None)

    def visit_WhileNode(self, node, context):
        res = RTResult()
        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.error:
                return res
            if not condition.is_true():
                break
            res.register(self.visit(node.body_node, context))
            if res.error:
                return res
        return res.success(None)
    
    def visit_FuncDefNode(self, node, context):
        res = RTResult()
        func_name = node.var_name_token.value if node.var_name_token else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_tokens]
        func_value = Function(func_name, body_node, arg_names).set_context(context).set_position(node.pos_start, node.pos_end)
        if node.var_name_token:
            context.symbol_table.set(func_name, func_value)
        return res.success(func_value)
    
    def visit_CallNode(self, node, context):
        res = RTResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.error:
            return res
        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.error:
                return res
        return_value = res.register(value_to_call.execute(args))
        if res.error:
            return res
        return res.success(return_value)

    def visit_StringNode(self, node, context):
        res = RTResult()
        return res.success(String(node.token.value).set_context(context).set_position(node.pos_start, node.pos_end))
