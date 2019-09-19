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

#raise ValueError(message)
import sys
import csv
import os
import collections
from pathlib import Path

class Logger(object):
    def __init__(self, output_directory:str):
        self.terminal = sys.stdout
        os.makedirs(Path(output_directory), exist_ok=True)
        self.log = open(Path(output_directory)/"data_dump.txt", "w")
        
    def __del__(self):
        #print("The logger deconstructor has been called!")
        # Currently stdout points to the logger.
        # Undo this by pointing stdout back to terminal.
        sys.stdout = self.terminal
        
    def manualDel(self):
        #print("Logger reset stdout to point to terminal.")
        sys.stdout = self.terminal
    
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        
    def flush(self):
        pass

class InputFile:
    def __init__(self, filename:str, data_type:str, delimiter:str,
                 id_column=[], fc_columns=[], sample1_column=[], sample2_column=[],
                 filter_by_col_nums = [], filter_by_col_cutoffs = [], pc_map:dict={}):
        # These parameters must be provided for every input file (name, data type, file type, and 
        # group label map.
        self.filename = filename
        self.data_type = data_type
        self.delimiter = delimiter
        
        # The column parameters are used with differential expression files only.
        self.pc_map = pc_map
        self.id_col = id_column
        self.fc_cols = fc_columns
        self.sample1_col = sample1_column
        self.sample2_col = sample2_column
        self.filter_by_col_nums = filter_by_col_nums
        self.filter_by_col_cutoffs = filter_by_col_cutoffs
        
    def __repr__(self):
        f = 'File Info:\n' + 'Filename: ' + str(self.filename) + '\n'
        dt = "Data Type: " + str(self.data_type) + '\n'
        d = "Delimiter: " + str(self.delimiter) + '\n'
        pcm = "Pairwise comparison map: " + str(self.pc_map) + '\n'
        icn = "Id column number: " + str(self.id_col) + '\n'
        fcn = "Fold change column number(s): " + str(self.fc_cols) + '\n'
        s1cn = "Sample 1 column number: " + str(self.sample1_col) + '\n'
        s2cn = "Sample 2 column number: " + str(self.sample2_col) + '\n'
        fbcn = "Filter by column numbers: " + str(self.filter_by_col_nums) + '\n'
        fbcc = "Filter by column cutoffs: " + str(self.filter_by_col_cutoffs) + '\n'
        return (f + dt + d + pcm + icn + fcn + s1cn + s2cn + fbcn + fbcc)
        
