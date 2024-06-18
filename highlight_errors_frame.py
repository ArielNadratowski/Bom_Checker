import tkinter as tk
from tableview import tableview

class HighlightErrorsFrame:
    def __init__(self, parent_window, position, padx_ = 10, pady_ = 10):

        # frame to hold visualization
        highlight_errors_frame = tk.LabelFrame(parent_window, text = 'Highlighted Errors')
        highlight_errors_frame.pack(side = position, fill = 'both', expand = True, padx = padx_, pady = pady_)

        # table view implementation to highlight mismatches and other potential errors (like duplicate reference designators)
        HEADER_List = ['Ref Dsg', 'Description_A', 'Quantity_A', 'Manufacturer_A', 'Manufacturer Part Number_A', 
                       'Description_B', 'Quantity_B', 'Manufacturer_B', 'Manufacturer Part Number_B', 
                       'Desc_match_ratio', 'MFG_match_ratio', 'MPN_match_ratio']
        COLUMN_WIDTH = [55, 85, 75, 100, 170, 85, 75, 100, 170, 110, 110, 110]
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
            
        tableview.setup_columns(root = highlight_errors_frame, 
                                window = highlight_errors_frame, 
                                column_headers = HEADER_List, 
                                column_widths = COLUMN_WIDTH, 
                                table_height = 20, 
                                frame_height = 700, 
                                column_height = 200, 
                                header_height = 49, 
                                table_color_map = COLOR_MAP)
        tableview.pack()