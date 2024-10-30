from bom_checker.scrolled_frame import ScrolledFrame

""" Place where warnings are shown """
class WarningFrame:
    def __init__(self, main_window, padx = 10, pady = 10):
        self.main_window = main_window
        
        self.warning_subframe = ScrolledFrame(main_window, True)
        self.warning_subframe.grid(column = 0, row = 4, sticky = 'EW', padx = padx, pady = pady)




            