def Process_User_Input(args)-> 'mandatory, module specific, and general parameters':
    ''' This method parses user input provided via command-line and 
    returns a list of InputFile objects and a dictionary of other parameters.'''  
    # This dictionary contains all the parameters that are non-file specific.
    # All file specific parameters are organized in a list of InputFile objects.
    parameters = {}    
    input_files = []
    
    comp_type = args.comparison_type[0]
    files = args.input_file
    Verify_Files_Exist(files)
            
    num_files = len(files)
    inp_delim = Expand_File_Arg_To_Match_Num_Files(args.id, num_files)
    
    o = args.o[0]
    od = args.od[0]
    
    v = bool(args.v)
    
    logger = Logger(o)
    sys.stdout = logger
    
    if(v):
        print()
        print("USER INPUT (ECHO): ")
        for ele in sys.argv:
            print(ele, end = ' ')
        print()
        print()
        print("USER INPUT (CLI ARGS): ")
        print(args) 
    
    if(comp_type == 'name-list'):
        query = args.query
        pc_sel = Get_Grp_Sel_From_Query(query[0])
        query_str_list = query
        query = Process_Query_Arg(query[0])
        query_dict_list = [query]
        
        data_types = []
        i = 0
        while i < num_files:
            data_types.append('name-list')
            i = i + 1
            
        i = 0
        while i < num_files:
            input_files.append(InputFile(files[i], data_types[i], inp_delim[i]))
            i = i + 1
    elif(comp_type == 'diff-expression'):
        query = args.dq
        pc_sel = Get_Grp_Sel_From_Query(query[0])
        query_str_list = Process_Query_ALL_Directions(query[0])
        query_dict_list = []
        for q in query_str_list:
            query = Process_Query_Arg(q)
            query_dict_list.append(query)
        
        sample1_col = Expand_File_Arg_To_Match_Num_Files(args.s1, num_files)
        sample2_col = Expand_File_Arg_To_Match_Num_Files(args.s2, num_files)
        fc_cols = Expand_File_Arg_To_Match_Num_Files(args.fc, num_files)
        id_col = Expand_File_Arg_To_Match_Num_Files(args.n, num_files)
        filter_by_col = Expand_File_Arg_To_Match_Num_Files(args.f, num_files)
    
        headers = Extract_File_Headers(files, inp_delim, num_files)
        
        if(v):
            print()
            print("File Headers: ", headers)
            print()
        
        filter_by_col_nums, filter_by_col_cutoffs = Process_Filter_Arg(filter_by_col,headers,num_files)
        data_types = Generate_DE_Data_Types(sample1_col)
        
        sample1_col = Process_Col_Header_Arg(sample1_col, 'Sample1', headers)
        sample2_col = Process_Col_Header_Arg(sample2_col, 'Sample2', headers)
        pc_maps = Process_PC_Map_Arg(args.pc, data_types, num_files, headers, fc_cols)
        id_col = Process_Col_Header_Arg(id_col, 'ID', headers)
        fc_cols = Process_Col_Header_Arg(fc_cols, 'Fold Change', headers)
        
        Check_Query_And_PC_Map_Consistency(pc_maps, pc_sel, data_types)
        
        i = 0
        while i < num_files:
            in_file = InputFile(files[i], data_types[i], inp_delim[i],
                               id_col[i], fc_cols[i], sample1_col[i], sample2_col[i],
                               filter_by_col_nums[i], filter_by_col_cutoffs[i], pc_maps[i])
            input_files.append(in_file)
            i = i + 1
            if(v):
                print(in_file)
                print()
    else:
        raise ValueError("Comparison type must be name-list or diff-expression.")
    
    Verify_Query_D_And_S(query_dict_list, query_str_list)
    
    parameters['query_d_list'] = query_dict_list
    parameters['query_s_list'] = query_str_list
    parameters['comp_type'] = comp_type
    parameters['out_delim'] = od
    parameters['out_dir'] = o
    parameters['v'] = v
    
    parameters['logger'] = logger

    return parameters, input_files

def Verify_Files_Exist(files:list):
    for file in files:
        if(not Path(file).is_file()):
            raise ValueError("File: " + str(file) + " does not exist.")

def Expand_File_Arg_To_Match_Num_Files(column:list, num_files:int)->list:
    ''' If the input file argument (other than sample mapping) is listed once, 
    (ex: input delimiter), but there are multiple input files than assume that all input files share 
    this argument. Number of files will be at least 1, guaranteed by the CLI. '''
    if(num_files < 1):
        raise ValueError("The number of files cannot be < 1.")
    if(len(column) == 1 and num_files!= 1):
        while len(column) < num_files:
            column.append(column[0])
    else:
        pass
    return column

def Get_Grp_Sel_From_Query(query:str)->list:
    grp_oper_sel = query.replace('(','')
    grp_oper_sel = grp_oper_sel.replace(')','')
    grp_oper_sel = grp_oper_sel.split('-')
    grp_sel = set()
    for group_or_operator in grp_oper_sel:
        if group_or_operator not in ['AND', 'FAND', 'OR', 'DIFF']:
            grp_sel.add(group_or_operator)
            
    return grp_sel

