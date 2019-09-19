# A-Lister v1.1

A-Lister is a dual interface (CLI & GUI) tool that assists with analysis of differentially expressed entities (DEEs), such as differentially expressed genes (DEGs), differentially expressed proteins (DEPs), and differentially methylated positions/regions (DMPs/DMRs), across multiple pairwise comparisons. 

## Installation

Supported Operating Systems: Windows 10, Mac OS (10.10.x+), Unix (Ubuntu, Other).

1) Install Python version 3.7 or higher. 
https://www.python.org/downloads/

2) Check whether you have pip installed. Type pip (or pip3) -V in 
command line (Windows), terminal (Mac OS), bash shell (Unix).
If you do not have pip installed follow these instructions to 
install pip (python package management system). 
https://pip.pypa.io/en/stable/installing/

3) Install Eel. https://github.com/ChrisKnott/Eel
```
pip install eel 
or
pip3 install eel
```

4) Download A-Lister from GitHub.

## Running A-Lister

To run A-Lister using command line type ```python ALister_CLI.py``` while located in A-Lister's directory. This will bring up the help menu with list of available commands. For more information please refer to command line interface documentation below. 

To run A-Lister using graphical user interface type ```python ALister_GUI.py``` while located in A-Lister's directory. For more information please refer to graphical user interface documentation below.

We recommend that novice users use the GUI. The GUI portion of documentation will guide you through complete examples.
The CLI is better suited for those experienced with command line or using UNIX OS.

**Note: Depending on how python is setup on your system you may need to type python3 instead of python within the terminal.**

## About/Documentation

### 1. A-Lister Input

Supported File Formats:
Theoretically any text delimited file should work. However, A-Lister has only been 
tested with standard .csv, .tsv, .txt (delimited), and .diff files.

##### Name List Mode:
In this mode A-Lister accepts files containg columns of names delimited
by tab or comma. The header row musts contain group names for each column. 
Examples of this format can be found in Sample_Input/Name_List folder.

|	Control | Treated1 | Treated2 | 
| ------- | ------- | ------- | 
| AADACL2 | AADACP1 | AADACP1 |
| AADACL4 | DUSP5P1 | AMICA1 | 

##### Differential Expression Mode:  
In this mode, A-Lister accepts differential expression files containing a primary id
column (e.g. gene name), fold change column(s), and any other columns present.
The columns in these files must be delimited by tab, comma, colon, semicolon, or space.
A-Lister supports two types of differential expression file formats described below.  

1) *Differential Expression Sample Format (DE-Sample) (Row-Format) File*:  
This is a delimited text file containing a primary ID column, single Fold Change column, 
one Sample1 column, and one Sample2 column. The Sample1 and Sample2 columns identify to
which pairwise comparison each row belongs. This way multiple pairwise comparisons can
be listed within the same DE-Sample file using a *single* fold change column. 
Examples of this format can be found in Sample_Input/DE_Sample/ folder.  

|	gene | locus | sample_1 | sample_2 | log2(FC) | p_value |
| ------- | ------- | ------- | ------- | ------- | ------- |
| FAM3A | chrX:154506158-154516242 | q1 | q2 | 2.73 | 0.0023 |
| FAM3A | chrX:154506158-154516242 | q3 | q4 | 0.0649976 | 0.81 |

2) *Differential Expression Series Format (DE-Series) (Column-Format) File*: 
This is a delimited text file containing a primary ID and multiple Fold Change columns. Each 
Fold Change column contains data pertaining to a single pairwise comparison. This way multiple
pairwise comparisons can be listed within the same DE-Series file using *multiple* 
fold change columns. Examples of this format can be found in Sample_Input/DE_Series/ folder.  

| gene | locus | log2(FC) | p_value | log2(FC)2 | p_value2 |
| ------ | ------ | ------ | ------ | ------ | ------ |
|FAM3A | chrX:154506158-154516242 | 2.73 | 0.0023 | 0.0649976 | 0.81 |

### 2. A-Lister Functionality  

