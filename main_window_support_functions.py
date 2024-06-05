import pandas as pd
import numpy as np
from functools import partial
import difflib
import tkinter as tk

## Splits reference designators into individual rows 
# warnings: list to store warning messages for display
# input_bom: bom that needs to have ref designators split
# input_ref_dsg: name of reference designator colummn
# input description: name of description column
# input_manufacturer1: name of manufacturer 1 column
# input_manufacturer_part_number1: name of manufacturer part number column
# Returns: cleaned up bom, with reference designators split to their own row, and remove rows with missing reference designator

def splitRefDesignatorSeparateRows(warnings, input_bom, input_ref_dsg, input_description, input_quantity, input_manufacturer1, input_manufacturer_part_number1):
    input_bom_renamed = input_bom.rename(columns={input_ref_dsg: 'Ref Dsg', input_description: 'Description', input_quantity: 'Quantity', input_manufacturer1: 'Manufacturer', input_manufacturer_part_number1: 'Manufacturer Part Number'}, errors = 'raise')
    input_bom_no_na = input_bom_renamed.dropna(subset=['Ref Dsg'], inplace=False) # drop any rows that are missing reference designators
    input_bom_no_na = input_bom_no_na.fillna('<NA>') # replacing null values (floats) with certain string because trying to apply strimg methods down a column with float NAs makes it mad
    input_bom_no_na['Ref Dsg'] = input_bom_no_na['Ref Dsg'].str.replace(' ','') # get rid of any whitespace so that the next line splits cleanly

    # use regex to insert a comma only when numbers > letters (ABC123,ABC123). Removes an extra comma if there is already a comma there, and removes the trailing comma that it inserts.
    input_bom_no_na['Ref Dsg'] = input_bom_no_na['Ref Dsg'].astype(str)
    input_bom_no_na['Ref Dsg'] = input_bom_no_na['Ref Dsg'].str.replace(r'[a-zA-Z]+[0-9]+', r'\g<0>,', regex=True)
    input_bom_no_na['Ref Dsg'] = input_bom_no_na['Ref Dsg'].str.replace(',,', ',')
    input_bom_no_na['Ref Dsg'] = input_bom_no_na['Ref Dsg'].str[:-1]
    
    split_columns = input_bom_no_na['Ref Dsg'].str.split(',', expand=True) # splits to new columns on the comma
    ref_dsg_position = list(split_columns.columns.values)
    input_bom_no_na = pd.concat([input_bom_no_na, split_columns], axis=1) 

    input_bom_no_na['original_index'] = range(0, len(input_bom_no_na))
    # using pivot longer to reformat. Does lose any columns not listed here. Will screw up quantities, want to fix later.
    input_bom_no_na = pd.melt(input_bom_no_na, id_vars=['original_index', 'Description', 'Quantity', 'Manufacturer', 'Manufacturer Part Number'], value_vars = ref_dsg_position, value_name = 'split_ref_designators', var_name = 'ref_dsg_position') 
    input_bom_no_na = input_bom_no_na.sort_values(by = ['split_ref_designators'])
    input_bom_no_na.dropna(subset=['split_ref_designators'], inplace=True) 
    input_bom_no_na = input_bom_no_na.reset_index() # need to reset index for later comparisons
    return(input_bom_no_na)


## check if boms are exact match
# warnings: list to store warning messages for display
# input_bomA: one of the boms to be compared
# input_bomB: the other bom to be compared

def checkBomsExactMatch(warnings, input_bomA, input_bom_B): 
    if len(input_bomA) == len(input_bom_B):
        boms_exact_match = input_bomA == input_bom_B # will break if boms aren't same dimentions (which I think should never happen?)
        if (
            np.all(boms_exact_match['Description'] == True) 
            and np.all(boms_exact_match['Quantity'] == True) 
            and np.all(boms_exact_match['Manufacturer'] == True) 
            and np.all(boms_exact_match['Manufacturer Part Number'] == True) 
            and np.all(boms_exact_match['ref_dsg_position'] == True) 
            and np.all(boms_exact_match['split_ref_designators'] == True)
        ):
            warnings.append('bomA and bomB are exact matches')
        else:
            warnings.append('bomA and bomB do not match')

