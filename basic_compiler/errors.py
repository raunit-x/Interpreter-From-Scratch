####################################
# ERRORS
####################################
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    
    def __repr__(self):
        return f'{self.error_name}:{self.details}\nFile: {self.pos_start.file_name}, Line Number: {self.pos_start.line + 1}'

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)