def Process_Query_ALL_Directions(query:str)->list:
    ''' The queries containing any ALL directions need to be translated 
    into multiple non-ALL queries. '''
    queries = [query]
    temp = []
    num_all = query.count('ALL')
    if(num_all == 0):
        return [query]
    else:
        i = 0
        while i < num_all:
            for query in queries:
                index = query.find('ALL')
                up_query = query.replace('ALL', 'UP', 1)
                down_query = query.replace('ALL', 'DOWN', 1)
                temp.append(up_query)
                temp.append(down_query)
            queries = temp
            temp = []
            i = i + 1
               
    return queries
                
def Process_Query_Arg(query:str)->'ordered_dict':
    ''' This function transforms a string query into a dictionary 
    that represents a set of equations. The keys represent the 
    left hand side of the equation and values represent the right 
    hand side of the equation. ''' 
    # Process query.
    
    # ((A*B-AND-B*C)-DIFF-(A*B-OR-(B*C-AND-A*C)))
    # ^^           >      ^       ^           >>>
    # {1:13,28:40,20:41,0:42} <- parens
    # [2,3,2,1] <- depths
    # R1:B*C-AND-A*C,R2:A*B-OR-R1,R3:A*B-AND-B*C,R4:R3-DIFF-R2 <- results
    # A*B-AND-B*C = R1
    # B*C-AND-A*C = R2
    # A*B-OR-R2 = R3
    # R1-DIFF-R3 = R4
    
    if(query.count('(') != query.count(')')):
        raise ValueError("Unbalanced parenthesis.")
    query = '(' + query + ')'
    
    # Indices of all open parenthesis
    open_parens = []
    # Indices of all close parenthesis
    close_parens = []
    # The parenthesis depth level of each character
    depths = []
    # Maximum parenthesis depth
    max_depth = 0
    # Indices of matched parenthesis (key = index of open parenthesis, value = index of close parenthesis)
    parens = {}
    results_d = collections.OrderedDict()
    results_l = []
    dec_max_depth = False
    i = 0
    r = 1
    for char in query:
        if(dec_max_depth):
            max_depth = max_depth - 1
            dec_max_depth = False
        if(char == '('):
            open_parens.append(i)
            max_depth = max_depth + 1
        elif(char == ')'):
            close_parens.append(i)
            if(max_depth > 0):
                dec_max_depth = True
                close_parens.append(i)
                open_paren_index = open_parens.pop()
                close_paren_index = close_parens.pop()
                parens[open_paren_index]=close_paren_index
                result = query[open_paren_index:close_paren_index+1]
                result_name = '$' + str(r)
                if(len(results_d) > 0):
                    for res in results_l:
                        if(res in result):
                            result = result.replace(res, results_d[res])
                results_d[result] = result_name
                results_l.append(result)
                depths.append(max_depth)
                r = r + 1
            else:
                raise ValueError("Unbalanced parenthesis.")
        i = i + 1    
        
    query_d = collections.OrderedDict() 
    for k,value in results_d.items():
        k = k.replace('(', '')
        k = k.replace(')', '')
        query_d[k] = value
            
    return query_d

def Extract_File_Headers(files:list, inp_delim:list, num_files:int)->list:
    ''' Returns a 2D list of file headers'''
    headers = []
    i = 0
    while i < num_files:
        filename = files[i]
        with open(Path(filename), newline='') as f:
            delim = ''
            if(inp_delim[i] == 'comma'):
                delim = ','
            elif(inp_delim[i] == 'tab'):
                delim = '\t'
            elif(inp_delim[i] == 'space'):
                delim = ' '
            elif(inp_delim[i] == 'semicolon'):
                delim = ';'
            elif(inp_delim[i] == 'colon'):
                delim = ':'
            reader = csv.reader(f,delimiter=delim)
            for row in reader:
                headers.append(row)
                break
        i = i + 1
    return headers

