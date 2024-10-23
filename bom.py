import tkinter as tk

""" BOM object that holds info about it """
class Bom:
    def __init__(self, main_window, upload_window, bom_dataframe, bom_status):       
        self.name = upload_window.input_storage[0].input.get('1.0', 'end').strip()
        self.description = upload_window.input_storage[1].input.get('1.0', 'end').strip()
        self.quantity = upload_window.input_storage[2].input.get('1.0', 'end').strip()
        self.reference_designator = upload_window.input_storage[3].input.get('1.0', 'end').strip()
        self.manufacturer = upload_window.input_storage[4].input.get('1.0', 'end').strip()
        self.manufacturer_part_number = upload_window.input_storage[5].input.get('1.0', 'end').strip()
        self.header = upload_window.input_storage[6].input.get('1.0', 'end').strip()
        self.bom_dataframe = bom_dataframe
        self.bom_status = bom_status
        self.selected = tk.IntVar(main_window, 0) # this is getting linked back to the main window bc the upload window goes away when you upload a bom

