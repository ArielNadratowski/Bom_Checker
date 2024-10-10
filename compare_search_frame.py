import tkinter as tk
import numpy as np
import pandas as pd
from functools import reduce
import highlight_error
import difflib

class CompareSearchFrame:
    def __init__(self, frame_holding_boms, position, compare_button_coords = [0, 0], search_coords  = [2, 0], padx_ = 10, pady_ = 10, search_input_height = 1, search_input_width = 10):
        # set up frame for compare and search bom buttons
        compare_search_frame = tk.Frame()
        compare_search_frame.pack(side = position)

        # place to hold highlight errors list and dataframe
        self.highlight_error_list = []
        self.highlight_error_dataframe = None

        # compare bom button
        compare_button = tk.Button(compare_search_frame, text = 'COMPARE BOMs', command = lambda: self.compare_boms(frame_holding_boms, self.highlight_error_list))
        compare_button.grid(row = compare_button_coords[0], column = compare_button_coords[1], padx = padx_, pady = pady_)

        # clear boms button
        clear_boms = tk.Button(compare_search_frame, text = 'CLEAR BOMs', foreground = 'red')
        clear_boms.grid(row = compare_button_coords[0], column = compare_button_coords[1] + 1, padx = padx_, pady = pady_)

        # search bom button 
        search_button = tk.Button(compare_search_frame, text = 'Search Ref Dsg')
        search_button.grid(row = search_coords[0], column = search_coords[1], padx = padx_, pady = pady_)
        search_input = tk.Text(compare_search_frame, height = search_input_height, width = search_input_width)
        search_input.grid(row = search_coords[0], column = search_coords[1] + 1, padx = padx_, pady = pady_)


    def test(self, frame_holding_boms):
        print(frame_holding_boms.boms[0].selected.get())
        print(frame_holding_boms.boms[1].selected.get())

    def compare_boms(self, frame_holding_boms):
        # filter for selected dataframes only
        selected_boms = []
        for bom in frame_holding_boms.boms:
            if bom.selected.get() == 1:
                selected_boms.append(bom)
        # check for duplicates
        self.check_for_duplicates(selected_boms)
        # check for missing reference designators
        self.check_missing_reference_designators(selected_boms)
        # check for differences between reference designator rows (different manufacturer, etc)
        self.compare_reference_designators(selected_boms)



                    


#             main_window_support_functions.check_boms_exact_match(warnings_list, restructured_bomA, restructured_bomB)    
#             main_window_support_functions.check_for_duplicates(warnings_list, restructured_bomA, restructured_bomB)
#             flagged_rows_temp_storage = main_window_support_functions.compare_reference_designators(warnings_list, highlight_column_numbers, highlight_row_numbers, restructured_bomA, restructured_bomB)

#             tableview.clear()

#             # fill in table
#             number_rows = len(flagged_rows_temp_storage.index)
#             for i in range(number_rows):
#                 column_number = 0
#                 row_as_list = flagged_rows_temp_storage.iloc[i].tolist()
#                 for item in row_as_list:
#                     tableview.insert_item(column_number, text = item)
#                     column_number += 1
            
#             # highlight cells that are different
#             for c, r in zip(highlight_column_numbers, highlight_row_numbers):
#                 tableview.highlight_cell(column = c, row = r, bg = 'yellow', fg = 'red')
            
#             # show warnings
#             for widgets in self.warnings_frame.winfo_children():
#                 widgets.destroy()
#             for index, value in enumerate(warnings_list):
#                 warnings_row.append(ttk.Label(self.warnings_frame, text = value, foreground = 'red'))
#                 warnings_row[index].grid()

