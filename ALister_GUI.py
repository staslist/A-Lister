import eel
import os
import csv
import shlex
from pathlib import Path
from tkinter import filedialog
from tkinter import *

import CLI
from ALister_CLI import Test_Main

# Set web files folder and optionally specify which file types to check for eel.expose()
#   *Default allowed_extensions are: ['.js', '.html', '.txt', '.htm', '.xhtml']
eel.init('web', allowed_extensions=['.js', '.html'])


# File Status Functions

@eel.expose
def checkFileExists(filepath:str)->bool:
    return Path(filepath).is_file()

@eel.expose 
def checkDirectoryExists(dirpath:str)->bool:
    return Path(dirpath).is_dir()

@eel.expose
def readFiveLines(filepath:str, input_delim:str)->list:
    '''Read in first 5 lines of a text delimited file.
    Then return a list containing those first 10 lines. '''
    toReturn = []
    with open(Path(filepath), newline='') as f:
        delim = ''
        if(input_delim == 'comma'):
            delim = ','
        elif(input_delim == 'tab'):
            delim = '\t'
        elif(input_delim == 'space'):
            delim = ' '
        elif(input_delim == 'colon'):
            delim = ':'
        elif(input_delim == 'semicolon'):
            delim = ';'
        else:
            raise ValueError('Invalid input delimiter: ', str(input_delim))
        reader = csv.reader(f,delimiter=delim)
        
        num_lines = 5
        i = 0
        for row in reader:
            if(i < num_lines):
                toReturn.append(row)
                i = i + 1
            else:
                break
    return toReturn

@eel.expose 
def findDESamplePCs(filepath:str, input_delimiter:str, sample1_column:str, sample2_column:str):
    ''' Read in and return all pairwise comparisons from a DE-Sample file. '''
    pairwise_comparisons = []
    sample1_column_num = 0
    sample2_column_num = 0
    with open(Path(filepath), newline='') as f:
        delim = ''
        if(input_delimiter == 'comma'):
            delim = ','
        elif(input_delimiter == 'tab'):
            delim = '\t'
        elif(input_delimiter == 'space'):
            delim = ' '
        elif(input_delimiter == 'colon'):
            delim = ':'
        elif(input_delimiter == 'semicolon'):
            delim = ';'
        else:
            raise ValueError('Invalid input delimiter: ', str(input_delimiter))
        reader = csv.reader(f,delimiter=delim)
        
        header = True
        for row in reader:
            if(header):
                sample1_column_num = row.index(sample1_column)
                sample2_column_num = row.index(sample2_column)
                header = False
                continue
            labels = []
            label1 = row[sample1_column_num]
            label2 = row[sample2_column_num]
            labels.append(label1)
            labels.append(label2)
            if(labels not in pairwise_comparisons):
                pairwise_comparisons.append(labels)
            
    return pairwise_comparisons


@eel.expose
def readDESampleLabels(filepath:str, input_delim:str, sample1_column:str, sample2_column:str)->list:
    '''Read in and return all labels from a DE-Sample file '''
    labels = []
    sample1_column_num = 0
    sample2_column_num = 0
    with open(Path(filepath), newline='') as f:
        delim = ''
        if(input_delim == 'comma'):
            delim = ','
        elif(input_delim == 'tab'):
            delim = '\t'
        elif(input_delim == 'space'):
            delim = ' '
        elif(input_delim == 'colon'):
            delim = ':'
        elif(input_delim == 'semicolon'):
            delim = ';'
        else:
            raise ValueError('Invalid input delimiter: ', str(input_delim))
        reader = csv.reader(f,delimiter=delim)
        
        header = True
        for row in reader:
            if(header):
                sample1_column_num = row.index(sample1_column)
                sample2_column_num = row.index(sample2_column)
                header = False
                continue
            label1 = row[sample1_column_num]
            label2 = row[sample2_column_num]
            if(label1 not in labels):
                labels.append(label1)
            if(label2 not in labels):
                labels.append(label2)
            
    return labels

# File Dialog Functions

@eel.expose
def fileDialog():
    """ Ask the user to select file. """
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    file_path = filedialog.askopenfilename(parent=root)
    root.update()
    root.destroy()
    return file_path

@eel.expose
def filesDialog():
    """ Ask the user to select one or more files. """
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    file_paths = filedialog.askopenfilenames(parent=root)
    root.update()
    root.destroy()
    return file_paths

@eel.expose
def directoryDialog():
    ''' Ask the user to select a directory. ''' 
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    file_path = filedialog.askdirectory(parent=root)
    root.update()
    root.destroy()
    return file_path


# Execute ALister with CLI Command Functions

@eel.expose                         # Expose this function to Javascript
def execute_ALister(command:str)->str:
    result = callALister(command)
    
    toReturn = ''
    for DEE in result:
        toReturn = toReturn + DEE + '\n'
    
    return toReturn

def callALister(s:str)->list:
    ''' This command takes in a CLI style A-Lister command such as the ones supplied 
    in A-Lister CLI examples and parses it. The command is received from GUI instead of 
    CLI. The results of the 1st A-Lister query are then output back into GUI. '''
    
    s = shlex.split(s)
    
    # Remove the python from CLI command + remove all quote marks.
    
    i = 1
    s2 = []
    while i < len(s):
        s2.append(s[i])
        i = i + 1
    
    cli = CLI.AListerCLI()
    args = cli.acceptInput(s2)
    
    results = Test_Main(args)
    result = results[0]
    print(result)
    return result

eel.start('A_Lister_Front.html')             # Start (this blocks and enters loop)