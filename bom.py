import tkinter as tk

""" BOM object that holds info about it """
class Bom:
    def __init__(self, main_window, sub_window, bom_dataframe, status):       
        self.name = sub_window.input_storage[0].input.get('1.0', 'end').strip()
        self.description = sub_window.input_storage[1].input.get('1.0', 'end').strip()
        self.quantity = sub_window.input_storage[2].input.get('1.0', 'end').strip()
        self.reference_designator = sub_window.input_storage[3].input.get('1.0', 'end').strip()
        self.manufacturer = sub_window.input_storage[4].input.get('1.0', 'end').strip()
        self.manufacturer_part_number = sub_window.input_storage[5].input.get('1.0', 'end').strip()
        self.header = sub_window.input_storage[6].input.get('1.0', 'end').strip()
        self.bom_dataframe = bom_dataframe
        self.bom_status = status
        self.selected = tk.IntVar(main_window, 0) # this is getting linked back to the main window bc the upload window goes away when you upload a bom

