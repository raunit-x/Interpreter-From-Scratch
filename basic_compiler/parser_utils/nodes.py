######################
# NODES 
######################
class NumbnerNode:
    def __init__(self, token):
        self.token = token
    
    def __repr__(self):
        return f'{self.token}'
    
class BinaryOperationNode:
    def __init__(self, operator_token, left_node, right_node):
        self.left = left_node
        self.right = right_node
        self.operator_token = operator_token

    def __repr__(self):
        return f'({self.left}, {self.operator_token}, {self.right})'