class Position:
    def __init__(self, index, line, column, file_name=None, file_text=None):
        self.index = index
        self.line = line
        self.column = column
        self.file_name = file_name
        self.file_text = file_text
    
    def advance(self, current_char=None) :
        self.index += 1
        self.column += 1
        if current_char == '\n':
            self.line += 1
            self.column = 0
        
    def copy(self):
        return Position(self.index, self.line, self.column, self.file_name, self.file_text)

    def __repr__(self):
        return f'{self.line}:{self.column}'