A-Lister has two primary modes of operation: name list and differential expression. 
In differential expression mode A-Lister can be used to compare and filter 
lists of differentially expressed entities (DEEs) such as DEGs, DEPs, 
and DMPs/DMRs. The input text delimited files containing differential 
expression data can be filtered by any column. A common example is filtering 
input data based on p-value column to only include rows with p-value <= 0.05.
A-Lister assumes that the DEEs are listed in form of paired comparisons 
within the input files. That is every DEE in a given file belongs to some paired 
comparison between two conditions (e.g., treated vs control). These 
paired comparisons can be filtered based on the directionality (sign) 
of their respective fold changes. That is, all DEEs belonging to a particular 
paired comparison can be filtered based on the sign of their fold change.  

In addition to column and directionality based filtering, A-Lister can 
compare paired comparisons with one another using set operations such 
as AND (intersect), FAND (fuzzy intersect), OR (union), and DIFF (difference). 
The combination of these filtering and set operations allows us to ask 
interesting questions (queries) about our data.  

For example, suppose we have two paired comparisons in a single differential 
expression file or across two differential expression files. Paired comparison 
number one has a list of differentially expressed genes (DEGs) between the 
control group and group treated with drug #1. Paired comparison number two 
has a list of DEGs between control group and group treated with drug #2. 
We would like to know which genes were more highly expressed in control 
group than in groups treated with drug #1 and drug #2. This question can 
be represented by the following A-Lister query (CNTRL\*T1:DOWN-AND-CNTRL\*T2:DOWN). 
More complex queries can be constructed by comparing any number of paired 
comparisons from across an unlimited number of files. Order of operations 
can be enforced within the query by using parenthesis.  

In name-list mode you can also perform set operations on lists of names. However, 
you cannot use any filtering operations.  

#### A-Lister Filtering  

A-Lister supports filtering differential expression files by columns (attributes). 
When filtering a DE-Sample file by an attribute the entire file is filtered. When filtering a 
DE-Series file by an attribute there are two possible behaviors. First, if the filter 
attribute belongs to a pairwise comparison, such as p-value2, then only that pairwise 
comparison is filtered. Second, if the filter attribute belongs to the entire file 
(e.g. ID column), then the entire file is filtered. Additionally, pairwise comparisons 
can be filtered by direction (sign of fold change) using the directional query argument.  

#### A-Lister Directional Query 

A-Lister directional query is composed of pairwise comparison names, set operators, and 
optional directions. The pairwise comparison names are derived from the pairwise 
comparison mapping. The permitted set operators are: AND, FAND, OR, and DIFF. 

**Set Operations**

*AND* - intersection. An intersection of two sets returns a set of all 
the elements that are present within both sets.  

*FAND* - fuzzy intersection. A fuzzy intersection of two sets returns a 
set of all the similar elements from within both sets. A customized Jaro-Winkler algorithm 
is used to calculate similarity. To be considered similar two strings must have have 
Jaro-Winkler score > 0.84.  

Jaro-winkler algorithm: http://users.cecs.anu.edu.au/~Peter.Christen/publications/tr-cs-06-02.pdf  

Example: \[FRAC10, ALOC, BRAC] FAND \[FRAC11, ALUK, PRAT14, MRA, BRAC] = \[FRAC10, FRAC11, BRAC]  

*OR* - union. A union of two sets returns all the elements present 
in either set.  

*DIFF* - difference. A difference of two sets returns all the elements 
present in the first set, but not in the second.  

**Directionality**

*UP* - upregulated. Selects all entities whose fold change values are positive 
for a given pairwise comparison.  

*DOWN* - downregulated. Selects all entities whose fold change values are negative 
for a given pairwise comparison.  

*ALL* is a special modifier that results in multiple queries. 
In one query ALL is replaced by UP. In the other query ALL is replaced by DOWN.
A query containing N ALL directions is transformed into N^2 queries. 
Each query is then executed and the results for each query are output into the 
output files.  

Example 1: CNTRL\*T:ALL-AND-CNTRL\*T2 -> CNTRL\*T:UP-AND-CNTRL\*T2 , CNTRL\*T:DOWN-AND-CNTRL\*T2.  

Example 2: CNTRL\*T:ALL-AND-CNTRL\*T2:ALL -> CNTRL\*T:UP-AND-CNTRL\*T2:UP ,
CNTRL\*T:UP-AND-CNTRL\*T2:DOWN , CNTRL\*T:DOWN-AND-CNTRL\*T2:UP , CNTRL\*T:DOWN-AND-CNTRL\*T2:DOWN.  

