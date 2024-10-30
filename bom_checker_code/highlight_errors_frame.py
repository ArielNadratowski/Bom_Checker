from bom_checker_code.scrolled_frame import ScrolledFrame

""" Shows the table that highlights where errors occur """
class HighlightErrorsFrame:
    def __init__(self, main_window, padx = 10, pady = 10):
        self.main_window = main_window
        self.highlight_errors_subframe = ScrolledFrame(self.main_window, False)
        self.highlight_errors_subframe.grid(column = 0, row = 5, sticky = 'EW', padx = padx, pady = pady)