def Process_Filter_Arg(filter_by_col:list, headers:list, num_files:int)->'list, list':
    ''' This function returns two 2D lists. Each sub-list contains the column numbers for all 
    filter columns in that file and their respective cutoffs. '''
    filter_by_col_numbers = []
    filter_by_col_cutoffs = []
    if(filter_by_col[0] == None):
        i = 0
        while i < num_files:
            filter_by_col_numbers.append([])
            filter_by_col_cutoffs.append([])
            i = i + 1
        return filter_by_col_numbers, filter_by_col_cutoffs
    
    i = 0
    for filter_by_columns in filter_by_col:
        if(filter_by_columns == "NONE"):
            filter_by_col_numbers.append([])
            filter_by_col_cutoffs.append([])
            continue
        
        filt_by_col = filter_by_columns.split(',')
        filter_column_cutoffs_file = []
        filter_by_col_numbers_file = []
        for fbc in filt_by_col:
            colon_index = fbc.find(':')
            name = fbc[:colon_index]
            cutoff = fbc[colon_index+1:]
            
            # Check the filter operator for validity. 
            cutoff_operator_determinant = cutoff[0]
            if(cutoff_operator_determinant == 'a'):
                cutoff_operator = cutoff[0:3]
                if(cutoff_operator != 'agt' and cutoff_operator != 'age' and cutoff_operator != 'alt' and 
                   cutoff_operator != 'ale' and cutoff_operator != 'aeq' and cutoff_operator != 'ane'):
                    raise ValueError("Invalid filter by column cutoff absolute operator: " + str(cutoff_operator))
            else:
                cutoff_operator = cutoff[0:2]
                if(cutoff_operator != 'gt' and cutoff_operator != 'ge' and cutoff_operator != 'lt' and 
                   cutoff_operator != 'le' and cutoff_operator != 'eq' and cutoff_operator != 'ne'):
                    raise ValueError("Invalid filter by column cutoff operator: " + str(cutoff_operator))
            
            if name in headers[i]:
                filter_by_col_numbers_file.append(headers[i].index(name))
                filter_column_cutoffs_file.append(cutoff)
            else:
                print("Warning. The column name " + str(name) + " was not found within file # " + str(i+1) + ".")
        filter_by_col_numbers.append(filter_by_col_numbers_file)
        filter_by_col_cutoffs.append(filter_column_cutoffs_file)
        i = i + 1
        
    return filter_by_col_numbers, filter_by_col_cutoffs

def Generate_DE_Data_Types(sample_cols:list)->list:
    data_types = []
    for col in sample_cols:
        if(col == 'NONE'):
            data_types.append('DE-Series')
        else:
            data_types.append('DE-Sample')
    return data_types

def Verify_Query_D_And_S(query_d_list:list, query_s_list:list):
    if(len(query_d_list) != len(query_s_list)):
        raise ValueError("Failure. A-Lister query dictionary and query string lists " +  
                         "are of different length.")

def Process_Col_Header_Arg(columns:list, column_name:str, headers:list)->list:
    ''' This function takes in column name(s) provided by the user and translates
    them into column numbers for each file for that particular column 
    (ex: ID -> 1,4,2 as in the ID column is column number 1 in file 1,
    column number 4 in file 2, and column number 2 in file 3). 
    Inputs:
    columns: a 1D list of strings.
    column_name: string.
    headers: a 2D list of file headers.
    Output: a 2D list of column numbers or an empty 1D list.
    '''
    column_numbers = []
    sub_result = []
    i = 0
    for file_header in headers:
        cols = columns[i].split(',')
        for col in cols:
            if (column_name == 'Sample1' or column_name == 'Sample2') and col == 'NONE':
                sub_result.append(-1)
                break
            if col not in file_header:
                raise ValueError("Could not find the column " + str(col) + " in file #" + str(i+1))
            else:
                sub_result.append(file_header.index(col))
        column_numbers.append(sub_result)
        sub_result = []
        i = i + 1 
    return column_numbers

