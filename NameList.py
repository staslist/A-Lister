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

import csv
import collections
from pathlib import Path
from CoreFunctionality import Core_Computation, Generate_Result_File 
from CoreFunctionality import Write_Query_And_Result_List

# MECHANICS (MODEL) FUNCTIONS

class AListerNameListClass:
    # Constructor
    def __init__(self, input_data:list, output_directory:str, output_delim:str, verbose:bool = False):
        self.output_directory = output_directory
        self.output_delim = output_delim
    
        self.query_d = collections.OrderedDict()
        self.query_s = ''
        
        self.input_data = input_data
        self.input_data_backup = input_data
          
        self.current_vector_values = []
        
        # Outputs
        self.result = []
        
        # Other Parameters
        self.verbose = verbose
        
    def groupSelect(self):
        grp_sel = []
        temp_dict = {}
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
                
        self.input_data = temp_dict

    # MAIN FUNCTION
    def compute(self, query_d_list:list, query_s_list:list)->'Union, Intersection, Fuzzy Intersection, and Difference':
        ''' This function performs the set operations on input data and returns the final result. '''
        results = []
        
        Generate_Result_File(self)
        i = 0
        for query_d in query_d_list:
        
            self.query_d = query_d
            self.query_s = query_s_list[i]
            self.groupSelect()
            
            Core_Computation(self)
            
            Write_Query_And_Result_List(self)
            
            results.append(self.result)
            self.cleanUp()
            
        return results
        
    def cleanUp(self):
        self.input_data = self.input_data_backup
        self.current_vector_values = []
        self.result = []
             
# INPUT PROCESSING FUNCTIONS    
def Merge_Name_List_Files_Data(input_files:list)->"Multiple Lists":
    ''' This functions reads in data from multiple name (>= 1) files and merges it together. '''
    i = 0
    total_input_data = {}
    while i < len(input_files):
        filename = input_files[i].filename
        input_data  = Read_In_Name_Lists_Files(filename, input_files[i].delimiter)
        total_input_data.update(input_data)
        i = i + 1
    return total_input_data
    
def Read_In_Name_Lists_Files(filename: str, delimiter:str)->dict:
    ''' This function reads in a comma delimited file containing names + and returns 
    a dictionary that maps groups to name lists. ''' 
    input_data = {}
    
    with open(Path(filename), newline='') as f:
        delim = ''
        if(delimiter == 'comma'):
            delim = ','
        elif(delimiter == 'tab'):
            delim = '\t'
        reader = csv.reader(f,delimiter=delim)
            
        header = True
        header_length = 0
        result = []
        group_names = []
        for row in reader:
            if(header):
                header_length = len(row)
                for group_name in row:
                    group_names.append(group_name)
                    result.append([])
                header = False
            elif(row):
            # This checks that the row is not an empty list.
                if(len(row) > header_length):
                    raise ValueError("The number of values in a value row is larger than the number of " +
                                     "values in the header row.")
                j = 0
                for value in row:
                    if(value):
                        result[j].append(value.upper())
                    j = j + 1
        i = 0
        for group_name in group_names:   
            input_data[group_name] = result[i]
            i = i + 1
          
    return input_data


