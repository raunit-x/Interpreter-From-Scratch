class NumberNode:
    def __init__(self, token):
        self.token = token
        self.pos_start = token.pos_start
        self.pos_end = token.pos_end
    
    def __repr__(self):
        return f'{self.token}'
    
class BinaryOperationNode:
    def __init__(self, operator_token, left_node, right_node):
        self.left = left_node
        self.right = right_node
        self.operator_token = operator_token
        self.pos_start = self.left.pos_start
        self.pos_end = self.right.pos_end

    def __repr__(self):
        return f'({self.left}, {self.operator_token}, {self.right})'

class UnaryOperationNode:
    def __init__(self, operator_token, node):
        self.operator_token = operator_token
        self.node = node
        self.pos_start = operator_token.pos_start
        self.pos_end = self.node.pos_end


    def __repr__(self):
        return f'{self.operator_token}:{self.node}'

class VarAccessNode:
    def __init__(self, var_name_token):
        self.var_name_token = var_name_token
        self.pos_start = var_name_token.pos_start
        self.pos_end = var_name_token.pos_end

    def __repr__(self):
        return f'[{self.var_name_token}]'

class VarAssignNode:
    def __init__(self, var_name_token, value_node):
        self.var_name_token = var_name_token
        self.value_node = value_node
        self.pos_start = var_name_token.pos_start
        self.pos_end = self.value_node.pos_end
    
    def __repr__(self):
        return f'[{self.var_name_token}: {self.value_node}]'

class IFNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case
        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = else_case.pos_end if else_case else self.cases[-1][0].pos_end
    
class ForNode:
    def __init__(self, var_name_token, start_value_node, end_value_node, step_value_node, body_node):
        self.var_name_token = var_name_token
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node
        self.pos_start = self.var_name_token.pos_start
        self.pos_end = self.body_node.pos_end
    
class WhileNode:
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node
        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end
        