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
        return f'{self.error_name}:{self.details}\nFile: {self.pos_start.file_name}, Line: {self.pos_start.line + 1}'

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

class InvalidSynatxError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Syntax', details)
    
class RunTimeError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, 'Runtime Error', details)
        self.context = context
    
    def __repr__(self):
        result = self.generate_traceback()
        return result
    
    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        context = self.context
        while context:
            result += f'{self.error_name}:{self.details}\nFile: {self.pos_start.file_name}, Line: {self.pos_start.line + 1} in {context.display_name}\n'
            pos = context.parent_entry_pos
            context = context.parent
        return f'Traceback (most recent call):\n{result}'
