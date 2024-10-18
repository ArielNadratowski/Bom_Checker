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
        self.geometry('800x400')
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

        # do a quick clean of the dataframe
        input_ref_dsg = self.input_storage[3].input.get('1.0', 'end').strip()
        input_description = self.input_storage[1].input.get('1.0', 'end').strip()
        input_quantity = self.input_storage[2].input.get('1.0', 'end').strip()
        input_manufacturer = self.input_storage[4].input.get('1.0', 'end').strip()
        input_manufacturer_part_number = self.input_storage[5].input.get('1.0', 'end').strip()

        cleaned_bom = clean_bom(bom_dataframe, input_ref_dsg, input_description, input_quantity, input_manufacturer, input_manufacturer_part_number)

        # create bom object
        bom = Bom(main_window, self, cleaned_bom, status)
        bom_storage.append(bom)

        # create checkbuttons for bom
        check_button = tk.Checkbutton(bom_frame, text = bom.name, variable = bom.selected)
        check_button.pack()


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
    


def clean_bom(input_bom, input_ref_dsg, input_description, input_quantity, input_manufacturer, input_manufacturer_part_number):
    input_bom_no_na = input_bom.dropna(subset=[input_ref_dsg], inplace=False) # drop any rows that are missing reference designators
    input_bom_no_na = input_bom_no_na.fillna('<NA>') # replacing null values (floats) with certain string because trying to apply strimg methods down a column with float NAs makes it mad
    input_bom_no_na[input_ref_dsg] = input_bom_no_na[input_ref_dsg].str.replace(' ','') # get rid of any whitespace so that the next line splits cleanly

    # use regex to insert a comma only when numbers > letters (ABC123,ABC123). Removes an extra comma if there is already a comma there, and removes the trailing comma that it inserts.
    input_bom_no_na[input_ref_dsg] = input_bom_no_na[input_ref_dsg].astype(str)
    input_bom_no_na[input_ref_dsg] = input_bom_no_na[input_ref_dsg].str.replace(r'[a-zA-Z]+[0-9]+', r'\g<0>,', regex=True)
    # r'[a-zA-Z]+[0-9]+' detects pattern that starts with any number of letter and any number of numbers
    # r'\g<0>,' takes the text of the whole match (\g<0>) and adds a period at the end of it (,)

    input_bom_no_na[input_ref_dsg] = input_bom_no_na[input_ref_dsg].str.replace(',,', ',')
    input_bom_no_na[input_ref_dsg] = input_bom_no_na[input_ref_dsg].str[:-1]
    
    split_columns = input_bom_no_na[input_ref_dsg].str.split(',', expand=True) # splits to new columns on the comma
    ref_dsg_position = list(split_columns.columns.values)
    input_bom_no_na = pd.concat([input_bom_no_na, split_columns], axis=1) 

    input_bom_no_na['original_index'] = range(0, len(input_bom_no_na))
    # using pivot longer (melt) to reformat. Does lose any columns not listed here. TODO: fix quantities 
    input_bom_no_na = pd.melt(input_bom_no_na, id_vars=['original_index', input_description, input_quantity, input_manufacturer, input_manufacturer_part_number], value_vars = ref_dsg_position, value_name = 'split_ref_designators', var_name = 'ref_dsg_position') 
    input_bom_no_na = input_bom_no_na.sort_values(by = ['split_ref_designators'])
    input_bom_no_na.dropna(subset=['split_ref_designators'], inplace=True) 
    input_bom_no_na = input_bom_no_na.reset_index() # need to reset index for later comparisons
    return(input_bom_no_na)

  

        