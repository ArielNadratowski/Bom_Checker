import tkinter as tk
from button_with_text import ButtonWithText
from tkinter import filedialog, Toplevel, messagebox
from button_with_label import ButtonWithLabel
import pandas as pd
from bom import Bom

class BomUploadWindow(Toplevel):
     
    def __init__(self, bom_storage, bom_frame, main_window):
        super().__init__()
        # set up window
        self.title('Upload Bom')
        self.geometry('800x800')
        self.wm_attributes("-topmost", True)

        label = tk.Label(self, text ='Upload a Bom')
        label.grid(row = 0, column = 0, columnspan = 2)

        # create text input and labels 
        button_starting_row = 1
        input_list = ['Bom Name', 'Description', 'Quantity', 'Reference Designator', 'Manufacturer', 'Manufacturer Part Number', 'Header Row'] # would be nice to see if this can be enum for use later in select_and_load_bom 
        self.input_storage = []

        for input in input_list:
            self.input_storage.append(ButtonWithText(self, input, button_starting_row))
            button_starting_row += 1

        ##### DELETE LATER #######
        self.input_storage[0].input.insert(1.0, "test") 
        self.input_storage[1].input.insert(1.0, "DESCRIPTION") 
        self.input_storage[2].input.insert(1.0, "QTY") 
        self.input_storage[3].input.insert(1.0, "REF DGN") 
        self.input_storage[4].input.insert(1.0, "MFG 1") 
        self.input_storage[5].input.insert(1.0, "MFG PN 1") 
        self.input_storage[6].input.insert(1.0, "2") 

        #######################################
        
        # create select file button and display file selected
        select_file_row = button_starting_row + 1
        select_file_button = ButtonWithLabel(self, 
                                            'Please select file', 
                                            'Select File', 
                                            select_file_row, 
                                            command_ = lambda: self.select_and_load_bom(bom_storage, bom_frame, main_window), # make bom object here
                                            column_span = 7, 
                                            sticky_ = "W")
        self.bom_label = select_file_button.label_value

        # exit window button
        exit_window_row = button_starting_row + 2
        exit_window_button = tk.Button(self, text = 'EXIT', command = self.destroy)
        exit_window_button.grid(row = exit_window_row, column = 0)


    def select_and_load_bom(self, bom_storage, bom_frame, main_window): 
        # select file
        filename = filedialog.askopenfilename()
        self.bom_label.set(filename)

        # load file
        header = self.input_storage[6].input.get('1.0', 'end').strip() # header entry will always be at index 6
        bom_dataframe, status = load_bom_from_file(filename, header)

        # create bom object
        bom = Bom(main_window, self, bom_dataframe, status)
        bom_storage.append(bom)

        # create list to store checkbutton objects
        check_buttons = []

        # create checkbuttons for boms that have been uploaded
        for index, bom in enumerate(bom_storage):
                check_buttons.append(tk.Checkbutton(bom_frame, text = bom.name, variable = bom.selected))
                check_buttons[index].pack()


def load_bom_from_file(filename, header):
    if filename.endswith('xlsx') or filename.endswith('xls'):
            try:
                bom = pd.read_excel(filename, header = int(header) - 1)
                bom.rename(columns = lambda x: x.strip(), inplace = True)
                bom_status = 1
            except ValueError:
                messagebox.showerror('Information', 'The file you have chosen is invalid or your header value is invalid!')
            except FileNotFoundError:
                messagebox.showerror('Information', f'No such file as {filename}')
    
    elif filename.endswith('csv'):
            try:
                bom = pd.read_csv(filename, header = int(header) - 1) 
                bom.rename(columns = lambda x: x.strip(), inplace = True)
                bom_status = 1
            except ValueError:
                messagebox.showerror('Information', 'The file you have chosen is invalid or your header value is invalid!')
            except FileNotFoundError:
                messagebox.showerror('Information', f'No such file as {filename}')
    return bom, bom_status
    





        