## check for dupolicate entries
# warnings: list to store warning messages for display
# input_bomA: one of the boms to be compared
# input_bomB: the other bom to be compared

def checkForDuplicates(warnings, input_bomA, input_bomB):
    # duplicates in bomA
    if input_bomA['split_ref_designators'].duplicated().any():
        duplicated = input_bomA['split_ref_designators'].duplicated()
        list_of_duplicates = []
        for index, item in enumerate(duplicated, start=0):
            if item == True:
                list_of_duplicates.append(input_bomA.loc[index]['split_ref_designators'])
        warnings.append('The following reference designators in bomA have duplicated reference designators: ' + str(list_of_duplicates))
    
    # duplicates in bomB
    if input_bomB['split_ref_designators'].duplicated().any():
        duplicated = input_bomB['split_ref_designators'].duplicated()
        list_of_duplicates = []
        for index, item in enumerate(duplicated, start=0):
            if item == True:
                list_of_duplicates.append(input_bomB.loc[index]['split_ref_designators'])
        warnings.append('The following reference designators in bomB have duplicated reference designators: ' + str(list_of_duplicates))


## make sequence matcher function to use below
# c1: column 1
# c2: column 2
# returns the ratio of match between column 1 and 2

def applySequenceMatcher(s, c1, c2): 
    return difflib.SequenceMatcher(None, s[c1], s[c2]).ratio()
        
## Compare reference designators
# warnings: list to store warning messages for display
# columns: list to store columns that need to be highlighted
# rows: list to store rows that need to be highlighted
# input_bomA: one of the boms to be compared
# input_bomB: the other bom to be compared

