import tkinter as tk
from tableview import tableview

class HighlightErrorsFrame:
    def __init__(self, parent_window, position, padx_ = 10, pady_ = 10):

        # create frame to hold visualization
        self.highlight_errors_frame = tk.LabelFrame(parent_window, text = 'Highlighted Errors')
        self.highlight_errors_frame.pack(side = position, fill = 'x', expand = False, padx = padx_, pady = pady_)

