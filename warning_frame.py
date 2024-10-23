import tkinter as tk
import scrolled_frame

""" Place where warnings are shown """
class WarningFrame:
    def __init__(self, main_window, padx = 10, pady = 10):
        self.warning_frame = scrolled_frame.ScrolledFrame(main_window, True)
        self.warning_frame.grid(column = 0, row = 4, sticky = 'EW', padx = padx, pady = pady)




            