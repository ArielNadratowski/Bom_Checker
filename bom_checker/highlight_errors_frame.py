import scrolled_frame

""" Shows the table that highlights where errors occur """
class HighlightErrorsFrame:
    def __init__(self, main_window, padx = 10, pady = 10):
        self.highlight_errors_frame = scrolled_frame.ScrolledFrame(main_window, False)
        self.highlight_errors_frame.grid(column = 0, row = 5, sticky = 'EW', padx = padx, pady = pady)

