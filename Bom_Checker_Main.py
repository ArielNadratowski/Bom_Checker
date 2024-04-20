# Bom Checker main window

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import numpy as np
#import re
import difflib
from functools import partial
from tableview import tableview


def main():

    BomCheckerMainWindow().mainloop() 


class BomCheckerMainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        # set up main window size and title
        self.geometry("1500x800")
        self.title("Bom Checker")
        self.test_name = tk.Label(self, text = "Bom Checker :)", font = ("Segoe UI", 15, "bold"))
        self.test_name.pack(side = "top")

        # set up frame for buttons you interact with
        input_frame = tk.Frame(self)
        input_frame.pack(side = "top")

        self.bomA_label_value = tk.StringVar(input_frame, "Please upload file")
        bomA_button = tk.Button(input_frame, text = "upload BOM A", command = self.uploadFileA)
        self.bomA_label = tk.Label(input_frame, textvariable=self.bomA_label_value)
        bomA_button.grid(row = 3, column = 2, padx = 5, pady = (30, 5))
        self.bomA_label.grid(row = 3, column = 3, columnspan = 7, sticky = "W", padx = 5, pady = (30, 5))

        self.bomB_label_value = tk.StringVar(input_frame, "Please upload file")
        bomB_button = tk.Button(input_frame, text = "upload BOM B", command = self.uploadFileB)
        self.bomB_label = tk.Label(input_frame, textvariable=self.bomB_label_value)   
        bomB_button.grid(row = 4, column = 2)
        self.bomB_label.grid(row = 4, column = 3, columnspan = 7, sticky = "W", padx = 5, pady = 5)

        # take input for what columns are what
        instructions = tk.Label(input_frame, text = "Please type the following column names EXACTLY as labeled in their respective BOM file", font = ("Segoe UI", 11, "bold"))
        instructions.grid(row = 0, column = 0, columnspan = 10, sticky = "W", padx = 5, pady = 5)

        self.descriptionA_input = tk.Text(input_frame, height =1, width = 15)
        self.descriptionA_input.insert(tk.END, "DESCRIPTION")
        descriptionA_label = tk.Label(input_frame, text = "Description BOM A")
        self.descriptionA_input.grid(row = 1, column = 1, padx = 5, pady = 5)
        descriptionA_label.grid(row = 1, column = 0, padx = 5, pady = 5)

        self.descriptionB_input = tk.Text(input_frame, height = 1, width = 15)
        self.descriptionB_input.insert(tk.END, "DESCRIPTION")
        descriptionB_label = tk.Label(input_frame, text = "Description BOM B")
        self.descriptionB_input.grid(row = 2, column = 1, padx = 5, pady = 5)
        descriptionB_label.grid(row = 2, column = 0, padx = 5, pady = 5)

        self.quantityA_input = tk.Text(input_frame, height = 1, width = 15)
        self.quantityA_input.insert(tk.END, "QTY")
        quantityA_label = tk.Label(input_frame, text = "Quantity BOM A")
        self.quantityA_input.grid(row = 1, column = 3, padx = 5, pady = 5)
        quantityA_label.grid(row = 1, column = 2, padx = 5, pady = 5)

        self.quantityB_input = tk.Text(input_frame, height = 1, width = 15)
        self.quantityB_input.insert(tk.END, "QTY")
        quantityB_label = tk.Label(input_frame, text = "Quantity BOM B")
        self.quantityB_input.grid(row = 2, column = 3, padx = 5, pady = 5)
        quantityB_label.grid(row = 2, column = 2, padx = 5, pady = 5)

        self.ref_dsgA_input = tk.Text(input_frame, height = 1, width = 15)
        self.ref_dsgA_input.insert(tk.END, "REF DGN")
        ref_dsgA_label = tk.Label(input_frame, text = "Reference Designator BOM A")
        self.ref_dsgA_input.grid(row = 1, column = 5, padx = 5, pady = 5)
        ref_dsgA_label.grid(row = 1, column = 4, padx = 5, pady = 5)

        self.ref_dsgB_input = tk.Text(input_frame, height = 1, width = 15)
        self.ref_dsgB_input.insert(tk.END, "REF DGN")
        ref_dsgB_label = tk.Label(input_frame, text = "Reference Designator BOM B")
        self.ref_dsgB_input.grid(row = 2, column = 5, padx = 5, pady = 5)
        ref_dsgB_label.grid(row = 2, column = 4, padx = 5, pady = 5)

        self.manuA_input = tk.Text(input_frame, height = 1, width = 15)
        self.manuA_input.insert(tk.END, "MFG 1")
        manuA_label = tk.Label(input_frame, text = "Manufacturer BOM A")
        self.manuA_input.grid(row = 1, column = 7, padx = 5, pady = 5)
        manuA_label.grid(row = 1, column = 6, padx = 5, pady = 5)

        self.manuB_input = tk.Text(input_frame, height = 1, width = 15)
        self.manuB_input.insert(tk.END, "MFG 1")
        manuB_label = tk.Label(input_frame, text = "Manufacturer BOM B")
        self.manuB_input.grid(row = 2, column = 7, padx = 5, pady = 5)
        manuB_label.grid(row = 2, column = 6, padx = 5, pady = 5)
        
        self.mpnA_input = tk.Text(input_frame, height = 1, width = 15)
        self.mpnA_input.insert(tk.END, "MFG PN 1")
        mpnA_label = tk.Label(input_frame, text = "Manufacturer Part Number BOM A")
        self.mpnA_input.grid(row = 1, column = 9, padx = 5, pady = 5)
        mpnA_label.grid(row = 1, column = 8, padx = 5, pady = 5)

        self.mpnB_input = tk.Text(input_frame, height = 1, width = 15)
        self.mpnB_input.insert(tk.END, "MFG PN 1")
        mpnB_label = tk.Label(input_frame, text = "Manufacturer Part Number BOM B")
        self.mpnB_input.grid(row = 2, column = 9, padx = 5, pady = 5)
        mpnB_label.grid(row = 2, column = 8, padx = 5, pady = 5)
 
        self.headerA_input = tk.Text(input_frame, height = 1, width = 10)
        self.headerA_input.insert(tk.END, "2")
        headerA_label = tk.Label(input_frame, text = "Header Row BOM A")
        self.headerA_input.grid(row = 3, column = 1, padx = 5, pady = (30, 5))
        headerA_label.grid(row = 3, column = 0, padx = 5, pady = (30, 5))

        self.headerB_input = tk.Text(input_frame, height = 1, width = 10)
        self.headerB_input.insert(tk.END, "2")
        headerB_label = tk.Label(input_frame, text = "Header Row BOM B")
        self.headerB_input.grid(row = 4, column = 1, padx = 5, pady = 5)
        headerB_label.grid(row = 4, column = 0, padx = 5, pady = 5)

        compare_button = tk.Button(input_frame, text = "COMPARE BOMs", command = self.compareBoms)
        compare_button.grid(row = 7, column = 0, columnspan = 10, padx = 10, pady = 10)

        # make frame to display the warnings
        self.warnings_frame = tk.Frame(self)
        self.warnings_frame.pack(side = "top", padx = 10, pady = 10)
        self.warnings_frame.pack_propagate(False)
        

        # frame for the flagged rows from the BOMs
        self.flagged_rows_frame = tk.LabelFrame(self, text = "Flagged Rows")
        self.flagged_rows_frame.pack(side = "bottom", fill = "both", expand = True, padx = 10, pady = 10)

        ## treeview for the actual data
        #self.flagged_rows = ttk.Treeview(flagged_rows_frame)
        #self.flagged_rows.place(relheight = 1, relwidth = 1)
        #flagged_rows_scrolly = tk.Scrollbar(flagged_rows_frame, orient = "vertical", command = self.flagged_rows.yview)
        #flagged_rows_scrollx = tk.Scrollbar(flagged_rows_frame, orient = "horizontal", command = self.flagged_rows.xview)
        #self.flagged_rows.configure(xscrollcommand = flagged_rows_scrollx.set, yscrollcommand = flagged_rows_scrolly.set)
        #flagged_rows_scrolly.pack(side = "right", fill = "y")
        #flagged_rows_scrollx.pack(side = "bottom", fill = "x")

        



        # Bom statuses (1 = loaded, 0 = not loaded)
        self.bomA_status = 0
        self.bomB_status = 0

    






    def uploadFileA(self, *_): # ISSUE: keyerror if the file is open when you press upload file button
        filename = filedialog.askopenfilename()
        self.bomA_label_value.set(filename)

        self.descA = self.descriptionA_input.get("1.0", "end")
        self.descA = self.descA.strip()
        self.quantA = self.quantityA_input.get("1.0", "end")
        self.quantA = self.quantA.strip()
        self.ref_dsgA = self.ref_dsgA_input.get("1.0", "end")
        self.ref_dsgA = self.ref_dsgA.strip()
        self.manuA = self.manuA_input.get("1.0", "end")
        self.manuA = self.manuA.strip()
        self.mpnA = self.mpnA_input.get("1.0", "end")
        self.mpnA = self.mpnA.strip()
        self.headerA = self.headerA_input.get("1.0", "end")
        self.headerA  = self.headerA.strip()

        try:
            self.bomA = pd.read_excel(filename, header = int(self.headerA) - 1) # want: also accept csv files
            self.bomA.rename(columns = lambda x: x.strip(), inplace = True)
            self.bomA_status = 1

        except ValueError:
            messagebox.showerror("Information", "The file you have chosen is invalid or your header value is invalid!")
        
        except FileNotFoundError:
            messagebox.showerror("Information", f"No such file as {filename}")

        

    def uploadFileB(self, *_): 
        filename = filedialog.askopenfilename()
        self.bomB_label_value.set(filename)

        self.descB = self.descriptionB_input.get("1.0", "end")
        self.descB = self.descB.strip()
        self.quantB = self.quantityB_input.get("1.0", "end")
        self.quantB = self.quantB.strip()
        self.ref_dsgB = self.ref_dsgB_input.get("1.0", "end")
        self.ref_dsgB = self.ref_dsgB.strip()
        self.manuB = self.manuB_input.get("1.0", "end")
        self.manuB = self.manuB.strip()
        self.mpnB = self.mpnB_input.get("1.0", "end")
        self.mpnB = self.mpnB.strip()
        self.headerB = self.headerB_input.get("1.0", "end")
        self.headerB  = self.headerB.strip()

        try:
            self.bomB = pd.read_excel(filename, header = int(self.headerB) - 1) # want: also accept csv files
            self.bomB.rename(columns = lambda x: x.strip(), inplace = True)
            self.bomB_status = 1

        except ValueError:
            messagebox.showerror("Information", "The file you have chosen is invalid or your header value is invalid!")
        
        except FileNotFoundError:
            messagebox.showerror("Information", f"No such file as {filename}")


    def compareBoms(self, *_):
        if self.bomA_status == 1 and self.bomB_status == 1: # want: make this throw an error if this doesn't evaluate
            warnings_row = []
            warnings_list = []

            restructured_bomA = split_Ref_Designator_To_Separate_Columns(warnings_list, self.bomA, self.ref_dsgA, self.descA, self.quantA, self.manuA, self.mpnA)
            restructured_bomB = split_Ref_Designator_To_Separate_Columns(warnings_list, self.bomB, self.ref_dsgB, self.descB, self.quantB, self.manuB, self.mpnB)
            
            check_Boms_Exact_Match(warnings_list, restructured_bomA, restructured_bomB)    
            check_For_Duplicates(warnings_list, restructured_bomA, restructured_bomB)
            flagged_rows_temp_storage = compare_Ref_Designators(warnings_list, restructured_bomA, restructured_bomB)
            #self.flagged_rows["column"] = list(flagged_rows_temp_storage.columns)
            #self.flagged_rows["show"]  = "headings"
            #for column in self.flagged_rows["columns"]:
            #    self.flagged_rows.heading(column, text = column)

            #flagged_rows_temp_storage_rows = flagged_rows_temp_storage.to_numpy().tolist()
            #for row in flagged_rows_temp_storage_rows:
            #    self.flagged_rows.insert("", "end", values = row)

            # table view implementation
            column_header = list(flagged_rows_temp_storage.columns.values)
            column_width = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
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

            tableview.setup_columns(root = self, window = self.flagged_rows_frame, column_headers = column_header, column_widths = column_width, table_height = 20, frame_height = 650, column_height = 200, header_height = 49, table_color_map = color_map)
            
            # using for loops to populate the table from the pandas dataframe
            number_rows = len(flagged_rows_temp_storage.index)
            for i in range(number_rows):
                column_number = 0
                row_as_list = flagged_rows_temp_storage.iloc[i].tolist()
                for item in row_as_list:
                    tableview.insert_item(column_number, text = item)
                    column_number += 1


            tableview.pack()
            tableview.highlight_cell(column = 1, row = 0, bg = "yellow", fg = "red")
            

        for index, value in enumerate(warnings_list):
            warnings_row.append(ttk.Label(self.warnings_frame, text = value))
            warnings_row[index].grid()
            
            

    