def Column_Names_To_Column_Numbers(column_names:list, headers:list):
    result = []
    for name in column_names:
        result.append(headers.index(name))
    return result

def Check_DE_Sample_Mappings_For_Uniq(pc_mappings:list):
    ''' No two condition labels within the same file should be assigned the same new condition 
    label. '''
    reference = []
    for mapping in pc_mappings:
        index = mapping.find('->')
        if(index == -1):
            inv_mapping_string = ("The pairwise comparison mapping is invalid (DE-Sample). "
                                  "Each mapping must be formatted as follows: \n"
                                  "condition label as listed in file -> condition "
                                  "label as listed in query. Example: q1->CNTRL. \n" 
                                  "Mapping: " + str(mapping) + ".\n"
                                  "All mappings for this file: " + str(pc_mappings) + ".")
            raise ValueError(str(inv_mapping_string))
        key,value = mapping.split('->')
        if(value in reference):
            raise ValueError("This new condition label has already been assigned to another  "
                             "condition label listed within this file. " 
                             "The duplicated new condition label: " + str(value) + ".")
        else:
            reference.append(value)

def Check_DE_Series_Mappings_For_Uniq(pc_mappings:list):
    '''Check that the columns assigned to each pairwise comparison are unique.
    That is no column should be assigned to more than one pairwise comparison. 
    Any columns that belong to all pairwise comparisons should not be listed 
    within the pairwise comparison map argument. '''
    reference = []
    for mapping in pc_mappings:
        index = mapping.find('->')
        if(index == -1):
            inv_mapping_string = ("The pairwise comparison mapping is invalid (DE-Series). "
                                  "Each mapping must be formatted as follows: \n"
                                  "pairwise comparison name -> columns belonging "
                                  "to that pairwise comparison. Example: "
                                  "CNTRL*T1->log2(FC)1,P-value1 \n"
                                  "Mapping: " + str(mapping) + ".\n"
                                  "All mappings for this file: " + str(pc_mappings) + ".")
            raise ValueError(str(inv_mapping_string))
        key,value = mapping.split('->')
        values = value.split(',')
        for v in values:
            if(v in reference):
                raise ValueError("This column has already been assigned to a pairwise comparison "
                                 "within this file. The column name: " + str(v) + ".")
            else:
                reference.append(v)

def Check_DE_Sample_Mapping_For_FC(pc_mapping:str, fc_cols:list)->int:
    ''' Returns the position of the fold change column within the
    pairwise comparison mapping. '''
    key,value = pc_mapping.split('->')
    j = 0
    for column_name in value.split(','):
        if(column_name in fc_cols):
            # Check if the column name is listed in the -fc argument. 
            fc_col_found = True
            break
        j = j + 1
    if(not fc_col_found):
        raise ValueError("Error. Each pairwise comparison must be mapped to exactly \n"
                         "one unique fold change column. Columns assigned to this \n"
                         "pairwise comparison (" + str(key) + ") -> "
                         + str(value.split(',')) + ". Fold change columns listed \n"
                         "for this file: " + str(fc_cols.split(',')) + ".\n")
    return j

