import tkinter as tk
from bom_checker_code.button_with_text import ButtonWithText
from tkinter import filedialog, Toplevel, messagebox
from bom_checker_code.button_with_label import ButtonWithLabel
import pandas as pd
import numpy as np
from bom_checker_code.bom import Bom

SET_DEBUG = False

""" Separate window from Main Window where BOMs are uploaded from a file """
class BomUploadWindow(Toplevel):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.title('Upload Bom')
        self.geometry('800x400')
        self.wm_attributes("-topmost", True)
        self.button_starting_row = None
        self.input_storage = []
        self.bom_label = None

        self._set_up_window()
        self._create_text_input_and_labels()
        if SET_DEBUG:
            self._set_debug_inputs()
        self._create_select_file_button()
        self._create_exit_button()
        
    def _set_up_window(self):
        label = tk.Label(self, text ='Upload a Bom')
        label.grid(row = 0, column = 0, columnspan = 2)

    def _create_text_input_and_labels(self):
        self.button_starting_row = 1
        input_list = [
            'Bom Name', 
            'Description', 
            'Quantity', 
            'Reference Designator', 
            'Manufacturer', 
            'Manufacturer Part Number', 
            'Header Row'
        ]

        for input in input_list:
            self.input_storage.append(ButtonWithText(self, input, self.button_starting_row))
            self.button_starting_row += 1

    def _set_debug_inputs(self):
        self.input_storage[0].input.insert(1.0, 'test') 
        self.input_storage[1].input.insert(1.0, 'DESCRIPTION') 
        self.input_storage[2].input.insert(1.0, 'QTY') 
        self.input_storage[3].input.insert(1.0, 'REF DGN') 
        self.input_storage[4].input.insert(1.0, 'MFG 1') 
        self.input_storage[5].input.insert(1.0, 'MFG PN 1') 
        self.input_storage[6].input.insert(1.0, '2') 

    def _create_select_file_button(self):
        select_file_row = self.button_starting_row + 1
        select_file_button = ButtonWithLabel(
            self, 
            'Please select file', 
            'Select File', 
            select_file_row, 
            command = self._import_bom, 
            column_span = 7, 
            sticky = "W"
        )
        self.bom_label = select_file_button.label_value

    def _create_exit_button(self):
        exit_window_row = self.button_starting_row + 2
        exit_window_button = tk.Button(self, text = 'EXIT', command = self.destroy)
        exit_window_button.grid(row = exit_window_row, column = 0)

    def _import_bom(self): 
        # prevent uploading boms with same name
        for bom in self.main_window.upload_frame.boms:
            if self.input_storage[0].input.get('1.0', 'end').strip() == bom.name:
                messagebox.showerror('Error', 'Cannot have identical bom names.')
                return
        bom_dataframe, bom_status = self._select_and_load_bom()
        cleaned_bom = self._make_cleaned_bom(bom_dataframe)
        bom = self._make_bom_object(cleaned_bom, bom_status)
        self._make_bom_checkbuttons(bom)

    def _select_and_load_bom(self):
        # select file
        filename = filedialog.askopenfilename()
        self.bom_label.set(filename)

        # load file
        header = self.input_storage[6].input.get('1.0', 'end').strip() # header entry will always be at index 6
        bom_dataframe, bom_status = self._load_bom_from_file(filename, header)
        return bom_dataframe, bom_status

    def _make_cleaned_bom(self, bom_dataframe):
        input_ref_dsg = self.input_storage[3].input.get('1.0', 'end').strip()
        input_description = self.input_storage[1].input.get('1.0', 'end').strip()
        input_quantity = self.input_storage[2].input.get('1.0', 'end').strip()
        input_manufacturer = self.input_storage[4].input.get('1.0', 'end').strip()
        input_manufacturer_part_number = self.input_storage[5].input.get('1.0', 'end').strip()

        cleaned_bom = self._clean_bom(
            bom_dataframe, 
            input_ref_dsg, 
            input_description, 
            input_quantity, 
            input_manufacturer, 
            input_manufacturer_part_number
        )
        return cleaned_bom

    def _make_bom_object(self, cleaned_bom, bom_status):
        bom = Bom(self.main_window, self, cleaned_bom, bom_status)
        self.main_window.upload_frame.boms.append(bom)
        return bom

    def _make_bom_checkbuttons(self, bom_object):
        check_button = tk.Checkbutton(
            self.main_window.upload_frame.boms_uploaded_frame, 
            text = bom_object.name, 
            variable = bom_object.selected
        )
        check_button.pack()

    def _load_bom_from_file(self, filename, header_index):
        if filename.endswith('xlsx') or filename.endswith('xls'):
                try:
                    bom = pd.read_excel(filename, header = int(header_index) - 1)
                    bom.rename(columns = lambda x: x.strip(), inplace = True)
                    bom_status = 1
                except ValueError:
                    messagebox.showerror('Information', 'The file you have chosen is invalid or your header value is invalid!')
                except FileNotFoundError:
                    messagebox.showerror('Information', f'No such file as {filename}')
        
        elif filename.endswith('csv'):
                try:
                    bom = pd.read_csv(filename, header = int(header_index) - 1) 
                    bom.rename(columns = lambda x: x.strip(), inplace = True)
                    bom_status = 1
                except ValueError:
                    messagebox.showerror('Information', 'The file you have chosen is invalid or your header value is invalid!')
                except FileNotFoundError:
                    messagebox.showerror('Information', f'No such file as {filename}')
        return bom, bom_status

    """ Does some data cleaning on the BOM to fix formating and stuff for later """
    def _clean_bom(
            self, 
            input_bom, 
            input_ref_dsg, 
            input_description, 
            input_quantity, 
            input_manufacturer, 
            input_manufacturer_part_number
    ):
        # drop any rows that are missing reference designators
        input_bom_clean = input_bom.dropna(subset=[input_ref_dsg], inplace=False) 
        # replacing null values (floats) with certain string because trying to apply strimg methods down a 
        # column with float NAs makes it mad
        input_bom_clean = input_bom_clean.fillna('<NA>') 
        # get rid of any whitespace so that the next line splits cleanly
        input_bom_clean[input_ref_dsg] = input_bom_clean[input_ref_dsg].str.replace(' ','') 
        input_bom_clean[input_manufacturer_part_number] = input_bom_clean[input_manufacturer_part_number].astype(str)
        # use regex to insert a comma only when numbers -> letters (ABC123,ABC123). 
        # Removes an extra comma if there is already a comma there, and removes the trailing comma that it inserts.
        input_bom_clean[input_ref_dsg] = input_bom_clean[input_ref_dsg].astype(str)
        input_bom_clean[input_ref_dsg] = input_bom_clean[input_ref_dsg].str.replace(r'[a-zA-Z]+[0-9]+', r'\g<0>,', regex=True)
        # r'[a-zA-Z]+[0-9]+' detects pattern that starts with any number of letter and then any number of numbers
        # r'\g<0>,' takes the text of the whole match (\g<0>) and adds a period at the end of it (,)
        input_bom_clean[input_ref_dsg] = input_bom_clean[input_ref_dsg].str.replace(',,', ',')
        input_bom_clean[input_ref_dsg] = input_bom_clean[input_ref_dsg].str[:-1]

        # count number of commas for quamtity check and cbind new column to dataset
        number_items = []
        for item in input_bom_clean[input_ref_dsg]:
            number_items.append(str(item).count(',') + 1)
        input_bom_clean = input_bom_clean.reset_index()
        column_to_bind = pd.DataFrame({'number_of_items': number_items})
        input_bom_clean = pd.concat([input_bom_clean, column_to_bind], axis=1)
        input_bom_clean['quantity_mismatch'] = np.where((pd.to_numeric(input_bom_clean['number_of_items']) != pd.to_numeric(input_bom_clean[input_quantity])), True, False)
        
        # splits to new columns on the comma
        split_columns = input_bom_clean[input_ref_dsg].str.split(',', expand=True) 
        ref_dsg_position = list(split_columns.columns.values)
        input_bom_clean = pd.concat([input_bom_clean, split_columns], axis=1) 

        input_bom_clean['original_index'] = range(0, len(input_bom_clean))
        # using pivot longer (melt) to reformat. Does lose any columns not listed here.
        input_bom_clean = pd.melt(
            input_bom_clean, 
            id_vars=['original_index', input_description, input_quantity, input_manufacturer, input_manufacturer_part_number, 'quantity_mismatch'], 
            value_vars = ref_dsg_position, 
            value_name = 'split_ref_designators', 
            var_name = 'ref_dsg_position'
        ) 
        input_bom_clean = input_bom_clean.sort_values(by = ['split_ref_designators'])
        input_bom_clean.dropna(subset=['split_ref_designators'], inplace=True) 
        input_bom_clean = input_bom_clean.reset_index() # need to reset index for later comparisons
        return(input_bom_clean)

  

        