*NONE* - the default direction for all pairwise comparisons.  

**Pairwise Comparison Mapping**

This is done differently depending on differential expression file type (DE-Sample or DE-Series).
The goal of pairwise comparison mapping is to clearly indicate the names of pairwise comparisons 
and to which pairwise comparison every entry in the file belongs.  

For DE-Sample files the user must map each label listed in the sample1 and sample2 columns 
to some unique, short, and descriptive new labels. For example, file
Sample_Input/DE_Sample/GSE76453_cuffdiff_E2.diff contains two labels: q1 and q2. 
These labels are not descriptive and may conflict with labels contained in other differential 
expression files. A good mapping for these labels would be q1->Ctl, q2->ZNF143 based on GEO GSE76453 
description. This mapping more clearly indicates what each condition represents. 
The q1\*q2 pairwise comparison will then be named based on these new labels as Ctl\*ZNF143.  

For DE-Series files the user must come up with their own pairwise comparison names and map 
these names to all the columns that contain data pertaining to those pairwise comparisons. 
For example, file Sample_Input/DE_Series/GSE126785_M2M4.csv contains two pairwise comparisons. 
These pairwise comparisons can be appropriately named as M2Low\*M2High and M4Low\*M4High based 
on the GEO GSE126785 experiment description. The correct mapping would then be 
M2Low\*M2High->log2(FC)M2,P-valueM2,P-adjM2 and M4Low\*M4High->log2(FC)M4,P-valueM4,P-adjM4. 
One of the mapped columns must always be a fold change column. The ID columns belong to all 
pairwise comparisons and therefore do not need to be mapped to any individual pairwise comparison.  

#### A-Lister Query (Non-Directional)

This is the query argument used in the name-list command. A non-directional query is
composed of group names and set operators. The set operators are the same as in the
directional query (i.e., AND, FAND, OR, DIFF). The group names are derived from the
first (header) row of the name list files.  

### 3. A-Lister Output

A-Lister's output is contained within several files. The result.txt file 
contains the name list of entities returned by the query. If an ALL direction 
query was requested the result file will contain a name list corresponding to 
each directional query generated from the all direction query. 
The filtered differential expression files are output in differential expression 
mode only. Additionally, a data_dump.txt file is output containing information 
about how A-Lister executed the query. This information is primarily used for 
validation and or debugging.  

**A-Lister Output Structure**  

For Example 2: CNTRL\*T:ALL-AND-CNTRL\*T2:ALL ->  

Query0: CNTRL\*T:UP-AND-CNTRL\*T2:UP  
Query1: CNTRL\*T:UP-AND-CNTRL\*T2:DOWN  
Query2: CNTRL\*T:DOWN-AND-CNTRL\*T2:UP  
Query3: CNTRL\*T:DOWN-AND-CNTRL\*T2:DOWN  

Output will be:  
1)result.txt  
2)data_dump.txt  
3)FilteredDEFiles  
--a)Query0 (CNTRL\*T:UP-AND-CNTRL\*T2:UP)  
--b)Query1 (CNTRL\*T:UP-AND-CNTRL\*T2:DOWN)  
--c)Query2 (CNTRL\*T:DOWN-AND-CNTRL\*T2:UP)  
--d)Query3 (CNTRL\*T:DOWN-AND-CNTRL\*T2:DOWN)  

## Graphical User Interface Documentation  

This section demonstrates how to use the A-Lister graphical user interface using examples.

**Name List Example**

One name-list file: Sample_Input/Name_List/names_comma.txt. There are 3 groups in this file: Control, Treated1, and Treated2.
We want to find entities in common between Treated1 and Treated2 groups.

1) Select the name list execution mode.
2) Select Sample_Input/Name_List/names_comma.txt file using the "browse" button. Then select the corresponding input file delimiter (comma). Finally, click "add file" in order to add file to the file selection area. A tab will appear. You can examine file previews within this tab. 

![NameListGUI1](/Images/NameListGUI1.png)

3) Either type the query into query input box or click "build query" and use the combination of group name and set operator buttons to 
build a query.
4) Select the output delimiter and output directory. 
5) Select whether to run in verbose or silent mode.
6) Click "generate command". This generates an appropriate CLI command. 

