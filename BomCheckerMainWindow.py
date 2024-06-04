import tkinter as tk
from tableview import tableview
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import Main_Window_Support_Functions
from ButtonWithText import ButtonWithText
from ButtonWithLabel import ButtonWithLabel

class BomCheckerMainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        # set up main window size and title
        self.geometry('1700x800')
        self.title('Bom Checker')
        self.test_name = tk.Label(self, text = 'Bom Checker :)', font = ('Segoe UI', 15, 'bold'))
        self.test_name.pack(side = 'top')

        # set up frame for buttons you interact with
        input_frame = tk.Frame(self)
        input_frame.pack(side = 'top')

        # directions for how to use
        instructions = tk.Label(input_frame, text = 'Please type the following column names EXACTLY as labeled in their respective BOM file', font = ('Segoe UI', 11, 'bold'))
        instructions.grid(row = 0, column = 0, columnspan = 10, sticky = 'W', padx = 5, pady = 5)

        # set up values for buttons with labels
        upload_bomA_button_coord = (3, 2)
        upload_bomB_button_coord = (4, 2)

        # create and place buttons with labels
        upload_bomA_button = ButtonWithLabel(input_frame, 
                                                 'Please upload file', 
                                                 'upload BOM A', 
                                                 upload_bomA_button_coord, 
                                                 command_ = self.uploadFileA, 
                                                 pady_ = (30, 5), 
                                                 column_span = 7, 
                                                 sticky_ = "W")
        
        self.bomA_label_value = upload_bomA_button.label_value

        upload_bomB_button = ButtonWithLabel(input_frame, 
                                                 'Please upload file', 
                                                 'upload BOM B', 
                                                 upload_bomB_button_coord, 
                                                 command_ = self.uploadFileB,
                                                 column_span = 7, 
                                                 sticky_ = "W")
        
        self.bomB_label_value = upload_bomB_button.label_value

        # set up values for buttons with text
        descriptionA_coord = (1, 1)
        descriptionB_coord = (2, 1)
        quantityA_coord = (1, 3)
        quantityB_coord = (2, 3)
        ref_dsgA_coord  = (1, 5)
        ref_dsgB_coord = (2, 5)
        manuA_coord = (1, 7)
        manuB_coord = (2, 7)
        mpnA_coord = (1, 9)
        mpnB_coord = (2, 9)
        headerA_coord = (3, 1)
        headerB_coord = (4, 1)

        # create and place buttons with text
        descriptionA = ButtonWithText(input_frame, 'Description BOM A', descriptionA_coord)
        self.descriptionA_input = descriptionA.input
        descriptionA.input.insert(tk.END, 'DESCRIPTION')

        descriptionB = ButtonWithText(input_frame, 'Description BOM B', descriptionB_coord)
        self.descriptionB_input = descriptionB.input
        descriptionB.input.insert(tk.END, 'DESCRIPTION')

        quantityA = ButtonWithText(input_frame, 'Quantity BOM A', quantityA_coord)
        self.quantityA_input = quantityA.input
        quantityA.input.insert(tk.END, 'QTY')

        quantityB = ButtonWithText(input_frame, 'Quantity BOM B', quantityB_coord)
        self.quantityB_input = quantityB.input
        quantityB.input.insert(tk.END, 'QTY')

        ref_dsgA = ButtonWithText(input_frame, 'Reference Designator BOM A', ref_dsgA_coord)
        self.ref_dsgA_input = ref_dsgA.input
        ref_dsgA.input.insert(tk.END, 'REF DGN')

        ref_dsgB = ButtonWithText(input_frame, 'Reference Designator BOM B', ref_dsgB_coord)
        self.ref_dsgB_input = ref_dsgB.input
        ref_dsgB.input.insert(tk.END, 'REF DGN')

        manuA = ButtonWithText(input_frame, 'Manufacturer BOM A', manuA_coord)
        self.manuA_input = manuA.input
        manuA.input.insert(tk.END, 'MFG 1')

        manuB = ButtonWithText(input_frame, 'Manufacturer BOM B', manuB_coord)
        self.manuB_input = manuB.input
        manuB.input.insert(tk.END, 'MFG 1')

        mpnA = ButtonWithText(input_frame, 'Manufacturer Part Number BOM A', mpnA_coord)
        self.mpnA_input = mpnA.input
        mpnA.input.insert(tk.END, 'MFG PN 1')

        mpnB = ButtonWithText(input_frame, 'Manufacturer Part Number BOM B', mpnB_coord)
        self.mpnB_input = mpnB.input
        mpnB.input.insert(tk.END, 'MFG PN 1')

        headerA = ButtonWithText(input_frame, 'Header Row BOM A', headerA_coord, pady_ = (30, 5))
        self.headerA_input = headerA.input
        headerA.input.insert(tk.END, '2')

        headerB = ButtonWithText(input_frame, 'Header Row BOM B', headerB_coord)
        self.headerB_input = headerB.input
        headerB.input.insert(tk.END, '2')

        # some additional buttons that don't fit into the button-with-label or button-with-text classes
        compare_button = tk.Button(input_frame, text = 'COMPARE BOMs', command = self.compareBoms)
        compare_button.grid(row = 7, column = 0, columnspan = 10, padx = 10, pady = 10)

        search_button = tk.Button(input_frame, text = 'Search Ref Dsg', command = self.searchRefDsg)
        search_button.grid(row = 8, column = 10, padx = 10, pady = 10)
        self.search_input = tk.Text(input_frame, height = 1, width = 10)
        self.search_input.grid(row = 8, column = 9, padx = 10, pady = 10)

        # make frame to display the warnings
        self.warnings_frame = tk.Frame(self)
        self.warnings_frame.pack(side = 'top', padx = 10, pady = 10)
        self.warnings_frame.pack_propagate(False)
        
        # frame for the flagged rows from the BOMs
        self.flagged_rows_frame = tk.LabelFrame(self, text = 'Flagged Rows')
        self.flagged_rows_frame.pack(side = 'bottom', fill = 'both', expand = True, padx = 10, pady = 10)

        # Bom statuses (1 = loaded, 0 = not loaded)
        self.bomA_status = 0
        self.bomB_status = 0

        self.merged_boms = []

        # table view implementation
        HEADER_List = ['Ref Dsg', 'Description_A', 'Quantity_A', 'Manufacturer_A', 'Manufacturer Part Number_A', 
                       'Description_B', 'Quantity_B', 'Manufacturer_B', 'Manufacturer Part Number_B', 
                       'Desc_match_ratio', 'MFG_match_ratio', 'MPN_match_ratio']
        COLUMN_WIDTH = [55, 85, 75, 100, 170, 85, 75, 100, 170, 110, 110, 110]
        COLOR_MAP = {
            'header_background': 'grey70',
            'header_foreground': 'black',
            'tree_background': 'white',
            'tree_foreground': 'grey',
            'item_foreground': 'black',
            'tree_erase_background': 'white',
            'selected_row_bg_color': 'grey90',
            'selected_row_text_color': 'black',
            'separator_color':'grey'
            }
            
        tableview.setup_columns(root = self.flagged_rows_frame, 
                                window = self.flagged_rows_frame, 
                                column_headers = HEADER_List, 
                                column_widths = COLUMN_WIDTH, 
                                table_height = 20, 
                                frame_height = 700, 
                                column_height = 200, 
                                header_height = 49, 
                                table_color_map = COLOR_MAP)
        tableview.pack()

    def uploadFileA(self): 
        filename = filedialog.askopenfilename()
        self.bomA_label_value.set(filename)

        self.descA = self.descriptionA_input.get('1.0', 'end').strip()
        self.quantA = self.quantityA_input.get('1.0', 'end').strip()
        self.ref_dsgA = self.ref_dsgA_input.get('1.0', 'end').strip()
        self.manuA = self.manuA_input.get('1.0', 'end').strip()
        self.mpnA = self.mpnA_input.get('1.0', 'end').strip()
        self.headerA = self.headerA_input.get('1.0', 'end').strip()

        if filename.endswith('xlsx'):
            try:
                self.bomA = pd.read_excel(filename, header = int(self.headerA) - 1)
                self.bomA.rename(columns = lambda x: x.strip(), inplace = True)
                self.bomA_status = 1
            except ValueError:
                messagebox.showerror('Information', 'The file you have chosen is invalid or your header value is invalid!')
            except FileNotFoundError:
                messagebox.showerror('Information', f'No such file as {filename}')
        
        elif filename.endswith('csv'):
            try:
                self.bomA = pd.read_csv(filename, header = int(self.headerA) - 1) 
                self.bomA.rename(columns = lambda x: x.strip(), inplace = True)
                self.bomA_status = 1
            except ValueError:
                messagebox.showerror('Information', 'The file you have chosen is invalid or your header value is invalid!')
            except FileNotFoundError:
                messagebox.showerror('Information', f'No such file as {filename}')

        
    def uploadFileB(self): 
        filename = filedialog.askopenfilename()
        self.bomB_label_value.set(filename)

        self.descB = self.descriptionB_input.get('1.0', 'end').strip()
        self.quantB = self.quantityB_input.get('1.0', 'end').strip()
        self.ref_dsgB = self.ref_dsgB_input.get('1.0', 'end').strip()
        self.manuB = self.manuB_input.get('1.0', 'end').strip()
        self.mpnB = self.mpnB_input.get('1.0', 'end').strip()
        self.headerB = self.headerB_input.get('1.0', 'end').strip()

        if filename.endswith('xlsx'):
            try:
                self.bomB = pd.read_excel(filename, header = int(self.headerB) - 1) 
                self.bomB.rename(columns = lambda x: x.strip(), inplace = True)
                self.bomB_status = 1
            except ValueError:
                messagebox.showerror('Information', 'The file you have chosen is invalid or your header value is invalid!')
            except FileNotFoundError:
                messagebox.showerror('Information', f'No such file as {filename}')

        elif filename.endswith('csv'):
            try:
                self.bomB = pd.read_csv(filename, header = int(self.headerB) - 1) 
                self.bomB.rename(columns = lambda x: x.strip(), inplace = True)
                self.bomB_status = 1
            except ValueError:
                messagebox.showerror('Information', 'The file you have chosen is invalid or your header value is invalid!')
            except FileNotFoundError:
                messagebox.showerror('Information', f'No such file as {filename}')


    def compareBoms(self):
        if self.bomA_status == 1 and self.bomB_status == 1: # want: make this throw an error if this doesn't evaluate
            warnings_row = []
            warnings_list = []
            highlight_column_numbers = []
            highlight_row_numbers = []

            restructured_bomA = Main_Window_Support_Functions.splitRefDesignatorSeparateRows(warnings_list, self.bomA, self.ref_dsgA, self.descA, self.quantA, self.manuA, self.mpnA)
            restructured_bomB = Main_Window_Support_Functions.splitRefDesignatorSeparateRows(warnings_list, self.bomB, self.ref_dsgB, self.descB, self.quantB, self.manuB, self.mpnB)
            
            Main_Window_Support_Functions.checkBomsExactMatch(warnings_list, restructured_bomA, restructured_bomB)    
            Main_Window_Support_Functions.checkForDuplicates(warnings_list, restructured_bomA, restructured_bomB)
            flagged_rows_temp_storage = Main_Window_Support_Functions.compareRefDesignators(warnings_list, highlight_column_numbers, highlight_row_numbers, restructured_bomA, restructured_bomB)

            tableview.clear()

            # fill in table
            number_rows = len(flagged_rows_temp_storage.index)
            for i in range(number_rows):
                column_number = 0
                row_as_list = flagged_rows_temp_storage.iloc[i].tolist()
                for item in row_as_list:
                    tableview.insert_item(column_number, text = item)
                    column_number += 1
            
            # highlight cells that are different
            for c, r in zip(highlight_column_numbers, highlight_row_numbers):
                tableview.highlight_cell(column = c, row = r, bg = 'yellow', fg = 'red')
            
            # show warnings
            for widgets in self.warnings_frame.winfo_children():
                widgets.destroy()
            for index, value in enumerate(warnings_list):
                warnings_row.append(ttk.Label(self.warnings_frame, text = value, foreground = 'red'))
                warnings_row[index].grid()

            # probably best place to stick this due to scoping
            self.merged_boms = restructured_bomA.merge(restructured_bomB, how='outer', on='split_ref_designators', sort=True, suffixes=('_A', '_B'), copy=None, indicator=False, validate=None)
            self.merged_boms.drop(['index_A', 'original_index_A', 'ref_dsg_position_A', 'index_B', 'original_index_B', 'ref_dsg_position_B'], axis=1, inplace = True)
            self.merged_boms = self.merged_boms[['split_ref_designators', 
                                                 'Description_A', 'Quantity_A', 'Manufacturer_A', 'Manufacturer Part Number_A', 
                                                 'Description_B', 'Quantity_B', 'Manufacturer_B', 'Manufacturer Part Number_B']]
            self.merged_boms.rename(columns = {'split_ref_designators': 'Ref Dsg'}, inplace = True)
            col = self.merged_boms.pop('Ref Dsg')
            self.merged_boms.insert(0, col.name, col)


    def searchRefDsg(self):
        tableview.clear()

        search_text = self.search_input.get('1.0', 'end')
        search_text = search_text.strip()

        self.merged_boms['Ref Dsg'] = self.merged_boms['Ref Dsg'].str.strip()

        searched_rows = self.merged_boms[self.merged_boms['Ref Dsg'] == search_text]

        # fill in table 
        number_rows = len(searched_rows.index)
        for i in range(number_rows):
            column_number = 0
            row_as_list = searched_rows.iloc[i].tolist()
            for item in row_as_list:
                tableview.insert_item(column_number, text = item)
                column_number += 1

