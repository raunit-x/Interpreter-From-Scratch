######################
# NODES 
######################
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