def split_Ref_Designator_To_Separate_Columns(warnings, input_bom, input_ref_dsg, input_description, input_quantity, input_manufacturer1, input_manufacturer_part_number1):
    input_bom = input_bom.rename(columns={input_ref_dsg: "Ref Dsg", input_description: 'Description', input_quantity: 'Quantity', input_manufacturer1: 'Manufacturer 1', input_manufacturer_part_number1: 'Manufacturer 1 part number'}, errors = "raise")
    input_bom_no_na = input_bom.dropna(subset=["Ref Dsg"], inplace=False) # drop any rows that are missing reference designators
    input_bom_no_na = input_bom_no_na.fillna("<NA>") # replacing null values (floats) with certain string in case that becomes a problem later (it does if trying to apply strimg methods down a column with float NAs)
    input_bom_no_na["Ref Dsg"] = input_bom_no_na["Ref Dsg"].str.replace(" ","") # get rid of any whitespace so that the next line splits cleanly

    # use regex to insert a comma only when numbers > letters (ABC123,ABC123). Removes an extra comma if there is already a comma there, and removes the trailing comma that it inserts.
    input_bom_no_na["Ref Dsg"] = input_bom_no_na["Ref Dsg"].astype(str)
    input_bom_no_na["Ref Dsg"] = input_bom_no_na["Ref Dsg"].str.replace(r'[a-zA-Z]+[0-9]+', r'\g<0>,', regex=True)
    input_bom_no_na["Ref Dsg"] = input_bom_no_na["Ref Dsg"].str.replace(",,", ",")
    input_bom_no_na["Ref Dsg"] = input_bom_no_na["Ref Dsg"].str[:-1]
    
    split_columns = input_bom_no_na["Ref Dsg"].str.split(",", expand=True) # splits to new columns on the comma
    ref_dsg_position = list(split_columns.columns.values)
    input_bom_no_na = pd.concat([input_bom_no_na, split_columns], axis=1) 

    input_bom_no_na["original_index"] = range(0, len(input_bom_no_na))
    # using pivot longer to reformat. Does lose any columns not listed here. Will screw up quantities, do a check on that later?
    input_bom_no_na = pd.melt(input_bom_no_na, id_vars=['original_index', 'Description', 'Quantity', 'Manufacturer 1', 'Manufacturer 1 part number'], value_vars = ref_dsg_position, value_name = "split_ref_designators", var_name = "ref_dsg_position") 
    input_bom_no_na = input_bom_no_na.sort_values(by = ["split_ref_designators"])
    input_bom_no_na.dropna(subset=['split_ref_designators'], inplace=True) 
    input_bom_no_na = input_bom_no_na.reset_index() # need to do this for later comparisons
    return(input_bom_no_na)


