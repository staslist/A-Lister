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

import argparse
import sys
import os
from pathlib import Path

class NameListExampleAction(argparse.Action):

    def __init__(self, option_strings, dest, default=None, required=False, help=None):
        super().__init__(option_strings=option_strings, dest=dest,
                         nargs=0, default=default, required=required, help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        print("Listed below are some usage examples. You may need to type python3 instead of "
              "python to run these examples depending on how python is set up on your system.")
        print()
        example1 = ("# Example Name List 1:\n"
                    "# One name-list file. Three groups: Control, Treated1, and Treated2.\n"
                    "# Query is an intersection of two groups.\n\n"
                    'python ALister_CLI.py name-list "Treated1-AND-Treated2" E:/Data/Sample_Input'
                    '/Name_List/names_comma.txt -id comma -o E:/Data/Sample_Output/Name_List/Example1/ '
                    '-od tab -v')
        print(example1)
        print()
        example2 = ("# Example Name List 2:\n"
                    "# Two name-list files. Complex query across groups from both files. \n\n"
                    'python ALister_CLI.py name-list "Set1-DIFF-(Control-OR-(Treated1-AND-Treated2))" '
                    'E:/Data/Sample_Input/Name_List/fileA.txt E:/Data/Sample_Input/Name_List/names_comma.txt '
                    "-id tab comma -o E:/Data/Sample_Output/Name_List/Example2/ -od comma-row -v")
        print(example2)
        sys.exit()
        
class DiffExpressionExampleAction(argparse.Action):

    def __init__(self, option_strings, dest, default=None, required=False, help=None):
        super().__init__(option_strings=option_strings, dest=dest,
                         nargs=0, default=default, required=required, help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        print("Listed below are some usage examples. You may need to type python3 instead of "
              "python to run these examples depending on how python is set up on your system.")
        print()
        print("Example Set 1 - DE-Sample Files Only:")
        print("-------------------------------------")
        example1 = ("# ZNF143 vs Control Cells (DE Example 1):\n"
                    "# Two Cuffdiff files. One pairwise comparison and two condition labels (q1,q2) in each file. \n"
                    "# Filter each file with log2(fold_change), q_value, value1, and value2 attributes.\n"
                    "# Execute a difference query over ZNF143_veh*ZNF143_E2 and Ctl_veh*Ctl_E2.\n\n"
                    "python ALister_CLI.py diff-expression "
                    'E:/Data/Sample_Input/DE_Sample/GSE76453_cuffdiff_siCtl.diff '
                    'E:/Data/Sample_Input/DE_Sample/GSE76453_cuffdiff_siZNF143.diff '
                    '-pc "q1->Ctl_veh,q2->Ctl_E2" "q1->ZNF143_veh,q2->ZNF143_E2" '
                    '-dq "ZNF143_veh*ZNF143_E2-DIFF-Ctl_veh*Ctl_E2" '
                    '-o E:/Data/Sample_Output/DE/Example1/ -n "gene" -s1 "sample_1" '
                    '-s2 "sample_2" -f "log2(fold_change):agt1.2,q_value:'
                    'lt0.05,value_1:gt1.0,value_2:gt1.0" -v')
        print(example1)
        print()
        example2 = ("# ZNF143 vs Control Cells (DE Example 2):\n"
                    "# One Cuffdiff file. One pairwise comparison and two condition labels (q1,q2). \n"
                    "# Filter file with several attributes. Execute an ALL direction query (2 direction patterns - U,D).\n\n"
                    'python ALister_CLI.py diff-expression '
                    'E:/Data/Sample_Input/DE_Sample/GSE76453_cuffdiff_E2.diff '
                    '-pc "q1->Ctl,q2->ZNF143" -dq "Ctl*ZNF143:ALL" '
                    '-o E:/Data/Sample_Output/DE/Example2/ -od tab -n "gene" -v '
                    '-fc "log2(fold_change)" -s1 "sample_1" -s2 "sample_2" -f '
                    '"log2(fold_change):agt1.2,q_value:lt0.05,value_1:gt1.0,value_2:gt1.0"')
        print(example2)
        print()
        example3 = ("# Exercise in Obese vs Lean Individuals (DE Example 3):\n"
                    "# One Cuffdiff file with four condition labels (LeanPre,LeanPost,OvobPre,OvobPost).\n"
                    "# Filter file with several attributes. Launch an ALL direction query (4 direction patterns - UU,UD,DU,DD).\n\n"
                    "python ALister_CLI.py diff-expression "
                    'E:/Data/Sample_Input/DE_Sample/GSE108643_Cuffdiff.txt '
                    '-pc "LeanPre->LPE,LeanPost->LPO,OvobPre->OPE,OvobPost->OPO" '
                    '-dq "LPE*LPO:ALL-AND-OPE*OPO:ALL" -o E:/Data/Sample_Output/DE/Example3/ '
                    '-f "log2(fold_change):agt1.0,q_value:lt0.05,value_1:gt1.0,value_2:gt1.0" '
                    '-v -s1 "sample_1" -s2 "sample_2" -n "gene"')
        print(example3)
        print()
        example4 = ("# Exercise in Obese vs Lean Individuals (DE Example 4):\n"
                    "# One Cuffdiff file with four condition labels (LeanPre,LeanPost,OvobPre,OvobPost).\n"
                    "# Filter file with several attributes. Execute a complex query over several pairwise comparisons.\n\n"
                    "python ALister_CLI.py diff-expression "
                    'E:/Data/Sample_Input/DE_Sample/GSE108643_Cuffdiff.txt '
                    '-pc "LeanPre->LPE,LeanPost->LPO,OvobPre->OPE,OvobPost->OPO" '
                    '-dq "(LPE*LPO-FAND-OPE*OPO)-DIFF-(LPE*LPO-AND-OPE*OPO)" '
                    '-id tab -o E:/Data/Sample_Output/DE/Example4/ -od comma-row '
                    '-f "log2(fold_change):agt1.2,q_value:lt0.05,value_1:gt1.0,value_2:gt1.0" '
                    '-v -s1 "sample_1" -s2 "sample_2" -n "gene"')
        print(example4)
        print()
        print()
        print("Example Set 2 - DE-Series files only:")
        print("-------------------------------------")
        example5 = ("# Effect of Oxygen Saturation on Stem Cells (DE Example 5):\n"
                    "# A single csv file built from three Deseq2 files. Three pairwise comparisons total.\n"
                    "# Filter each pairwise comparison according to the fold change and p-value columns.\n"
                    "# Execute an ALL direction query (8 direction patterns - UUU,UUD,UDU,UDD,DDD,DDU,DUD,DUU).\n\n"
                    "python ALister_CLI.py diff-expression "
                    'E:/Data/Sample_Input/DE_Series/GSE126785_M2M4M5.csv '
                    '-pc "M2Low*M2High->log2(FC)M2,P-valueM2,P-adjM2;M4Low*M4High->log2(FC)M4,'
                    'P-valueM4,P-adjM4;M5Low*M5High->log2(FC)M5,P-valueM5,P-adjM5" '
                    '-dq "M2Low*M2High:ALL-AND-M4Low*M4High:ALL-AND-M5Low*M5High:ALL" '
                    '-o E:/Data/Sample_Output/DE/Example5/ '
                    '-f "P-valueM2:lt0.05,P-valueM4:lt0.05,P-valueM5:lt0.05,log2(FC)M2:agt0.8,'
                    'log2(FC)M4:agt0.8,log2(FC)M5:agt0.8" '
                    '-fc "log2(FC)M2,log2(FC)M4,log2(FC)M5" -n "GeneID" -id comma -v')
        print(example5)
        print()
        example6 = ("# Effect of Oxygen Saturation on Stem Cells (DE Example 6):\n"
                    "# One csv file with two pairwise comparisons and one Deseq2 file with one pairwise comparison.\n"
                    "# Three pairwise comparisons total. Filter the pairwise comparisons across both files according to fold change. \n"
                    "# Execute a complex query across all pairwise comparisons.\n\n"
                    "python ALister_CLI.py diff-expression "
                    'E:/Data/Sample_Input/DE_Series/GSE126785_M2M4.csv '
                    'E:/Data/Sample_Input/DE_Series/GSE126785_M5.txt '
                    '-pc "M2Low*M2High->log2(FC)M2,P-valueM2,P-adjM2;M4Low*M4High->log2(FC)M4,'
                    'P-valueM4,P-adjM4" "M5Low*M5High->3.log2(FC)" '
                    '-dq "M2Low*M2High-DIFF-(M5Low*M5High-OR-M4Low*M4High)" '
                    '-o E:/Data/Sample_Output/DE/Example6/ -n "GeneID" "1.GeneID" '
                    '-f "log2(FC)M2:agt1.0,log2(FC)M4:agt1.0" "3.log2(FC):agt1.0" '
                    '-fc "log2(FC)M2,log2(FC)M4" "3.log2(FC)" -id comma tab -v')
        print(example6)
        print()
        example7 = ("# Effect of Oxygen Saturation on Stem Cells (DE Example 7):\n"
                    "# Three DESeq2 files with one pairwise comparison in each file.\n"
                    "# Filter the pairwise comparisons across both files according to fold change. \n"
                    "# Execute a complex query across all pairwise comparisons.\n\n"
                    "python ALister_CLI.py diff-expression "
                    'E:/Data/Sample_Input/DE_Series/GSE126785_M2.txt '
                    'E:/Data/Sample_Input/DE_Series/GSE126785_M4.txt '
                    'E:/Data/Sample_Input/DE_Series/GSE126785_M5.txt '
                    '-pc "M2Low*M2High->3.log2(FC)" "M4Low*M4High->3.log2(FC)" "M5Low*M5High->3.log2(FC)" '
                    '-dq "M2Low*M2High-DIFF-(M5Low*M5High-OR-M4Low*M4High)" '
                    '-o E:/Data/Sample_Output/DE/Example7/ -n "1.GeneID" '
                    '-f "3.log2(FC):agt1.0" -fc "3.log2(FC)" -v')
        print(example7)
        print()
        print()
        print("Example Set 3 - DE-Series and DE-Sample files:")
        print("----------------------------------------------")
        example8 = ("Melanoma in Mice (DE Example 8):\n"
                    "# One Cuffdiff and one DESeq2 file with one pairwise comparison in each file. \n"
                    "# Filter the Cuffdiff file according to fold change and p-value.\n"
                    "# Filter the DESeq2 file according to base mean, fold change, and adjusted p-value. \n"
                    "# Execute a query across EVP*D and CPOS*CNEG pairwise comparisons.\n\n"
                    "python ALister_CLI.py diff-expression "
                    'E:/Data/Sample_Input/DE_Series/GSE114528_differential_exp_EVP_D.tsv '
                    'E:/Data/Sample_Input/DE_Sample/GSE99397_CreNeg-MHCPos_vs_CrePos-MHCNeg.diff '
                    '-pc "EVP*D->log2FoldChange" "CrePos-MHCNeg->CPOS,CreNeg-MHCPos->CNEG" '
                    '-dq "EVP*D-AND-CPOS*CNEG" -fc "log2FoldChange" "log2(fold_change)" '
                    '-o E:/Data/Sample_Output/DE/Example8/ -od comma-row '
                    '-f "padj:lt1E-5,log2FoldChange:agt2.5,baseMean:gt500" '
                    '"log2(fold_change):agt0.85,p_value:lt0.05" -v -s1 "NONE" "sample_1" -s2 "NONE" '
                    '"sample_2" -n "Gene_Name" "gene"')
        print(example8)
        print()
        sys.exit()

class AListerCLI():
    
    def __init__(self):
        usage_string = ("\n  ALister_CLI.py command \n"
                        "commands: \n"
                        "  diff-expression Analyze differential expression data.\n"
                        "  name-list       Analyze name list data.\n")
        
        self.parser = argparse.ArgumentParser(description = "A-Lister v1.1: a differentially expressed entities "+
                                              "analysis package. Namely, A-Lister assists in identification "+
                                              "of top genes, proteins, and methylation markers of interest "+ 
                                              "across multiple pairwise comparisons. ",
                                              usage = usage_string)
        self.subparsers = self.parser.add_subparsers()
        
        usage_string = ("\n  ALister_CLI.py name-list <query> <input-file> [<input-file> ...] [options] \n"
                        "  ALister_CLI.py name-list (-e | --examples) \n"
                        "  ALister_CLI.py name-list (-h | --help) \n \n")
        self.parser2 = self.subparsers.add_parser('name-list', description = "Analyze name list data.", 
                                                  usage = usage_string,
                                                  formatter_class=argparse.RawTextHelpFormatter)
        
        cwd = os.getcwd()
        
        query_string = ('The non-directional query argument is used to perform set \n'
                        'operations on name lists. The group names are derived \n'
                        'from the 1st row (column headers) of the delimited text file. \n'
                        'The following set operations are permitted: AND, FAND, DIFF, OR. \n'
                        'AND = intersect, FAND = fuzzy intersect, DIFF = difference, and \n'
                        'OR = union. Additionally, parenthesis can be used to set order of \n'
                        'operations. The query argument must be surrounded by quote marks. \n'
                        'Example: "(CONTROL-OR-TREATED1)-AND-(TREATED2)" \n'
                        'Permitted characters: alphanumeric, (), and -. \n')
        self.parser2.add_argument('query', nargs = 1, type = str, metavar= '<query>',
                                  help = query_string)
        self.parser2.add_argument('input_file', nargs = '+', metavar = '<input-file>',
                                  help = 'Full path to the input file.')
        self.parser2.add_argument('-e', '--examples', action = NameListExampleAction,
                                  help = "show examples and exit")
        inp_delim_s =   ("The delimiter used within the input file. \n"
                        "List once if all input files use the same delimiter. \n"
                        "List for every file - in the same order as that of the \n"
                        "input files - if delimiter varies between input files. \n"
                        "Options: tab and comma. Default: tab.\n")
        self.parser2.add_argument('-id', nargs = '+', metavar = '<input_delimiter>',
                                  help = inp_delim_s, choices = ['tab', 'comma'],
                                  default = ['tab'])
        self.parser2.add_argument('-o', nargs = 1, metavar = '<output_directory>',
                                  help = "The output directory. Default: current working directory.",
                                  default = [cwd])
        self.parser2.add_argument('-od', nargs = 1, metavar = '<output_delimiter>', 
                                  help = "The delimiter used in the result file. \n" + 
                                  "Options: tab, comma-row. Default: tab.\n", 
                                  choices = ['tab', 'comma-row'], default = ['tab'])
        self.parser2.add_argument('-v', action = 'count',
                                  help = "Make the output more verbose.")
        usage_string = ("\n  ALister_CLI.py diff-expression <input-file> [<input-file> ...] -pc <pc-mapping> [<pc-mapping> ...] "
                        "-dq <direct-query> [options] \n"
                        "  ALister_CLI.py diff-expression (-e | --examples) \n"
                        "  ALister_CLI.py diff-expression (-h | --help) \n \n")
        self.parser3 = self.subparsers.add_parser('diff-expression', 
                                                  description = "Analyze differential expression data.",
                                                  usage = usage_string,
                                                  formatter_class=argparse.RawTextHelpFormatter)
        self.optional = self.parser3._action_groups.pop()
        self.required = self.parser3.add_argument_group('required arguments')
        self.parser3._action_groups.append(self.optional)
        pc_mapping_s =  ('The pairwise comparison mapping argument is used to indicate \n'
                        'the names and the layout of pairwise comparisons within the \n'
                        'input file. The formatting of this argument is dependent \n'
                        'on the format of the input file (DE-Sample or DE-Series). Within \n'
                        'DE-Sample files each entry (row) in a file is already assigned to a \n'
                        'pairwise comparison via the labels in sample1 and sample2 columns. \n'
                        'A-Lister requires the user to assign each of these file labels new names. \n'
                        'For example, assume that there is a DE-Sample file with labels \n'
                        'q1, q2, q3, and q4 that represent the control, treated1, treated2, \n'
                        'and treated3 conditions. The user would then specify the following \n'
                        'mapping: -pc "q1->CNTRL,q2->T1,q3->T2,q4->T3". \n'
                        'DE-Series files usually do not specify pairwise comparison names. \n'
                        'Therefore, the user must provide their own pairwise comparison names and \n'
                        'then map these names to the appropriate columns. For example, assume \n'
                        'that there is a DE-Series file with five columns: gene, log2(FC)1, P-value1, \n'
                        'log2(FC)2, and P-value2. Assume that this file contains two pairwise \n'
                        'comparisons: day0 vs day7 and day7 vs day14. Columns log2(FC)1 and P-value1 \n'
                        'contain data for day0 vs day7 comparison. Columns log2(FC)2 and P-value2 \n'
                        'contain data for day7 vs day14 comparison. The user would then specify the \n'
                        'following mapping: -pc "d0*d7->log2(FC)1,P-value1;d7*d14->log2(FC)2,P-value2" \n'
                        'The star represents versus. Each pairwise comparison must be assigned \n'
                        'one unique fold change column (e.g. log2(FC)1 and log2(FC)2 above). \n'
                        'For DE-Series files containing a single pairwise comparison it is \n'
                        'sufficient to list only the name of the fold change column. For example, \n'
                        'assume that the log2(FC)2 and P-value2 columns were removed from the \n'
                        'above mentioned file. The appropriate mapping for this new file would \n'
                        'be either -pc "day0*day7->log2(FC)1" or -pc "day0*day7->log2(FC)1,P-value1". \n'
                        'The pairwise comparison mapping argument must be surrounded by \n'
                        'quote marks. Permitted characters: alphanumeric, (), *, ;, -, >. \n')
        self.required.add_argument('-pc', nargs = '+', metavar = '<pc-mapping>',
                                  help = pc_mapping_s, required = True)
        d_query_string =('The directional query argument is used to perform \n'
                        'set operations on pairwise comparisons from differential \n'
                        'expression data and to apply directional filtering. The \n'
                        'following set operations are permitted: AND, FAND, DIFF, OR. \n'
                        'AND = intersection, DIFF = difference, OR = union, FAND = \n'
                        'fuzzy intersection. Additionally, parenthesis can be used to nest \n'
                        'and to set order of operations. Each pairwise comparison listed in \n'
                        'the query can be assigned a direction of UP, DOWN, ALL. \n'
                        'All pairwise comparisons have a direction of NONE by default. \n'
                        'UP in context of pairwise group comparison q1*q2 means \n'
                        'that q2 contains higher expression of this entity than q1. \n'
                        'As in fold change - log2(q2/q1) - is a positive value. \n'
                        'ALL direction is a special modifier that results in multiple queries. \n'
                        'In one query ALL is replaced by UP. In the other query ALL is \n'
                        'replaced by DOWN. A query containing N ALL directions is \n'
                        'transformed into N^2 queries. Each query is then executed \n'
                        'and the results for each query are output into the output files. \n'
                        'The names of pairwise comparisons are constructed \n'
                        'using the pairwise comparison mapping (refer to -pc option). \n'
                        'The query argument must be surrounded by quote marks. \n'
                        'Example: "(CNTRL*T1:UP-AND-CNTRL*T2:UP)-DIFF-CNTRL2*T3" \n'
                        'Permitted characters: alphanumeric, (), *, :, and -. \n')
        self.required.add_argument('-dq', nargs = 1, metavar = '<direct-query>',
                                  help = d_query_string, required = True)
        self.parser3.add_argument('input_file', nargs = '+', metavar = '<input-file>', 
                                  help = 'Full path to the input file.')
        self.optional.add_argument('-e', '--examples', action = DiffExpressionExampleAction,
                                  help = "show examples and exit")
        id_col_string = ("The name of id column within the input files. \n"
                        "List once if all input files have the same column name. \n"
                        "List for every file - in same order as that of the input files - \n"
                        "if column name varies between input files. The id column argument \n"
                        "must be surrounded by quote marks. Default: Id.\n")
        self.optional.add_argument('-n', nargs = '+', metavar = '<id-column>',
                                  help = id_col_string, default = ["Id"])
        fc_col_string = ("The names of fold change columns within the input files. \n"
                        "List once if all input files have the same column names. \n"
                        "List for every file - in same order as that of the input files - \n"
                        "if column names vary between input files. Multiple fold change \n"
                        "columns can be listed for DE-Series files. When listing \n"
                        "multiple fold change columns for a DE-Series file delimit \n"
                        "the column names with commas. The fold change column argument \n"
                        "must be surrounded by quote marks. \n"
                        "Default: log2(fold_change).\n")
        self.optional.add_argument('-fc', nargs = '+', metavar = '<fc-column>',
                                  help = fc_col_string, default = ["log2(fold_change)"])
        sample1_col_s = ('The name of sample1 column within the input files. \n'
                        'List once if all input files have the same column name. \n'
                        'List for every file - in same order as that of the input \n'
                        'files - if column name varies between input files. For DE-Series \n'
                        'files the sample1 column name must be listed as "NONE". \n'
                        'The sample1 column argument must be surrounded by \n'
                        'quote marks. Default: NONE.\n')
        self.optional.add_argument('-s1', nargs = '+', metavar = '<sample1-column>',
                                  help = sample1_col_s, default = ["NONE"])
        sample2_col_s = ('The name of sample2 column within the input files. \n'
                        'List once if all input files have the same column name. \n'
                        'List for every file - in same order as that of the input \n'
                        'files - if column name varies between input files. For DE-Series \n'
                        'files the sample2 column name must be listed as "NONE". \n'
                        'The sample2 column argument must be surrounded by \n'
                        'quote marks. Default: NONE.\n')
        self.optional.add_argument('-s2', nargs = '+', metavar = '<sample2-column>',
                                  help = sample2_col_s, default = ["NONE"])
        filter_col_s =  ('The names of columns by which to filter the files alongside \n'
                        'the respective comparison operators and comparison constant values. \n'
                        'List once if you would like to filter all files the same way. \n'
                        'List for every file - in same order as that of the input files - \n'
                        'otherwise. If you would like to filter some, but not all of the \n'
                        'files, write "NONE" for the files that you do not want to be filtered. \n'
                        'The following comparison operators are permitted: lt (a<b), \n'
                        'le (a<=b), gt (a>b), ge (a>=b), eq (a==b), ne (a!=b), \n'
                        'alt (|a|<b), ale (|a|<=b), agt (|a|>b), age (|a|>=b), \n'
                        'aeq (|a|==b), ane (|a|!=b). \n'
                        'This argument must be surrounded by quote marks. \n'
                        'Example: "log2(fold_change):agt1.2,p_value:lt0.05,q_value:lt0.05." \n')
        
        self.optional.add_argument('-f', nargs = '+', metavar = '<filter-by-column>',
                                  help = filter_col_s, default = [None])
        
        inp_delim_s =   ("The delimiter used within the input file. \n"
                        "List once if all input files use the same delimiter. \n"
                        "List for every file - in the same order as that of the \n"
                        'input files - if delimiter varies between input files. \n'
                        "Options: tab, comma, colon, semicolon, space. \n"
                        "Default: tab.")
        self.optional.add_argument('-id', nargs = '+', metavar = '<input_delimiter>',
                                  help = inp_delim_s, choices = ['tab', 'comma', 'colon', 'semicolon', 'space'],
                                  default = ['tab'])
        self.optional.add_argument('-o', nargs = 1, metavar = '<output_directory>',
                                  help = "The output directory. Default: current working directory.",
                                  default = [cwd])
        self.optional.add_argument('-od', nargs = 1, metavar = '<output_delimiter>', 
                                  help = "The delimiter/format used in the result file. \n" + 
                                  "Options: tab, comma-row. Default: tab.\n", 
                                  choices = ['tab', 'comma-row'], default = ['tab'])
        self.optional.add_argument('-v', action = 'count',
                                   help = "Make the output more verbose.")
        
    def acceptInput(self, test=None):

        if(test!=None):
            sys.argv = test
        
        # If user does not supply any arguments print the help prompt_text and exit.
        if(len(sys.argv) == 1):
            self.parser.print_help()
            sys.exit()
        elif(len(sys.argv) == 2):
            if(sys.argv[1] == 'name-list'):
                self.parser2.print_help()
            elif(sys.argv[1] == 'diff-expression'):
                self.parser3.print_help()
            elif(sys.argv[1] == '--help' or sys.argv[1] == '-h'):
                self.parser.print_help()
            sys.exit()
        else:
            args = self.parser.parse_args(sys.argv[1:])
            args.comparison_type = [sys.argv[1]]
        
        return args
    
    def getParser(self):
        return self.parser 