import tkinter as tk
from tableview import tableview
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import Support_Functions_Main_Window_Class

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

        # Upload bom buttons and their respective labels

        self.bomA_label_value = tk.StringVar(input_frame, 'Please upload file')
        bomA_button = tk.Button(input_frame, text = 'upload BOM A', command = self.uploadFileA)
        self.bomA_label = tk.Label(input_frame, textvariable=self.bomA_label_value)
        bomA_button.grid(row = 3, column = 2, padx = 5, pady = (30, 5))
        self.bomA_label.grid(row = 3, column = 3, columnspan = 7, sticky = 'W', padx = 5, pady = (30, 5))

        self.bomB_label_value = tk.StringVar(input_frame, 'Please upload file')
        bomB_button = tk.Button(input_frame, text = 'upload BOM B', command = self.uploadFileB)
        self.bomB_label = tk.Label(input_frame, textvariable=self.bomB_label_value)   
        bomB_button.grid(row = 4, column = 2)
        self.bomB_label.grid(row = 4, column = 3, columnspan = 7, sticky = 'W', padx = 5, pady = 5)

        # take input for what columns are what
        instructions = tk.Label(input_frame, text = 'Please type the following column names EXACTLY as labeled in their respective BOM file', font = ('Segoe UI', 11, 'bold'))
        instructions.grid(row = 0, column = 0, columnspan = 10, sticky = 'W', padx = 5, pady = 5)

        self.descriptionA_input = tk.Text(input_frame, height =1, width = 15)
        self.descriptionA_input.insert(tk.END, 'DESCRIPTION')
        descriptionA_label = tk.Label(input_frame, text = 'Description BOM A')
        self.descriptionA_input.grid(row = 1, column = 1, padx = 5, pady = 5)
        descriptionA_label.grid(row = 1, column = 0, padx = 5, pady = 5)

        self.descriptionB_input = tk.Text(input_frame, height = 1, width = 15)
        self.descriptionB_input.insert(tk.END, 'DESCRIPTION')
        descriptionB_label = tk.Label(input_frame, text = 'Description BOM B')
        self.descriptionB_input.grid(row = 2, column = 1, padx = 5, pady = 5)
        descriptionB_label.grid(row = 2, column = 0, padx = 5, pady = 5)

        self.quantityA_input = tk.Text(input_frame, height = 1, width = 15)
        self.quantityA_input.insert(tk.END, 'QTY')
        quantityA_label = tk.Label(input_frame, text = 'Quantity BOM A')
        self.quantityA_input.grid(row = 1, column = 3, padx = 5, pady = 5)
        quantityA_label.grid(row = 1, column = 2, padx = 5, pady = 5)

        self.quantityB_input = tk.Text(input_frame, height = 1, width = 15)
        self.quantityB_input.insert(tk.END, 'QTY')
        quantityB_label = tk.Label(input_frame, text = 'Quantity BOM B')
        self.quantityB_input.grid(row = 2, column = 3, padx = 5, pady = 5)
        quantityB_label.grid(row = 2, column = 2, padx = 5, pady = 5)

        self.ref_dsgA_input = tk.Text(input_frame, height = 1, width = 15)
        self.ref_dsgA_input.insert(tk.END, 'REF DGN')
        ref_dsgA_label = tk.Label(input_frame, text = 'Reference Designator BOM A')
        self.ref_dsgA_input.grid(row = 1, column = 5, padx = 5, pady = 5)
        ref_dsgA_label.grid(row = 1, column = 4, padx = 5, pady = 5)

        self.ref_dsgB_input = tk.Text(input_frame, height = 1, width = 15)
        self.ref_dsgB_input.insert(tk.END, 'REF DGN')
        ref_dsgB_label = tk.Label(input_frame, text = 'Reference Designator BOM B')
        self.ref_dsgB_input.grid(row = 2, column = 5, padx = 5, pady = 5)
        ref_dsgB_label.grid(row = 2, column = 4, padx = 5, pady = 5)

        self.manuA_input = tk.Text(input_frame, height = 1, width = 15)
        self.manuA_input.insert(tk.END, 'MFG 1')
        manuA_label = tk.Label(input_frame, text = 'Manufacturer BOM A')
        self.manuA_input.grid(row = 1, column = 7, padx = 5, pady = 5)
        manuA_label.grid(row = 1, column = 6, padx = 5, pady = 5)

        self.manuB_input = tk.Text(input_frame, height = 1, width = 15)
        self.manuB_input.insert(tk.END, 'MFG 1')
        manuB_label = tk.Label(input_frame, text = 'Manufacturer BOM B')
        self.manuB_input.grid(row = 2, column = 7, padx = 5, pady = 5)
        manuB_label.grid(row = 2, column = 6, padx = 5, pady = 5)
        
        self.mpnA_input = tk.Text(input_frame, height = 1, width = 15)
        self.mpnA_input.insert(tk.END, 'MFG PN 1')
        mpnA_label = tk.Label(input_frame, text = 'Manufacturer Part Number BOM A')
        self.mpnA_input.grid(row = 1, column = 9, padx = 5, pady = 5)
        mpnA_label.grid(row = 1, column = 8, padx = 5, pady = 5)

        self.mpnB_input = tk.Text(input_frame, height = 1, width = 15)
        self.mpnB_input.insert(tk.END, 'MFG PN 1')
        mpnB_label = tk.Label(input_frame, text = 'Manufacturer Part Number BOM B')
        self.mpnB_input.grid(row = 2, column = 9, padx = 5, pady = 5)
        mpnB_label.grid(row = 2, column = 8, padx = 5, pady = 5)
 
        self.headerA_input = tk.Text(input_frame, height = 1, width = 10)
        self.headerA_input.insert(tk.END, '2')
        headerA_label = tk.Label(input_frame, text = 'Header Row BOM A')
        self.headerA_input.grid(row = 3, column = 1, padx = 5, pady = (30, 5))
        headerA_label.grid(row = 3, column = 0, padx = 5, pady = (30, 5))

        self.headerB_input = tk.Text(input_frame, height = 1, width = 10)
        self.headerB_input.insert(tk.END, '2')
        headerB_label = tk.Label(input_frame, text = 'Header Row BOM B')
        self.headerB_input.grid(row = 4, column = 1, padx = 5, pady = 5)
        headerB_label.grid(row = 4, column = 0, padx = 5, pady = 5)

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
        header_list = ['Ref Dsg', 'Description_A', 'Quantity_A', 'Manufacturer_A', 'Manufacturer Part Number_A', 'Description_B', 'Quantity_B', 'Manufacturer_B', 'Manufacturer Part Number_B', 'Desc_match_ratio', 'MFG_match_ratio', 'MPN_match_ratio']
        column_header = header_list
        column_width = [55, 85, 75, 100, 170, 85, 75, 100, 170, 110, 110, 110]
        color_map = {
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
            
        tableview.setup_columns(root = self.flagged_rows_frame, window = self.flagged_rows_frame, column_headers = column_header, column_widths = column_width, table_height = 20, frame_height = 700, column_height = 200, header_height = 49, table_color_map = color_map)
        tableview.pack()

    def uploadFileA(self, *_): 
        filename = filedialog.askopenfilename()
        self.bomA_label_value.set(filename)

        self.descA = self.descriptionA_input.get('1.0', 'end')
        self.descA = self.descA.strip()
        self.quantA = self.quantityA_input.get('1.0', 'end')
        self.quantA = self.quantA.strip()
        self.ref_dsgA = self.ref_dsgA_input.get('1.0', 'end')
        self.ref_dsgA = self.ref_dsgA.strip()
        self.manuA = self.manuA_input.get('1.0', 'end')
        self.manuA = self.manuA.strip()
        self.mpnA = self.mpnA_input.get('1.0', 'end')
        self.mpnA = self.mpnA.strip()
        self.headerA = self.headerA_input.get('1.0', 'end')
        self.headerA  = self.headerA.strip()

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

        
    def uploadFileB(self, *_): 
        filename = filedialog.askopenfilename()
        self.bomB_label_value.set(filename)

        self.descB = self.descriptionB_input.get('1.0', 'end')
        self.descB = self.descB.strip()
        self.quantB = self.quantityB_input.get('1.0', 'end')
        self.quantB = self.quantB.strip()
        self.ref_dsgB = self.ref_dsgB_input.get('1.0', 'end')
        self.ref_dsgB = self.ref_dsgB.strip()
        self.manuB = self.manuB_input.get('1.0', 'end')
        self.manuB = self.manuB.strip()
        self.mpnB = self.mpnB_input.get('1.0', 'end')
        self.mpnB = self.mpnB.strip()
        self.headerB = self.headerB_input.get('1.0', 'end')
        self.headerB  = self.headerB.strip()

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


    def compareBoms(self, *_):
        if self.bomA_status == 1 and self.bomB_status == 1: # want: make this throw an error if this doesn't evaluate
            warnings_row = []
            warnings_list = []
            highlight_column_numbers = []
            highlight_row_numbers = []

            restructured_bomA = Support_Functions_Main_Window_Class.split_Ref_Designator_To_Separate_Columns(warnings_list, self.bomA, self.ref_dsgA, self.descA, self.quantA, self.manuA, self.mpnA)
            restructured_bomB = Support_Functions_Main_Window_Class.split_Ref_Designator_To_Separate_Columns(warnings_list, self.bomB, self.ref_dsgB, self.descB, self.quantB, self.manuB, self.mpnB)
            
            Support_Functions_Main_Window_Class.check_Boms_Exact_Match(warnings_list, restructured_bomA, restructured_bomB)    
            Support_Functions_Main_Window_Class.check_For_Duplicates(warnings_list, restructured_bomA, restructured_bomB)
            flagged_rows_temp_storage = Support_Functions_Main_Window_Class.compare_Ref_Designators(warnings_list, highlight_column_numbers, highlight_row_numbers, restructured_bomA, restructured_bomB)

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
            self.merged_boms = self.merged_boms[['split_ref_designators', 'Description_A', 'Quantity_A', 'Manufacturer_A', 'Manufacturer Part Number_A', 'Description_B', 'Quantity_B', 'Manufacturer_B', 'Manufacturer Part Number_B']]
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