#             # probably best place to stick this due to scoping
#             self.merged_boms = restructured_bomA.merge(restructured_bomB, how='outer', on='split_ref_designators', sort=True, suffixes=('_A', '_B'), copy=None, indicator=False, validate=None)
#             self.merged_boms.drop(['index_A', 'original_index_A', 'ref_dsg_position_A', 'index_B', 'original_index_B', 'ref_dsg_position_B'], axis=1, inplace = True)
#             self.merged_boms = self.merged_boms[['split_ref_designators', 
#                                                  'Description_A', 'Quantity_A', 'Manufacturer_A', 'Manufacturer Part Number_A', 
#                                                  'Description_B', 'Quantity_B', 'Manufacturer_B', 'Manufacturer Part Number_B']]
#             self.merged_boms.rename(columns = {'split_ref_designators': 'Ref Dsg'}, inplace = True)
#             col = self.merged_boms.pop('Ref Dsg')
#             self.merged_boms.insert(0, col.name, col)


    def check_for_duplicates(self, selected_boms):
        for bom in selected_boms:
            if bom.bom_dataframe['split_ref_designators'].duplicated().any():
                duplicated = bom.bom_dataframe['split_ref_designators'].duplicated()
                list_of_duplicates = []
                for index, item in enumerate(duplicated, start=0):
                    if item == True:
                        list_of_duplicates.append(bom.bom_dataframe.loc[index]['split_ref_designators'])
                for item in list_of_duplicates:
                    message = 'There are duplicates of ' + str(item) + ' in ' + bom.name
                    highlight_error_item = highlight_error.HighlightError(item, message, 'duplicate', None) # using None to indicate entire row gets highlighted for right now
                    self.highlight_error_list.append(highlight_error_item)

    def check_missing_reference_designators(self, selected_boms):
        list_of_reference_designator_lists = []
        for bom in selected_boms:
            list_of_reference_designator_lists.append(bom.bom_dataframe['split_ref_designators'].to_list())
        key_as_list = []
        for list in list_of_reference_designator_lists:
            for reference_designator in list:
                if reference_designator not in key_as_list:
                    key_as_list.append(reference_designator)
        key = set(key_as_list)
        # key is now a set of all possible reference designators

        for index, list in enumerate(list_of_reference_designator_lists):
            missing_reference_designators = set(key).difference(list)
            for reference_designator in missing_reference_designators:
                message = str(reference_designator) + ' is missing from ' + str(selected_boms[index].name) # depends on the index staying consistent between selected_boms and list_of_reference_designator_lists, which I think should be the case
                highlight_error_item = highlight_error.HighlightError(reference_designator, message, 'missing', None) # using None to indicate entire row gets highlighted for right now
                self.highlight_error_list.append(highlight_error_item)

    ## Compare reference designators

    def compare_reference_designators(self, selected_boms):
        selected_bom_dataframes = []
        selected_bom_names = []
        for bom in selected_boms:
            bom_drop_quantity = bom.bom_dataframe.drop(bom.bom_dataframe.columns[3], axis=1, inplace=False) # drop quantity column because the way it currently is isn't useful TODO: add a function to check quantity somehow (probably count duplicates in Description?)
            bom_drop_quantity.columns = bom_drop_quantity.columns.map(lambda x : x + '_' + str(bom.name) if x !='split_ref_designators' else x)  # need to rename columns besides split_ref_designators to prevent merge error later
            selected_bom_dataframes.append(bom_drop_quantity)
            selected_bom_names.append(bom.name)

        all_boms_merged = reduce(lambda  left,right: pd.merge(left,right,on=['split_ref_designators'],
                                            how='outer'), selected_bom_dataframes)
        
        # do some cleaning so that it will be in the same format as will be shown in the highlight errors frame
        all_boms_merged = all_boms_merged[['split_ref_designators'] + [ col for col in all_boms_merged.columns if col != 'split_ref_designators' ]] # pull split_ref_designators to front of dataframe
        all_boms_merged = all_boms_merged.loc[:, ~(all_boms_merged.columns.str.startswith('index')|all_boms_merged.columns.str.startswith('original_index')|all_boms_merged.columns.str.startswith('ref_dsg_position'))] # drop some additional columns that aren't useful
        print(all_boms_merged)

        for index, reference_designator in enumerate(all_boms_merged['split_ref_designators'], start= 0): # will iterate down the rows of merged boms
            for i in range(0, len(selected_bom_names)): # using this to compare coresponding columns (description1 index vs description2 index, description1 index vs description3 index...) First bom will be the comparison bom for sake of simplicity
                self.compare_columns(all_boms_merged, index, selected_bom_names, reference_designator, self.highlight_error_list, i, 1, 'description')
                self.compare_columns(all_boms_merged, index, selected_bom_names, reference_designator, self.highlight_error_list, i, 2, 'maufacturer')
                self.compare_columns(all_boms_merged, index, selected_bom_names, reference_designator, self.highlight_error_list, i, 3, 'manufacturer part number')

        # make highlight_error_dataframe
        self.make_highlight_error_dataframe(all_boms_merged)

    def make_highlight_error_dataframe(self, all_boms_merged):
        # compile list of all ref dsg in highlight error list and pull from all_boms_merged
        reference_designators_with_errors = []
        for item in self.highlight_error_list:
            reference_designators_with_errors.append(item.reference_designator)
        reference_designators_with_errors_set = set(reference_designators_with_errors)
        self.highlight_error_dataframe = all_boms_merged[all_boms_merged['split_ref_designators'].isin(reference_designators_with_errors_set)]

    def compare_columns(self, all_boms_merged, index, selected_bom_names, reference_designator, place_storing_highlight_errors, loop_iteration, reference_column_index, category_name):
        if all_boms_merged.loc[index][reference_column_index].tolist() != all_boms_merged.loc[index][1 + loop_iteration*3].tolist():
            message = str(selected_bom_names[loop_iteration + 1]) + ' ' + str(category_name) + ' for ' + str(reference_designator) + ' does not match ' + str(selected_bom_names[0])
            highlight_error_item = highlight_error.HighlightError(reference_designator, message, str(category_name) + ' discrepancy', [reference_column_index, 1 + loop_iteration*3])
            place_storing_highlight_errors.append(highlight_error_item)