# check if boms are exact match
def check_Boms_Exact_Match(warnings, input_bomA, input_bom_B): 
# check if exact match between boms
    if len(input_bomA) == len(input_bom_B):
        boms_exact_match = input_bomA == input_bom_B # only works if boms are same dimensions
        if np.all(boms_exact_match['Description'] == True) and np.all(boms_exact_match["Quantity"] == True) and np.all(boms_exact_match["Manufacturer 1"] == True) and np.all(boms_exact_match['Manufacturer 1 part number'] == True) and np.all(boms_exact_match["ref_dsg_position"] == True) and np.all(boms_exact_match["split_ref_designators"] == True):
            warnings.append("bomA and bomB are exact matches") # if overall boms match row for row (if so, then they're exact matches and no need to further check)
        else:
            warnings.append("bomA and bomB do not match")

# check for dupolicate entries            
def check_For_Duplicates(warnings, input_bomA, input_bomB):
    if input_bomA['split_ref_designators'].duplicated().any():
        duplicated = input_bomA['split_ref_designators'].duplicated()
        list_of_duplicates = []
        for index, item in enumerate(duplicated, start=0):
            if item == True:
                list_of_duplicates.append(input_bomA.loc[index]["split_ref_designators"])
        warnings.append("The following reference designators in bomB have duplicated entries: " + str(list_of_duplicates))
    
    if input_bomB['split_ref_designators'].duplicated().any():
        duplicated = input_bomB['split_ref_designators'].duplicated()
        list_of_duplicates = []
        for index, item in enumerate(duplicated, start=0):
            if item == True:
                list_of_duplicates.append(input_bomB.loc[index]["split_ref_designators"])
        warnings.append("The following reference designators in bomB have duplicated entries: " + str(list_of_duplicates))


