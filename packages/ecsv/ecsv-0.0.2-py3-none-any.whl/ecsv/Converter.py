import pandas as pd
import sys
import os
sys.path.append(os.path.join('/', os.path.relpath('src', '/')))
from ecsv.Cell import Cell

class Converter:
    def __init__(self, file_path):
        self.file_path = file_path
        try:
            self.csv_as_data_frame = pd.read_csv(self.file_path)
        except pd.errors.EmptyDataError:
            print("Please provide a non-empty file.")
        else:
            self.num_of_rows = self.csv_as_data_frame.shape[0]
            self.num_of_cols = self.csv_as_data_frame.shape[1]
            self.title = self.csv_as_data_frame.keys()[0]

    def into_HTML_Form(self):
        """Convert the csv to a simple HTML form

        Returns:
            String: HTML form
        """
        table = "<table><form>"
        table += f"<tr><th>{self.title}</th></tr>"
        for row in range(self.num_of_rows):
            table += "<tr>"
            for col in range(self.num_of_cols):
                table += "<td>"
                table += Cell(self.csv_as_data_frame, row, col).get_html()
                table += "</td>"
            table += "</tr>"
        table += "</form></table>"
        return table