import tkinter as tk
from tableview import tableview

class HighlightErrorsFrame:
    def __init__(self, parent_window, position, compare_search_frame, padx_ = 10, pady_ = 10):

        # frame to hold visualization
        highlight_errors_frame = tk.LabelFrame(parent_window, text = 'Highlighted Errors')
        highlight_errors_frame.pack(side = position, fill = 'both', expand = True, padx = padx_, pady = pady_)

        # set up tableview
        self.set_up_table_view(compare_search_frame)

        # fill out table
        self.fill_table(compare_search_frame)

        # highlight stuff in table
        self.highlight_table_cells(compare_search_frame)

    def set_up_table_view(self, compare_search_frame):
        # set up table view 
        header_list = list(compare_search_frame.highlight_error_dataframe.columns)
        column_width = []
        for i in header_list:
            column_width.append(100)

        COLOR_MAP = {
            'header_background': 'grey70',
            'header_foreground': 'black',
            'tree_background': 'white',
            'tree_foreground': 'grey',
            'item_foreground': 'black',
            'tree_erase_background': 'white',
            'selected_row_bg_color': 'grey90',
            'selected_row_text_color': 'black',
            'separator_color':'grey'
            }
            
        tableview.setup_columns(root = self, 
                                window = self, 
                                column_headers = header_list, 
                                column_widths = column_width, 
                                table_height = 20, 
                                frame_height = 700, 
                                column_height = 200, 
                                header_height = 49, 
                                table_color_map = COLOR_MAP)
        tableview.pack()

    def fill_table(self, compare_search_frame):
        tableview.clear()

        number_rows = len(compare_search_frame.highlight_error_dataframe.index)
        for i in range(number_rows):
            column_number = 0
            row_as_list = compare_search_frame.highlight_error_dataframe.iloc[i].tolist()
            for item in row_as_list:
                tableview.insert_item(column_number, text = item)
                column_number += 1

    def highlight_table_cells(self, compare_search_frame):
        # wow I hate this entire for loop
        for error in compare_search_frame.highlight_error_list: # iterates down the list of highlight errors
            if error.warning == 'duplicate':
                row_indexes = compare_search_frame.highlight_error_dataframe[compare_search_frame.highlight_error_dataframe['split_ref_designators'] == error.reference_designator].index.tolist()
                for row_index in row_indexes: # because there are more than one index here because this is specifically duplicates, need to highlight both rows, but can only feed highlight_cell 1 row at a time
                    for column_index in range(len(list(compare_search_frame.highlight_error_dataframe.columns))): # also need to iterate through each column because highlight_cell also only takes 1 column at a time
                        tableview.highlight_cell(column = column_index + 1, row = row_index, bg = 'orange', fg = 'black') # column index gets +1 because tableview doesn't zero index this for some reason??
            elif error.warning == 'missing':
                row_index = compare_search_frame.highlight_error_dataframe[compare_search_frame.highlight_error_dataframe['split_ref_designators'] == error.reference_designator].index.tolist()
                for column_index in error.error_location: # also need to iterate through each column because highlight_cell also only takes 1 column at a time
                        tableview.highlight_cell(column = column_index + 1, row = row_index, bg = 'red', fg = 'black')
            else:
                row_index = compare_search_frame.highlight_error_dataframe[compare_search_frame.highlight_error_dataframe['split_ref_designators'] == error.reference_designator].index.tolist()
                for column_index in error.error_location: # also need to iterate through each column because highlight_cell also only takes 1 column at a time
                        tableview.highlight_cell(column = column_index + 1, row = row_index, bg = 'yellow', fg = 'black')
