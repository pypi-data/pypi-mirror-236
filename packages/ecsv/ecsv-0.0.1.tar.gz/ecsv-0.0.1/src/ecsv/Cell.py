class Cell:
    def __init__(self, data_frame, row, col):
        self.row = row
        self.col = col
        self.data_frame = data_frame
        self.content = self.data_frame.iloc[row,col]
        self.input_dict = {
            "Text": "type='text'",
            "Password": "type='password'",
            "Date": "type='date'",
            "File": "type=file",
            "Submit": "type='submit'",
            "Email": "type='email'"
        }
    
    def get_html(self):
        """Matches the input into the corresponding input dictionary

        Returns:
            String: HTML attribute
        """
        if self.content in self.input_dict.keys():
            return self.create_input()
        elif str(self.content) == 'nan':
            return ""
        else:
            return f"<label for='{self.content}' name='{self.content}'>{self.content}</label>"
    
    def create_input(self):
        """Gives the corresponding HTML input string

        Returns:
            String: HTML input
        """
        top = self.data_frame.iloc[self.row - 1,self.col]
        left = self.data_frame.iloc[self.row, self.col - 1]

        if left in self.input_dict.keys() or str(left) == 'nan':
            if top in self.input_dict.keys() or str(top) == 'nan':
                return f"<input {self.input_dict[self.content]}/>"
            else:
                return f"<input id='{top}' {self.input_dict[self.content]}/>"
        else:
            return f"<input id='{left}' {self.input_dict[self.content]}/>"