![NameListGUI2](/Images/NameListGUI2.png)

7) You can then launch this command within GUI or by pasting it into command line.

![NameListGUI3](/Images/NameListGUI3.png)

**Differential Expression Example**

Two differential expression files: Sample_Input/DE_Series/GSE114528_differential_exp_EVP_D.tsv and Sample_Input/DE_Sample/GSE99397_CreNeg-MHCPos_vs_CrePos-MHCNeg.diff. We want to find significantly differentially expressed genes in common between the EVP\*D and CreNeg\*CrePos pairwise comparisons. 

1) Select the differential expression execution mode.
2) Select Sample_Input/DE_Series/GSE114528_differential_exp_EVP_D.tsv file using the "browse" button. Then select the corresponding input file delimiter (tab). Click "add file" in order to add file to the file selection area. Click on "File1" in the file selection tab bar. 

![DiffExpressionGUI1](/Images/DiffExpressionGUI1.png)

3) Verify that the ID Column Name is correct. In this example we want to use Gene_Name column. Select the differential expression file type (DE-Series). Click on "Add PC Map" in order to add a pairwise comparison mapping for this file. Name the pairwise comparison EVP\*D. Then select the appropriate fold change column. If this file contains only a single pairwise comparison then it is not necessary to select additional columns. 

![DiffExpressionGUI2](/Images/DiffExpressionGUI2.png)

4) Add filters. Herein, we have added fold change, adjusted p-value, and base mean based filters.  

![DiffExpressionGUI3](/Images/DiffExpressionGUI3.png)

5) Select Sample_Input/DE_Sample/GSE99397_CreNeg-MHCPos_vs_CrePos-MHCNeg.diff file using the "browse" button. Then select the corresponding input file delimiter (tab). Click "add file" in order to add file to the file selection area. Click on "File2" in the file selection tab bar. Verify that the ID, Fold Change, Sample1, and Sample2 column names are correct.
6) Select DE-Sample file type. Click on "Build PC Map". Map the file specific sample labels to new label names of your choice. Add filters. Herein, we have added fold change and p-value filters.

![DiffExpressionGUI4](/Images/DiffExpressionGUI4.png)

7) Either directly enter the query or click on build query and use the pairwise comparison, set operator, and directionality buttons.

![DiffExpressionGUI5](/Images/DiffExpressionGUI5.png)

8) Select the output delimiter and output directory. 
9) Select whether to run in verbose or silent mode.
10) Click generate command. This generates an appropriate CLI command. 

![DiffExpressionGUI6](/Images/DiffExpressionGUI6.png)

11) You can then launch this command within GUI or by pasting it into command line. Note that the output within the GUI shows the results of a single query only. The complete results can be found in output files. 

## Command Line Interface Documentation  

**A-Lister Help**
```
$ python ALister_CLI.py --help
usage:
  ALister_CLI.py command
commands:
  diff-expression Analyze differential expression data.
  name-list       Analyze name list data.

A-Lister v1.0: a differentially expressed entities analysis package. Namely,
A-Lister assists in identification of top genes, proteins, and methylation
markers of interest across multiple pairwise comparisons.

positional arguments:
  {name-list,diff-expression}

optional arguments:
  -h, --help            show this help message and exit
```

**Name List Help & Example Commands**  

```
$ python ALister_CLI.py name-list --help
$ python ALister_CLI.py name-list --examples
```

**Differential Expression Help & Example Commands**  

```
$ python ALister_CLI.py diff-expression --help
$ python ALister_CLI.py diff-expression --examples
```

## Future Development Roadmap  

1) Pip packaging. User interface update. (2020 Q1-Q2)
2) ID validation and mapping. Genomic types integration. (2020 Q2-Q3)
3) Web interface. (2020 Q3-Q4)

## Acknowledgements  

The following Gene Expression Omnibus datasets are used as sample and test input 
within A-Lister: GSE76453, GSE116610, GSE108643, GSE75035, GSE77137, GSE126785, 
GSE101484, GSE99397, GSE114528.
https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi

## Authors 

Stanislav Listopad and
Trina Norden-Krichmar
