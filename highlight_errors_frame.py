import tkinter as tk
import scrolled_frame

class HighlightErrorsFrame:
    def __init__(self, parent, padx_ = 10, pady_ = 10):

        # create frame to hold visualization
        self.highlight_errors_frame = scrolled_frame.ScrolledFrame(parent, False)
        self.highlight_errors_frame.grid(column = 0, row = 5, sticky = 'EW', padx = padx_, pady = pady_)