# make sequence matcher function to use later
def apply_sequence_matcher(s, c1, c2): 
    return difflib.SequenceMatcher(None, s[c1], s[c2]).ratio()
        
#  Compare reference designators
def compare_Ref_Designators(warnings, input_bomA, input_bom_B):
    # check if missing
    merged_boms = input_bomA.merge(input_bom_B, how='inner', on="split_ref_designators", sort=True, suffixes=('_A', '_B'), copy=None, indicator=False, validate=None)
    in_bomA_not_in_bomB = ~input_bomA["split_ref_designators"].isin(merged_boms["split_ref_designators"])
    list_ref_dsg_not_in_bomB = []
    for index, item in enumerate(in_bomA_not_in_bomB, start=0): 
        if item == True:
            list_ref_dsg_not_in_bomB.append(input_bomA.loc[index]["split_ref_designators"])
    if len(list_ref_dsg_not_in_bomB) != 0:
        warnings.append("The following reference designators are in bomA but not in bomB: " + str(list_ref_dsg_not_in_bomB))

    in_bomB_not_in_bomA = ~input_bom_B["split_ref_designators"].isin(merged_boms["split_ref_designators"])
    list_ref_dsg_not_in_bomA = []
    for index, item in enumerate(in_bomB_not_in_bomA, start=0):
        if item == True:
            list_ref_dsg_not_in_bomA.append(input_bom_B.loc[index]["split_ref_designators"])
    if len(list_ref_dsg_not_in_bomA) != 0:
        warnings.append("The following reference designators are in bomB but not in bomA: " + str(list_ref_dsg_not_in_bomA))

    # check if stuff doesn't match
    merged_boms[["Description_A", "Description_B", "Manufacturer 1_A", "Manufacturer 1_B", "Manufacturer 1 part number_A", "Manufacturer 1 part number_B"]] = merged_boms[["Description_A", "Description_B", "Manufacturer 1_A", "Manufacturer 1_B", "Manufacturer 1 part number_A", "Manufacturer 1 part number_B"]].astype(str) 
    merged_boms['Description_match_ratio'] = merged_boms.apply(partial(apply_sequence_matcher, c1='Description_A', c2='Description_B'), axis=1)
    merged_boms['manufacturer1_match_ratio'] = merged_boms.apply(partial(apply_sequence_matcher, c1='Manufacturer 1_A', c2='Manufacturer 1_B'), axis=1)
    merged_boms['manufacturer1_part_number_match_ratio'] = merged_boms.apply(partial(apply_sequence_matcher, c1="Manufacturer 1 part number_A", c2="Manufacturer 1 part number_B"), axis=1)

    flagged_rows = []
    for index, item in enumerate(merged_boms['split_ref_designators'], start=0): 
        temp_index = merged_boms.index[merged_boms['split_ref_designators'] == item].tolist()
        if len(temp_index) == 1:
            if merged_boms.loc[temp_index]["Description_A"].tolist() != merged_boms.loc[temp_index]["Description_B"].tolist(): 
                warnings.append("description for " + str(item) + " doesn't match!")
                flagged_rows = flagged_rows + temp_index
            if merged_boms.loc[temp_index]["Quantity_A"].tolist() != merged_boms.loc[temp_index]["Quantity_B"].tolist(): 
                warnings.append("quantity for " + str(item) + " doesn't match!")
                flagged_rows = flagged_rows + temp_index
            if merged_boms.loc[temp_index]["Manufacturer 1_A"].tolist() != merged_boms.loc[temp_index]["Manufacturer 1_B"].tolist(): 
                warnings.append("manufacturer1 for " + str(item) + " doesn't match!")
                flagged_rows = flagged_rows + temp_index
            if merged_boms.loc[temp_index]["Manufacturer 1 part number_A"].tolist() != merged_boms.loc[temp_index]["Manufacturer 1 part number_B"].tolist():
                warnings.append("manufacturer1 part number for " + str(item) + " doesn't match!")
                flagged_rows = flagged_rows + temp_index
        if len(temp_index) > 1:
            flagged_rows = flagged_rows + temp_index
    flagged_rows = set(flagged_rows)
    flagged_rows = list(flagged_rows)
    flagged_merged_bom_rows = merged_boms.loc[flagged_rows]
    flagged_merged_bom_rows.drop(['index_A', 'original_index_A', "ref_dsg_position_A", 'index_B', 'original_index_B', "ref_dsg_position_B"], axis=1, inplace = True)
    flagged_merged_bom_rows = flagged_merged_bom_rows[['split_ref_designators', 'Description_A', 'Quantity_A', 'Manufacturer 1_A', 'Manufacturer 1 part number_A', 'Description_B', 'Quantity_B', 'Manufacturer 1_B', 'Manufacturer 1 part number_B', "Description_match_ratio", "manufacturer1_match_ratio", "manufacturer1_part_number_match_ratio"]]
    flagged_merged_bom_rows.rename(columns = {'split_ref_designators': 'Ref Dsg'}, inplace = True)
    return(flagged_merged_bom_rows)




# https://stackoverflow.com/questions/44798950/how-to-display-a-dataframe-in-tkinter - pandas table maybe useful
# https://www.youtube.com/watch?v=PgLjwl6Br0kS
# https://stackoverflow.com/questions/48358084/how-to-change-the-foreground-or-background-colour-of-a-selected-cell-in-tkinter
# https://github.com/Deagek/tableview/blob/main/README.md

# Note: uploading BOM > change header index does not update, you have to refresh by hitting upload bom

main()