def compareRefDesignators(warnings, columns, rows, input_bomA, input_bom_B):
    # check if missing
    merged_boms = input_bomA.merge(input_bom_B, how='outer', on='split_ref_designators', sort=True, suffixes=('_A', '_B'), copy=None, indicator=False, validate=None)
    in_bomA_not_in_bomB = ~input_bomA['split_ref_designators'].isin(input_bom_B['split_ref_designators'])
    list_ref_dsg_not_in_bomB = []
    for index, item in enumerate(in_bomA_not_in_bomB, start=0): 
        if item == True:
            list_ref_dsg_not_in_bomB.append(input_bomA.loc[index]['split_ref_designators'])
    if len(list_ref_dsg_not_in_bomB) != 0:
        warnings.append('The following reference designators are in bomA but not in bomB: ' + str(list_ref_dsg_not_in_bomB))

    in_bomB_not_in_bomA = ~input_bom_B['split_ref_designators'].isin(input_bomA['split_ref_designators'])
    list_ref_dsg_not_in_bomA = []
    for index, item in enumerate(in_bomB_not_in_bomA, start=0):
        if item == True:
            list_ref_dsg_not_in_bomA.append(input_bom_B.loc[index]['split_ref_designators'])
    if len(list_ref_dsg_not_in_bomA) != 0:
        warnings.append('The following reference designators are in bomB but not in bomA: ' + str(list_ref_dsg_not_in_bomA))

    # make ratio of how much columns match 
    merged_boms[['Description_A', 'Description_B', 'Manufacturer_A', 'Manufacturer_B', 'Manufacturer Part Number_A', 'Manufacturer Part Number_B']] = \
        merged_boms[['Description_A', 'Description_B', 'Manufacturer_A', 'Manufacturer_B', 'Manufacturer Part Number_A', 'Manufacturer Part Number_B']].astype(str) 
    merged_boms['Desc_match_ratio'] = merged_boms.apply(partial(applySequenceMatcher, c1='Description_A', c2='Description_B'), axis=1)
    merged_boms['MFG_match_ratio'] = merged_boms.apply(partial(applySequenceMatcher, c1='Manufacturer_A', c2='Manufacturer_B'), axis=1)
    merged_boms['MPN_match_ratio'] = merged_boms.apply(partial(applySequenceMatcher, c1='Manufacturer Part Number_A', c2='Manufacturer Part Number_B'), axis=1)

    # two things are happening simultaneously below:
    # 1) flagged_rows is recording indexes from the full bom so that I can pull only the rows with mismatches out of it (contained in flagged_merged_bom_rows).
    # 2) "columns" and "rows" are recording the row and column numbers that need to get highlighted once flagged_merged_bom_rows is created.
    # tableview wants x and y coordinates for indicating each cell that gets highlighted, so temp_row holds on the x coordinate (or row number that the loop is on) while 
    # the correct y coordinates are added to "columns". This allows several pairs of columns to be highlighted in the same row. 
    # increment tells temp_row to increment by 1 only if something needs to get highlighted, and needs to get reset to 0 at the beginning of each loop.
    # this is because indexes for both the full bom and smaller bom are being collected at the same time.

    flagged_rows = []
    flagged_row_tracker = 0 
    for index, item in enumerate(merged_boms['split_ref_designators'], start=0): 
        index_tracker = merged_boms.index[merged_boms['split_ref_designators'] == item].tolist()
        increment = 0 
        if len(index_tracker) == 1:
            if merged_boms.loc[index_tracker]['Description_A'].tolist() != merged_boms.loc[index_tracker]['Description_B'].tolist(): 
                columns.extend([2, 6])
                rows.extend([flagged_row_tracker, flagged_row_tracker])
                flagged_rows = flagged_rows + index_tracker
                increment = 1
            if merged_boms.loc[index_tracker]['Quantity_A'].tolist() != merged_boms.loc[index_tracker]['Quantity_B'].tolist(): 
                columns.extend([3, 7])
                rows.extend([flagged_row_tracker, flagged_row_tracker])
                flagged_rows = flagged_rows + index_tracker
                increment = 1
            if merged_boms.loc[index_tracker]['Manufacturer_A'].tolist() != merged_boms.loc[index_tracker]['Manufacturer_B'].tolist(): 
                columns.extend([4, 8])
                rows.extend([flagged_row_tracker, flagged_row_tracker])
                flagged_rows = flagged_rows + index_tracker
                increment = 1
            if merged_boms.loc[index_tracker]['Manufacturer Part Number_A'].tolist() != merged_boms.loc[index_tracker]['Manufacturer Part Number_B'].tolist():
                columns.extend([5, 9])
                rows.extend([flagged_row_tracker, flagged_row_tracker])
                flagged_rows = flagged_rows + index_tracker
                increment = 1
        if len(index_tracker) > 1:
            flagged_rows = flagged_rows + index_tracker
            columns.extend(range(1, 13))
            rows.extend([flagged_row_tracker] * 12)
            increment = 1
        if increment == 1:
            flagged_row_tracker += 1
       
    flagged_rows = set(flagged_rows)
    flagged_rows = list(flagged_rows)
    flagged_rows.sort()
    print(flagged_rows)
    flagged_merged_bom_rows = merged_boms.loc[flagged_rows]
    flagged_merged_bom_rows.drop(['index_A', 'original_index_A', 'ref_dsg_position_A', 'index_B', 'original_index_B', 'ref_dsg_position_B'], axis=1, inplace = True)
    flagged_merged_bom_rows = flagged_merged_bom_rows[['split_ref_designators', 'Description_A', 'Quantity_A', 'Manufacturer_A', 'Manufacturer Part Number_A', 'Description_B', 'Quantity_B', 'Manufacturer_B', 'Manufacturer Part Number_B', 'Desc_match_ratio', 'MFG_match_ratio', 'MPN_match_ratio']]
    flagged_merged_bom_rows.rename(columns = {'split_ref_designators': 'Ref Dsg'}, inplace = True)
    pd.set_option('display.max_rows', None)
    return(flagged_merged_bom_rows)



    


# Note: uploading BOM > change header index does not update, you have to refresh by hitting upload bom