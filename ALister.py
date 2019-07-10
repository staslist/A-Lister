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

from DiffExpression import Read_And_Filter_DE_Files
from DiffExpression import AListerDiffExprClass
from NameList import Merge_Name_List_Files_Data
from NameList import AListerNameListClass
from ProcessUserInput import Process_User_Input
from CLI import AListerCLI

# Naming conventions:

# Variable names style: hello_world
# Function names style: 
# Hello_World
# Method name style: 
# public: helloWorld
# private: _helloWorld
# Class/File names style: HelloWorld

# Format Conventions:
# Avoid long lines of code whenever possible. 
# Avoid long variable names. Balance clarity/documentation against character count.

# TO DO: 
# 1) Refactor (+optimize) + document + test (Windows CMD Prompt + Ubuntu Shell)
#     (+expand test suite as necessary) code. (RE DO AFTER EVERY NEW FEATURE)
# Major Iteration Features:
# 2)Gene and protein expression integration. (UNIPROT) [v1.1]
# a)Uniprot approach. Filter data. Convert to same genomic data type. 
#   Perform set operations.  
# 3)Methylation and gene expression integration. [v1.2] 
# 4)GUI. [v1.3]

# Other Tasks:
# 1)a)Find a way to get rid of quote marks in the command line arguments.*

#   Command-Builder:  *
#   c)Add header look up.
#   d)File browsing/auto-suggestion. 
#   d2)Sense of progression.
#   d3)Build query last. Provide hints by showing sample mappings, etc.
#   d4)More aggressive error checking during command building.

# 2)a)Gene family fuzzy matching. Fuzzy matching configuration. 
# b)Get top N most differentially expressed genes. 
# c)Replace all complex custom dictionaries (ex: file data) with class objects.

# 3)a)Test ALL core computation corner cases.*
#   b)Expand Test Suites
#    i) No -o flag test case(s). Have to re-factor loggers first in order to release data_dump.txt.
#   c)Setup a streamlined Windows/Unix(Command Line,Batch Job)/Mac OS test scheme.
#   https://realpython.com/python-testing/#executing-your-first-test

#   d)Select distribution option:
#     e)Distribute as a Python package through Github*/Pip*/Conda?/Docker??

# 4) Security/Cloud/Etc.
  
def Main_Helper(parameters:dict, input_files:list)->list:
    result = []

    comp_type = parameters['comp_type']
    out_ftype = parameters['out_delim']
    out_dir = parameters['out_dir']
    query_d_list = parameters['query_d_list']
    query_s_list = parameters['query_s_list']
    
    v = parameters['v']
    
    if(comp_type == 'diff-expression'): 
        total_input_data, total_file_data = Read_And_Filter_DE_Files(input_files)
        driver = AListerDiffExprClass(total_input_data, total_file_data, out_dir, out_ftype, v)
        result = driver.compute(query_d_list, query_s_list)
    elif(comp_type == "name-list"):
        total_input_data = Merge_Name_List_Files_Data(input_files)
        driver = AListerNameListClass(total_input_data, out_dir, out_ftype, v)
        result = driver.compute(query_d_list, query_s_list)
    
    return result

def main():
    ''' This is the A-Lister's main function. This function accepts the command line user input, launches the 
    appropriate interface, processes user input, performs all the necessary computations,
    and writes out the result.'''
    # Process command line input.
    CLI = AListerCLI()
    parameters, input_files = Process_User_Input(CLI.acceptInput())
        
    return Main_Helper(parameters, input_files)    

def Test_Main(args):
    ''' This is the A-Lister's test main function. This function accepts simulated command line user input,
    processes user input, performs all the necessary computations,
    and writes out the result.'''
    # Process command line input.
    parameters, input_files = Process_User_Input(args)
    
    return Main_Helper(parameters, input_files) 
    
    
if __name__ == '__main__':
    main()