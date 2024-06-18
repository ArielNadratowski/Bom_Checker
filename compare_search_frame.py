import tkinter as tk

class CompareSearchFrame:
    def __init__(self, position, compare_button_coords = [0, 0], search_coords  = [2, 0], compare_button_columnspan = 2, padx_ = 10, pady_ = 10, search_input_height = 1, search_input_width = 10):
        # set up frame for compare and search bom buttons
        compare_search_frame = tk.Frame()
        compare_search_frame.pack(side = position)

        # compare bom button
        compare_button = tk.Button(compare_search_frame, text = 'COMPARE BOMs')
        compare_button.grid(row = compare_button_coords[0], column = compare_button_coords[1], columnspan = compare_button_columnspan, padx = padx_, pady = pady_)

        # search bom button 
        search_button = tk.Button(compare_search_frame, text = 'Search Ref Dsg')
        search_button.grid(row = search_coords[0], column = search_coords[1], padx = padx_, pady = pady_)
        search_input = tk.Text(compare_search_frame, height = search_input_height, width = search_input_width)
        search_input.grid(row = search_coords[0], column = search_coords[1] + 1, padx = padx_, pady = pady_)



 





    # def compare_boms(self):
    #     if self.bomA_status == 1 and self.bomB_status == 1: # want: make this throw an error if this doesn't evaluate
    #         warnings_row = []
    #         warnings_list = []
    #         highlight_column_numbers = []
    #         highlight_row_numbers = []

    #         restructured_bomA = main_window_support_functions.split_reference_designator_separate_rows(warnings_list, self.bomA, self.ref_dsgA, self.descA, self.quantA, self.manuA, self.mpnA)
    #         restructured_bomB = main_window_support_functions.split_reference_designator_separate_rows(warnings_list, self.bomB, self.ref_dsgB, self.descB, self.quantB, self.manuB, self.mpnB)
            
    #         main_window_support_functions.check_boms_exact_match(warnings_list, restructured_bomA, restructured_bomB)    
    #         main_window_support_functions.check_for_duplicates(warnings_list, restructured_bomA, restructured_bomB)
    #         flagged_rows_temp_storage = main_window_support_functions.compare_reference_designators(warnings_list, highlight_column_numbers, highlight_row_numbers, restructured_bomA, restructured_bomB)

    #         tableview.clear()

    #         # fill in table
    #         number_rows = len(flagged_rows_temp_storage.index)
    #         for i in range(number_rows):
    #             column_number = 0
    #             row_as_list = flagged_rows_temp_storage.iloc[i].tolist()
    #             for item in row_as_list:
    #                 tableview.insert_item(column_number, text = item)
    #                 column_number += 1
            
    #         # highlight cells that are different
    #         for c, r in zip(highlight_column_numbers, highlight_row_numbers):
    #             tableview.highlight_cell(column = c, row = r, bg = 'yellow', fg = 'red')
            
    #         # show warnings
    #         for widgets in self.warnings_frame.winfo_children():
    #             widgets.destroy()
    #         for index, value in enumerate(warnings_list):
    #             warnings_row.append(ttk.Label(self.warnings_frame, text = value, foreground = 'red'))
    #             warnings_row[index].grid()

    #         # probably best place to stick this due to scoping
    #         self.merged_boms = restructured_bomA.merge(restructured_bomB, how='outer', on='split_ref_designators', sort=True, suffixes=('_A', '_B'), copy=None, indicator=False, validate=None)
    #         self.merged_boms.drop(['index_A', 'original_index_A', 'ref_dsg_position_A', 'index_B', 'original_index_B', 'ref_dsg_position_B'], axis=1, inplace = True)
    #         self.merged_boms = self.merged_boms[['split_ref_designators', 
    #                                              'Description_A', 'Quantity_A', 'Manufacturer_A', 'Manufacturer Part Number_A', 
    #                                              'Description_B', 'Quantity_B', 'Manufacturer_B', 'Manufacturer Part Number_B']]
    #         self.merged_boms.rename(columns = {'split_ref_designators': 'Ref Dsg'}, inplace = True)
    #         col = self.merged_boms.pop('Ref Dsg')
    #         self.merged_boms.insert(0, col.name, col)


    # def search_reference_designator(self):
    #     tableview.clear()

    #     search_text = self.search_input.get('1.0', 'end')
    #     search_text = search_text.strip()

    #     self.merged_boms['Ref Dsg'] = self.merged_boms['Ref Dsg'].str.strip()

    #     searched_rows = self.merged_boms[self.merged_boms['Ref Dsg'] == search_text]

    #     # fill in table 
    #     number_rows = len(searched_rows.index)
    #     for i in range(number_rows):
    #         column_number = 0
    #         row_as_list = searched_rows.iloc[i].tolist()
    #         for item in row_as_list:
    #             tableview.insert_item(column_number, text = item)
    #             column_number += 1

