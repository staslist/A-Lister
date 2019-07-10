'''
MIT License

Copyright (c) 2019 Stanislav Listopad and Trina Norden-Krichmar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import os
import csv
import collections
from pathlib import Path
from CoreFunctionality import Translate_Name_To_Character
from CoreFunctionality import Match_Direction, Generate_Result_File
from CoreFunctionality import Inverse_Direction, Sign
from CoreFunctionality import Core_Computation, Write_Query_And_Result_List

class AListerDiffExprClass:
    # Constructor
    def __init__(self, input_data:dict, file_data:dict,
                 output_directory:str, output_delim:str, verbose:bool = False):
        self.output_directory = output_directory
        self.output_delim = output_delim
        
        self.query_d = collections.OrderedDict()
        self.query_s = ''
        self.dir_pcs = []
        
        self.current_vector_values = []
        
        self.input_data = input_data
        self.input_data_backup = input_data
        
        self.file_data = file_data
        self.file_data_backup = file_data
        
        self.result = []
        
        self.verbose = verbose
        
    def groupSelect(self):
        ''' Remove all pairwise comparisons not listed in the query from input data 
        and file data. '''
        grp_sel = []
        temp_dict = {}
        temp_subdict = {}
        temp_dict2 = {}
        for k in self.query_d.keys():
            k = k.replace('(', '')
            k = k.replace(')', '')
            k = k.split('-')
            for g_or_op in k:
                if((g_or_op not in ['FAND', 'AND', 'OR', 'DIFF'])
                    and ('$' not in g_or_op) and (g_or_op not in grp_sel)):
                    grp_sel.append(g_or_op)
        for key,value in self.input_data.items():
            if key in grp_sel:
                temp_dict[key] = value
                
        grp_sel2 = []
        for grp in grp_sel:
            index = grp.find(':')
            if(index != -1):
                if(grp[:index] not in grp_sel2):
                    grp_sel2.append(grp[:index])
            else:
                if(grp not in grp_sel2):
                    grp_sel2.append(grp)
        
        grp_sel2.append('HEADER-ROW')
        grp_sel2.append('ID-COLUMN')
        grp_sel2.append('DELIM')
        grp_sel2.append('DATA-TYPE')
        grp_sel2.append('DATA')
        for key,value in self.file_data.items():
            for k,v in value.items():
                if k in grp_sel2:
                    temp_subdict[k] = v
            temp_dict2[key] = temp_subdict
            temp_subdict = {}
                
        self.input_data = temp_dict 
        self.file_data = temp_dict2
        
    def filterFileDataByResult(self):
        ''' Filter DEEs in file data structure by the result list. 
        The file data dictionary is organized as follows:
        Each key is a name of a file. Each corresponding value is a dictionary.
        Each subdictionary has keys that are either HEADER-ROW, ID-COLUMN, DELIM,
        DATA-TYPE, DATA, or a non-directional pairwise comparison name. '''
        
        temp_dict = {}
        temp_subdict = {}
        temp_list = []
        for key,value in self.file_data.items():
            if(value['DATA-TYPE'] == 'DE-Sample'):
                id_col = value['ID-COLUMN']
                for k,v in value.items():
                    if(k in ['HEADER-ROW', 'DELIM']):
                        temp_subdict[k] = v
                    elif(k in ['ID-COLUMN', 'DATA-TYPE']):
                        pass
                    else:
                        for entity in v:
                            if(entity[id_col] in self.result):
                                temp_list.append(entity)
                        temp_subdict[k] = temp_list
                        temp_list = []
            elif(value['DATA-TYPE'] == 'DE-Series'):
                id_col = value['ID-COLUMN']
                for k,v in value.items():
                    if(k in ['HEADER-ROW', 'DELIM']):
                        temp_subdict[k] = v
                    elif(k in ['ID-COLUMN', 'DATA-TYPE']):
                        pass
                    elif(k == 'DATA'):
                        for entity in v:
                            if(entity[id_col] in self.result):
                                temp_list.append(entity)
                        temp_subdict[k] = temp_list
                        temp_list = []
                    else:
                        raise ValueError('An invalid key in the file data structure (DE-Series).')
            temp_dict[key] = temp_subdict
            temp_subdict = {}
            
        self.file_data = temp_dict
        
    def writeResDataList(self, folder_name:str):
        ''' Output the contents of file data structure into result file. '''
        os.makedirs(Path(self.output_directory)/"FilteredDEFiles"/folder_name, exist_ok=True)
        i = 0
        for key,value in self.file_data.items():
            delimeter = value['DELIM']
            
            f = open(Path(self.output_directory)/"FilteredDEFiles"/folder_name/("DEFile"+str(i)+".txt"), "w")
            f.write("File Path: " + str(key))
            f.write('\n')
            f.write("Query:     " + self.query_s)
            f.write('\n')
            f.write('\n')
            for k,v in value.items():
                if(k not in ['HEADER-ROW', 'DELIM']):
                    f.write("Number of rows in " + str(k) + ": " + "(" + str(len(v)) + ")")
                    f.write('\n')
            f.write('\n')
            
            j = 0
            for header in value['HEADER-ROW']:
                f.write(header)
                
                if(j < (len(value['HEADER-ROW'])-1)):
                    f.write(Translate_Name_To_Character(delimeter))
                    j = j + 1
            
            for k,v in value.items():
                if(k not in ['HEADER-ROW', 'DELIM']):
                    f.write('\n')
                    for row in v:
                        j = 0
                        for element in row:
                            f.write(element)
                
                            if(j < (len(row)-1)):
                                f.write(Translate_Name_To_Character(delimeter))
                                j = j + 1
                        f.write('\n')
            i = i + 1
            f.write('\n')
            f.close()     
        
    def correctDirectQueryAndInputData(self):
        ''' 1)Sync the names of pairwise comparisons between the query argument and input 
        data structure. 2)Add (filtered) directional pairwise comparisons to input data (ex: AA*AH:UP).
        3) Remove fold changes from input data.
        '''
        self.correctDirectQuery()
        self.filterAndExpandInputData()
        self.removeFoldChangesFromInputData()
        
    def correctDirectQuery(self)->dict:
        ''' Adjust the directional query in accordance to how data is formatted in the file(s).
        1)For example if AA*AH is provided in the query, but the paired comparison is listed 
        as AH*AA in the input delimited text file then change the listing to AH*AA in the query.
        2)For example if AA*AH:UP is provided in the query, but the directional paired comparison
        is listed as AH*AA in the input delimited text file then change the listing to AH*AA:DOWN
        in the query.
        3) If there is a paired comparison for which neither it nor its reverse are present 
        in the input data raise an error.
        '''
        corrected_query = collections.OrderedDict()
        directional_pcs = set()
        for sub_query in self.query_d.keys():
            adjusted_query = ''
            pc_and_opers = sub_query.split('-')
            for pc_or_oper in pc_and_opers:
                if(pc_or_oper not in ['AND', 'FAND', 'DIFF', 'OR']):
                    pc = pc_or_oper
                    index = pc.find('$')
                    # If this is a result ($) than we don't need to do anything with it.
                    if(index != -1):
                        adjusted_query += pc
                    else:
                        index = pc.find(':')
                        if(index == -1):
                            # 1) + 3)
                            adjusted_query = self.correctNonDirPairComp(pc, adjusted_query)
                        else:
                            # 2) + 3)
                            adjusted_query = self.correctDirPairComp(pc, adjusted_query,
                                                                     index, directional_pcs)
                else:
                    oper = pc_or_oper
                    adjusted_query += oper
                adjusted_query += '-'
            corrected_query[adjusted_query[:-1]] = self.query_d[sub_query]
        
        self.query_d = corrected_query
        self.dir_pcs = directional_pcs
    
    def correctNonDirPairComp(self, pc:str, adjusted_query:str):
        ''' Sync the non directional pairwise comparison name between query argument 
        and input data. ''' 
        grps = pc.split('*')
        reverse_pc = grps[-1] + '*' + grps[0]
        if(reverse_pc in self.input_data.keys()):
            adjusted_query += reverse_pc
        elif(pc in self.input_data.keys()):
            adjusted_query += pc
        else:
            raise ValueError("This paired comparison - ", str(pc), " - listed in the query ",
                             "was not found in the input files. \n All paired comparisons found ",
                             "in the input files: ", str(self.input_data.keys()))
            
        return adjusted_query
    
    def correctDirPairComp(self, pc:str, adjusted_query:str, index:int, directional_pcs:set):
        ''' Sync the directional pairwise comparison name between query argument 
        and input data. '''
        directional_pc = pc
        grps = directional_pc[:index]
        direction = directional_pc[index+1:]
        groups = grps.split('*')
        reverse_pc = groups[-1] + '*' + groups[0] 
        if(reverse_pc in self.input_data.keys()):
            reverse_directional_pc = reverse_pc + ':' + Inverse_Direction(direction)
            adjusted_query += reverse_directional_pc
            directional_pcs.add(reverse_directional_pc)
        elif(grps in self.input_data.keys()):
            adjusted_query += directional_pc
            directional_pcs.add(directional_pc)
        else:
            raise ValueError("This paired comparison - " + str(grps) + " - listed in the query " +
                             "was not found in the input files (post-filtering). \n All paired comparisons found " +
                             "in the input files: " + str(self.input_data.keys()) + ". Change the filter " +
                             "parameters or verify that the given pairwise comparison exists in the files. ")
        return adjusted_query
    
    def filterAndExpandInputData(self):
        '''
        1) Filter relevant paired comparisons based on provided directions. 
        2) Add directional paired comparisons to input data and return it.
        '''
        temp = {}
        for key,value in self.input_data.items():
            temp[key] = value
        for dpc in self.dir_pcs:
            index = dpc.find(':')
            grps = dpc[:index]
            direction = dpc[index+1:]
            values = self.input_data[grps]
            result = []
            for vector_value in values:
                if(Match_Direction(Sign(float(vector_value[1])), direction)):
                    result.append(vector_value)
            temp[dpc] = result
        self.input_data = temp
        
    def removeFoldChangesFromInputData(self):
        '''Each value in input data dictionary is a 2D list. Each sublist within 
        any given 2D list contains an entity name (index 0) and a fold change (index 1).
        This function flattens all 2D lists into 1D values by removing fold changes. '''
        temp = {}
        for key, two_dim_list in self.input_data.items():
            one_dim_list = []
            for two_dim_value in two_dim_list:
                one_dim_list.append(two_dim_value[0])
            temp[key] = one_dim_list
            
        self.input_data = temp
        
    # MAIN FUNCTION
    def compute(self, query_d_list:list, query_s_list)->list:
        ''' This function performs the set operations on input data and 
        outputs/returns the result(s). '''
        result_entity_name_lists = []
        result_data_lists = []
        
        # Creates a result.txt file in the output directory. 
        Generate_Result_File(self)
        
        i = 0
        for query_d in query_d_list:
            # DATA/QUERY PREPARATION SECTION
            
            # Sync the query with input data.
            # Add filtered directional paired comparisons to data.
            # Remove all fold changes from data.
            # Remove all paired comparisons that are not in the query from data.
            self.query_d = query_d
            self.query_s = query_s_list[i]
            self.correctDirectQueryAndInputData()
            self.groupSelect()
            
            if(self.verbose):
                print("The current query is: " + self.query_s)
            
            # CORE COMPUTATION SECTION
            
            # Perform the set operations on input data.
            # Obtain the result entity name list.
            Core_Computation(self)
            
            # OUTPUT SECTION
            # Write out the result entity name list and result differential expression 
            # data into the result.txt file. 
            
            # Write out entity name list into the result.txt file. 
            result_entity_name_lists.append(self.result)
            Write_Query_And_Result_List(self)
            
            # Use the result entity name list to filter the full differential expression data.
            self.filterFileDataByResult()
            
            # Write out the result differential expression data into the result.txt file. 
            result_data_lists.append(self.file_data)
            self.writeResDataList("Query" + str(i))
            
            # Reset all the relevant fields. 
            self.cleanUp()
            i = i + 1
        return result_entity_name_lists
    
    def cleanUp(self):
        self.input_data = self.input_data_backup
        self.file_data = self.file_data_backup
        self.current_vector_values = []
        self.result = []
    
# FILE INPUT PROCESSING FUNCTIONS 
def Read_And_Filter_DE_Files(input_files:list)->dict:
    ''' This functions reads in data from text delimited file(s) and merges it together. 
    It returns total input data. '''
    i = 0
    # Pairwise Comparison -> Entity names + fold changes.
    total_input_data = {}
    # Pairwise Comparison -> Entire row (entity name, fold change, p-value, etc...)
    total_file_data = {}
    while i < len(input_files):
        if(input_files[i].data_type == 'DE-Sample'):
            input_data, file_data = Read_Filter_DE_Sample_File(input_files[i].filename,
                                                  input_files[i].pc_map,
                                                  input_files[i].delimiter, 
                                                  input_files[i].id_col, 
                                                  input_files[i].sample1_col,
                                                  input_files[i].sample2_col, 
                                                  input_files[i].fc_cols,
                                                  input_files[i].filter_by_col_nums,
                                                  input_files[i].filter_by_col_cutoffs)
        elif(input_files[i].data_type == 'DE-Series'):
            input_data, file_data = Read_Filter_DE_Series_File(input_files[i].filename,
                                                  input_files[i].pc_map,
                                                  input_files[i].delimiter, 
                                                  input_files[i].id_col, 
                                                  input_files[i].fc_cols,
                                                  input_files[i].filter_by_col_nums,
                                                  input_files[i].filter_by_col_cutoffs)
        else:
            raise ValueError("Each differential expression must be DE-Sample or DE-Series type.")
        total_input_data.update(input_data)
        total_file_data[input_files[i].filename] = file_data
        i = i + 1
              
    return total_input_data, total_file_data

def Filter_DE_Series_Setup(pc_map:dict, filter_by_col_nums:list, 
                           filter_by_col_cutoffs:list)->dict:
    '''Merge these three parameters into one dictionary. (for a single file) '''
    result = {}
    result['ALL'] = []
    for key in pc_map.keys():
        result[key] = []
    
    i = 0
    for col_num in filter_by_col_nums:
        filt_dict = {}
        filt_dict[col_num] = filter_by_col_cutoffs[i]
        col_assigned_pc = False
        for key,values in pc_map.items():
            if(col_num in values):
                # Any given column can only belong to a single pairwise comparison
                result[key].append(filt_dict)
                col_assigned_pc = True
                break
        if(not col_assigned_pc):
            result['ALL'].append(filt_dict)
        i = i + 1
    return result

def Read_Filter_DE_Series_File(filename: str, pc_map:dict, delimiter:str,
                        id_cols:list, fc_cols:list, filter_by_col_nums:list,
                        filter_by_col_cutoffs:list)->'dict,dict':
    ''' This function reads in a DE-Series file and returns 1) a dictionary 
    that maps pairwise comparison names (ex: AA*AH, DA*AH, NF*AH, C*AH) to  
    lists containing entity names and fold changes (input_data). 
    2) a dictionary that contains header row, id column number, data type, 
    and file data.'''
    input_data = {}
    file_data = {}
    subresult = []
    subresult2 = []
    
    filt_map = Filter_DE_Series_Setup(pc_map, filter_by_col_nums, filter_by_col_cutoffs)
    
    id_col = id_cols[0]
    
    with open(Path(filename), newline='') as f:
        delim = ''
        if(delimiter == 'comma'):
            delim = ','
        elif(delimiter == 'tab'):
            delim = '\t'
        elif(delimiter == 'space'):
            delim = ' '
        elif(delimiter == 'colon'):
            delim = ':'
        elif(delimiter == 'semicolon'):
            delim = ';'
        else:
            raise ValueError('Invalid input delimiter: ', str(delimiter))
        reader = csv.reader(f,delimiter=delim)
        iter_rows = iter(reader)
        header = next(iter_rows)
        file_data['HEADER-ROW'] = header 
        file_data['ID-COLUMN'] = id_col
        file_data['DELIM'] = delimiter
        file_data['DATA-TYPE'] = 'DE-Series'
        
        for row in iter_rows:
            filter_pass_row = Filter_Row_Alt(row, filt_map['ALL'])
            row[id_col] = row[id_col].upper()
            i = 0
            if(filter_pass_row):
                for key,values in pc_map.items():
                    try:
                        float(values[0])
                    except ValueError:
                        continue
                    
                    filter_pass_pc = Filter_Row_Alt(row, filt_map[key])
                    if(not filter_pass_pc):
                        continue
                    
                    group_comparison_name = key
                    subresult.append(row[id_col])
                    subresult.append(row[values[0]])
                    try:
                        input_data[group_comparison_name].append(subresult)
                    except KeyError:
                        input_data[group_comparison_name] = []
                        input_data[group_comparison_name].append(subresult)
                    subresult = []
                    i = i + 1
                
                if(i > 0):  
                    # Only write this row if data from it was written into at least one 
                    # pairwise comparison. 
                    subresult2 = row
                    try:
                        file_data['DATA'].append(subresult2)
                    except KeyError:
                        file_data['DATA'] = []
                        file_data['DATA'].append(subresult2)
                    subresult2 = []
        if(len(input_data) == 0):
            raise ValueError("Error. The file: " + str(filename) +
                             " is either empty or all the rows have been filtered out.")
                
    return input_data, file_data

def Read_Filter_DE_Sample_File(filename: str, sample_label_map:dict, delimiter:str,
                        id_cols:list, sample1_cols:list, sample2_cols:list,
                        fc_cols:list, filter_by_col_nums:list, 
                        filter_by_col_cutoffs:list)->'dict,dict':
    ''' This function reads in a DE-Sample file and returns 1) a dictionary 
    that maps pairwise comparison names (ex: AA*AH, DA*AH, NF*AH, C*AH) to  
    lists containing entity names and fold changes (input_data). 
    2) a dictionary that maps pairwise comparison names to lists containing 
    entire rows from the input files (file_data).''' 
    input_data = {}
    file_data = {}
    subresult = []
    subresult2 = []
    
    id_col = id_cols[0]
    sample1_col = sample1_cols[0]
    sample2_col = sample2_cols[0]
    fc_col = fc_cols[0]
    
    with open(Path(filename), newline='') as f:
        delim = ''
        if(delimiter == 'comma'):
            delim = ','
        elif(delimiter == 'tab'):
            delim = '\t'
        elif(delimiter == 'space'):
            delim = ' '
        elif(delimiter == 'colon'):
            delim = ':'
        elif(delimiter == 'semicolon'):
            delim = ';'
        else:
            raise ValueError('Invalid input delimiter: ', str(delimiter))
        reader = csv.reader(f,delimiter=delim)
        iter_rows = iter(reader)
        header = next(iter_rows)
        file_data['HEADER-ROW'] = header 
        file_data['ID-COLUMN'] = id_col
        file_data['DELIM'] = delimiter
        file_data['DATA-TYPE'] = 'DE-Sample'
        i = 0
        for row in iter_rows:
            
            try:
                float(row[fc_col])
            except ValueError:
                continue
            
            filter_pass = Filter_Row(row, filter_by_col_nums,
                                               filter_by_col_cutoffs)
            row[id_col] = row[id_col].upper()
            if(filter_pass):
                i = i + 1
                try:
                    group_comparison_name = sample_label_map[row[sample1_col]] + '*' + sample_label_map[row[sample2_col]]
                except KeyError:
                    print("Filename: " + str(filename))
                    print("Warning. The value listed in the sample column is not listed in the sample mapping.")
                    print("Row #" + str(i) + '; Sample column1 value: ' + str(row[sample1_col]) 
                          + '; Sample column2 value: ' + str(row[sample2_col]))
                    print("This row will be ignored and will not be read in.")
                    print()
                    continue
            
                subresult.append(row[id_col])
                subresult.append(row[fc_col])
                try:
                    input_data[group_comparison_name].append(subresult)
                except KeyError:
                    input_data[group_comparison_name] = []
                    input_data[group_comparison_name].append(subresult)
                subresult = []
                
                subresult2 = row
                try:
                    file_data[group_comparison_name].append(subresult2)
                except KeyError:
                    file_data[group_comparison_name] = []
                    file_data[group_comparison_name].append(subresult2)
                subresult2 = []
    if(len(input_data) == 0):
        raise ValueError("Error. The file: " + str(filename) +
                         " is either empty or all the rows have been filtered out.")
    
    return input_data, file_data


def Filter_Row(row:list, filter_by_col_nums:list, filter_by_col_cutoffs:list):
    ''' Check whether the given row passes all of the user supplied filters. '''
    i = 0
    for col_num in filter_by_col_nums:
        cutoff_operator_determinant = filter_by_col_cutoffs[i][0]
        if(cutoff_operator_determinant == 'a'):
            cutoff_operator = filter_by_col_cutoffs[i][0:3]
            cutoff_value = filter_by_col_cutoffs[i][3:]
        else:
            cutoff_operator = filter_by_col_cutoffs[i][0:2]
            cutoff_value = filter_by_col_cutoffs[i][2:]
        filter_pass = Filter_Value(row[col_num], cutoff_operator, cutoff_value)
        if(filter_pass):
            pass
        else:
            return False
        i = i + 1
        
    return True

def Filter_Row_Alt(row:list, filter_by_col:list):
    ''' Check whether the given row passes all of the user supplied filters. '''
    for col in filter_by_col:
        for col_num, col_cutoff in col.items():
            cutoff_operator_determinant = col_cutoff[0]
            if(cutoff_operator_determinant == 'a'):
                cutoff_operator = col_cutoff[0:3]
                cutoff_value = col_cutoff[3:]
            else:
                cutoff_operator = col_cutoff[0:2]
                cutoff_value = col_cutoff[2:]
            filter_pass = Filter_Value(row[col_num], cutoff_operator, cutoff_value)
            if(filter_pass):
                pass
            else:
                return False
        
    return True

def Filter_Value(value:str, operator:str, cutoff:str)->bool:
    ''' Return true if the value passes the provided operator and cutoff combination. '''
    filter_pass = False
    try:
        if(operator == 'gt'):
            if (float(value) > float(cutoff)):
                filter_pass = True
        elif(operator == 'ge'):
            if (float(value) >= float(cutoff)):
                filter_pass = True
        elif(operator == 'agt'):
            if (abs(float(value)) > float(cutoff)):
                filter_pass = True
        elif(operator == 'age'):
            if (abs(float(value)) >= float(cutoff)):
                filter_pass = True
        elif(operator == 'lt'):
            if (float(value) < float(cutoff)):
                filter_pass = True
        elif(operator == 'le'):
            if (float(value) <= float(cutoff)):
                filter_pass = True
        elif(operator == 'alt'):
            if (abs(float(value)) < float(cutoff)):
                filter_pass = True
        elif(operator == 'ale'):
            if (abs(float(value)) <= float(cutoff)):
                filter_pass = True
        elif(operator == 'eq'):
            if (value == cutoff):
                filter_pass = True
        elif(operator == 'ne'):
            if (value != cutoff):
                filter_pass = True
        elif(operator == 'aeq'):
            if (abs(float(value)) == float(cutoff)):
                filter_pass = True
        elif(operator == 'ane'):
            if (abs(float(value)) != float(cutoff)):
                filter_pass = True
        
    except ValueError:
        pass
            
    return filter_pass