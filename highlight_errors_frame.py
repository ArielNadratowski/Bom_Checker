import tkinter as tk
import scrolled_frame

""" Shows the table that highlights where errors occur """
class HighlightErrorsFrame:
    def __init__(self, parent, padx_ = 10, pady_ = 10):
        self.highlight_errors_frame = scrolled_frame.ScrolledFrame(parent, False)
        self.highlight_errors_frame.grid(column = 0, row = 5, sticky = 'EW', padx = padx_, pady = pady_)