def Check_Mapping_For_Global_Uniq(pc_mappings:list, data_types:list):
    ''' There cannot be any pairwise comparisons that have the same name across 
    all input files. If it is possible to construct a duplicate pairwise comparison 
    name using the user provided pairwise comparison mapping argument throw an error.'''
    error_msg = ("Error. Detected non unique pairwise comparison name. "
                 "There are multiple identical pairwise comparison "
                 "names listed across all input files. The duplicated "
                 "pairwise comparison name: ")
    reference = []
    i = 0
    for pc_map in pc_mappings:
        if(data_types[i] == 'DE-Sample'):
            labels = []
            for label in pc_map.values():
                labels.append(label)
            length = len(labels)
            j = 0
            while j < length:
                r = j + 1
                while r < length:
                    pc_name = labels[j] + '*' + labels[r]
                    pc_name_inv = labels[r] + '*' + labels[j]
                    if(pc_name in reference or pc_name_inv in reference):
                        raise ValueError(error_msg + str(pc_name) + ".")
                    else:
                        reference.append(pc_name)
                        reference.append(pc_name_inv)
                    r = r + 1
                j = j + 1
        elif(data_types[i] == 'DE-Series'):
            for key in pc_map.keys():
                grps = key.split('*')
                inv_key = grps[1] + '*' + grps[0]
                if (key in reference or inv_key in reference):
                    raise ValueError(error_msg  + str(key) + ".")
                else:
                    reference.append(key)
                    reference.append(inv_key)
        i = i + 1
        
def Process_PC_Map_Arg(pc_mappings:list, data_types:list, num_files:int,
                       headers:list, fc_cols:list)->list:
    ''' Returns a list of pairwise comparison maps. '''
    result = []
    if(len(pc_mappings) != num_files):
        raise ValueError("The number of sample mappings must equal to the number of input files.")
    i = 0
    for pc_map in pc_mappings:
        sub_result = {}
        if(data_types[i] == 'DE-Sample'):
            mappings = pc_map.split(',')
            Check_DE_Sample_Mappings_For_Uniq(mappings)
        elif(data_types[i] == 'DE-Series'):
            mappings = pc_map.split(';')
            Check_DE_Series_Mappings_For_Uniq(mappings)
        for mapping in mappings:
            index = mapping.find('->')    
            key, value = mapping.split('->')
            if(data_types[i] == 'DE-Sample'):
                sub_result[key] = value
            elif(data_types[i] == 'DE-Series'):
                # At least one of the columns belonging to each pairwise comparison must be 
                # a fold change column. Verify that this is so. Then place the fold change 
                # column as the first one in the value list.
                current_fc_cols = fc_cols[i]
                j = Check_DE_Sample_Mapping_For_FC(mapping, current_fc_cols)
                col_names = value.split(',')
                new_col_names = []
                # Place the fold change column first.
                new_col_names.append(col_names.pop(j))
                for name in col_names:
                    new_col_names.append(name)
                column_nums = Column_Names_To_Column_Numbers(new_col_names, headers[i])
                sub_result[key] = column_nums
        result.append(sub_result)   
        i = i + 1
    Check_Mapping_For_Global_Uniq(result, data_types)
    return result

def Check_Query_And_PC_Map_Consistency(pc_maps:list, pc_sel:list, data_types:list):
    '''Every paired comparison in query must be either compossible from a pair of labels 
    within the pc_map values (DE-Sample) or be a key in the pc_map (DE-Series).
    Additionally, any listed directions must be UP, DOWN or ALL.'''
    for pc in pc_sel:
        valid = False
        index = pc.find(':')
        if(index == -1):
            pass
        else:
            dpc = pc
            pc = dpc[:index]
            direction = dpc[index+1:]
            if(direction != 'DOWN' and direction != 'UP' and direction != 'ALL'):
                raise ValueError("Directionalities can only be UP, DOWN, or ALL. " + 
                                 "The direction: " + str(direction) + ".")
        i = 0
        for pc_map in pc_maps:
            grps = pc.split('*')
            if(data_types[i] == 'DE-Sample'):
                if(grps[0] in pc_map.values() and grps[1] in pc_map.values()):
                    valid = True
            elif(data_types[i] == 'DE-Series'):
                inverse_pc = grps[1] + '*' + grps[0]
                if(pc in pc_map.keys() or inverse_pc in pc_map.keys()):
                    valid = True
            i = i + 1
        if(not valid):
            raise ValueError("Query is inconsistent with pairwise comparison map. " + 
                             "Could not generate this paired comparison: " + str(pc) + 
                             " from pairwise comparison map:" + str(pc_maps))