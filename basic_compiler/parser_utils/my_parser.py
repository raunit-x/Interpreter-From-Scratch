######################
# PARSER 
######################
class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.token_index = -1
        self.advance()
    
    def advance(self):
        self.token_index += 1
        self.current_token = self.token[self.token_index] if self.token_index < len(self.tokens) else None
    
    def factor(self):
        # TODO: complete the function
        pass

    def term(self):
        # TODO: complete the function
        pass
    
    def expr(self):
        # TODO: complete the function
        pass
