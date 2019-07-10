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

from pathlib import Path

# COMPUTATION HELPER FUNCTIONS
def Same_Elements(l:list)->bool:
    ''' If all elements in this list are identical return True.
    If the list empty raise a Value Error. 
    Else return false.'''
    if(len(l) < 1):
        raise ValueError("This list is empty.")
    i = 0
    while i < (len(l)-1):
        if(l[i] == l[i+1]):
            i = i + 1
        else:
            return False
    return True

def Sign(number:float)->int:
    if(number >= 0):
        return 1
    return -1
    
def Inverse_Direction(direction:str)->str:
    if(direction == 'UP'):
        return 'DOWN'
    elif(direction == 'DOWN'):
        return 'UP'
    elif(direction == 'NONE'):
        return 'NONE'
    else:
        raise ValueError("Invalid direction: ", str(direction))
    
def Match_Direction(i:int, s:str)->bool:
    return ((i == 1 and s == 'UP') or (i==-1 and s == 'DOWN') or ((i == 1 or i == -1) and s == 'NONE'))

def jaro_winkler(s:str, t:str)->float:
    sim_j = jaro(s, t)
    len_s = len(s)
    len_t = len(t)
    if(len_s > 2 and len_t > 2):
        min_s_t = min(len_s, len_t)
        min_len = min(min_s_t, 4)
        i = 0
        l = 0
        while i < min_len:
            if(s[i] == t[i]):
                l = l + 1
                i = i + 1
            else:
                break
        sim_w = sim_j + (l * 0.1)*(1-sim_j)
        return sim_w
    else:
        return sim_j

def jaro(s:str, t:str)->float:
    '''Jaro distance between two strings.'''
    s_len = len(s)
    t_len = len(t)
 
    if s_len == 0 and t_len == 0:
        return 1
 
    match_distance = (max(s_len, t_len) // 2) - 1
    if match_distance < 0:
        match_distance = 0
 
    s_matches = [False] * s_len
    t_matches = [False] * t_len
 
    matches = 0
    transpositions = 0
 
    for i in range(s_len):
        start = max(0, i - match_distance)
        end = min(i + match_distance + 1, t_len)
 
        for j in range(start, end):
            if t_matches[j]:
                continue
            if s[i] != t[j]:
                continue
            s_matches[i] = True
            t_matches[j] = True
            matches += 1
            break
 
    if matches == 0:
        return 0
 
    k = 0
    for i in range(s_len):
        if not s_matches[i]:
            continue
        while not t_matches[k]:
            k += 1
        if s[i] != t[k]:
            transpositions += 1
        k += 1
 
    return ((matches / s_len) +
            (matches / t_len) +
            ((matches - transpositions / 2) / matches)) / 3

def Similar(a:str, b:str)->float:
    ''' Reports the similarity ratio between two strings. '''
    #return jellyfish.jaro_winkler(a, b)
    return jaro_winkler(a,b)

def Core_Computation(AListerModule):
    Core_Computation_Loop(AListerModule)
        
def Core_Computation_Loop(AListerModule):
    ''' This function takes a AListerModule object and runs the main compute loop using that object's fields. '''
    if(AListerModule.verbose):
        print("List of groups / paired comparisons to be examined:")
        print(list(AListerModule.input_data.keys()))
    
    num_groups = 0
    groups = []
    group_operators = []
    for k,v in AListerModule.query_d.items():
        if(AListerModule.verbose):
            print("Current subquery: ")
            print(str(k), ' = ', str(v))
        num_groups = 0
        groups = []
        group_operators = []
        groups_and_operators = k.split('-')
        for group_or_operator in groups_and_operators:
            if group_or_operator not in ['AND','FAND','OR','DIFF']:
                if(group_or_operator not in AListerModule.input_data.keys()):
                    print(group_or_operator)
                    raise ValueError("The query group could not be found in the file.")
                groups.append(group_or_operator)
                num_groups = num_groups + 1
            else:
                group_operators.append(group_or_operator) 
        AListerModule.current_vector_values = AListerModule.input_data[groups[0]]
        if(num_groups == 1):
            AListerModule.input_data[v] = AListerModule.current_vector_values
            continue
        i = 1
        while i < num_groups:
            if(AListerModule.verbose):
                print("The groups being compared are current vector values and " + str(groups[i]) + ".")
                print()
                # Sort for ease of examination. 
                AListerModule.current_vector_values.sort()
                print("Current vector values(", len(AListerModule.current_vector_values) ," values): ")
                Print_String_With_Limited_Line_Length(str(AListerModule.current_vector_values))
                print()
                print("The current set operator is: " + group_operators[i-1])
                print()
                AListerModule.input_data[groups[i]].sort()
                print(str(groups[i]) + " values(", len(AListerModule.input_data[groups[i]]) ," values): ")
                Print_String_With_Limited_Line_Length(str(AListerModule.input_data[groups[i]]))
                print()
        
        # The resultant set of a binary directional set operation has no fold changes and therefore a directionality of none.
        
            if(group_operators[i-1] == 'AND'):
                AListerModule.current_vector_values = Intersect(AListerModule.current_vector_values, 
                                                                AListerModule.input_data[groups[i]])
            elif(group_operators[i-1] == 'FAND'):
                AListerModule.current_vector_values = Fuzzy_Intersect(AListerModule.current_vector_values, 
                                                                      AListerModule.input_data[groups[i]])
            elif(group_operators[i-1] == 'OR'):
                AListerModule.current_vector_values = Union(AListerModule.current_vector_values, 
                                                            AListerModule.input_data[groups[i]])
            elif(group_operators[i-1] == 'DIFF'):
                AListerModule.current_vector_values = Difference(AListerModule.current_vector_values, 
                                                                 AListerModule.input_data[groups[i]])
            if(AListerModule.verbose):    
                AListerModule.current_vector_values.sort()
                print("The resultant vector values(", len(AListerModule.current_vector_values) ," values): ")
                Print_String_With_Limited_Line_Length(str(AListerModule.current_vector_values))
                print()
            i = i + 1
        AListerModule.input_data[v] = AListerModule.current_vector_values
    if(AListerModule.verbose):    
        print("The result values(", len(AListerModule.current_vector_values) ," values): ")
        Print_String_With_Limited_Line_Length(str(AListerModule.current_vector_values))
        print()
        
    for value in AListerModule.current_vector_values:
        AListerModule.result.append(value)
    AListerModule.result.sort()

def Intersect(a1:list, b1:list)->list:
    ''' Taken from GeeksforGeeks website.
    1) Initialize intersection I as empty.
    2) Find smaller of m and n and sort the smaller array.
    3) For every element x of larger array, do following
    b) Binary Search x in smaller array. If x is present, then copy it to I.
    4) Return I.
    
    Time complexity of this method is min(mLogm + nLogm, mLogn + nLogn) which can also be written as O((m+n)Logm, (m+n)Logn). 
    This approach works much better than the previous approach when difference between sizes of two arrays is significant.
    
    This function takes in two 1-D lists. Each entry in the list is an UPPER CASE string 
    gene/protein/methylation marker name. It then returns an intersection of these two lists. '''
    
    #1)
    intersection = []
    #2&3)
    length_a1 = len(a1)
    length_b1 = len(b1)
    if(length_a1 < length_b1):
        intersection = _Fast_Inter(a1, length_a1, b1)
    else:
        intersection = _Fast_Inter(b1, length_b1, a1)
    return intersection

def Fuzzy_Intersect(a2:list, b1:list):
    ''' This function takes in two 1-D lists. Each entry in the list is an UPPER CASE string
    gene/protein/methylation marker name. It then returns a fuzzy intersection of these two lists.'''
    #1)
    fuzzy_intersection = []
    #2&3)
    length_a2 = len(a2)
    length_b1 = len(b1)
    
    if(length_a2 < length_b1):
        fuzzy_intersection = _Fast_Fuzzy_Inter(a2, length_a2, b1)
    else:
        fuzzy_intersection = _Fast_Fuzzy_Inter(b1, length_b1, a2)
            
    return fuzzy_intersection
                 
def _Fast_Inter(a1:list, length_a1:int, b1:list):
    ''' This function efficiently computes intersection of two lists.'''
    
    intersection = []
    
    a1.sort()
    for element in b1:
        i = Binary_Search(a1, 0, length_a1-1, element)
        if(i != -1):
            if(element not in intersection):
                intersection.append(element)    
    return intersection

def _Fast_Fuzzy_Inter(a2:list, length_a2:int, b1:list):
    ''' This function efficiently computes the fuzzy intersection of two lists. '''
    fuzzy_intersection = []
    
    a2.sort()
    for element in b1:
        indeces = Binary_Similarity_Search(a2, 0, length_a2-1, element)
        if(indeces != -1):
            for i in indeces:
                cond3 = (a2[i] == element)
                if((a2[i] in fuzzy_intersection) and (element in fuzzy_intersection)):
                    pass
                else:
                    if(cond3):
                        fuzzy_intersection.append(a2[i])
                    else:
                        if(a2[i] not in fuzzy_intersection):
                            fuzzy_intersection.append(a2[i])
                        if(element not in fuzzy_intersection):
                            fuzzy_intersection.append(element)
                            
    return fuzzy_intersection

def Union(a:list, b:list)->list:
    ''' This function takes in two 1-D lists. Each entry in the list is an UPPER CASE
    string gene/protein/methylation marker name. It then returns a union of these two lists.'''
    union = set()
    
    for element in a:
        union.add(element)
    
    for element in b:
        union.add(element)
      
    return list(union)
    
def Difference(a:list, b:list)->list:
    ''' This function takes in two 1-D lists. Each entry in the list is an UPPER CASE
    string gene/protein/methylation marker name. It then returns a difference of these two lists.'''
    
    difference = []
    
    b.sort()
    for element in a:
        cond = False
        index = Binary_Search(b, 0, len(b)-1, element)
        if(index != -1):
            pass
        else:
            difference.append(element)
      
    return difference
        
        
def Binary_Search(arr:'1D-List', l:int, r:int, x:'value')->int:
    ''' Taken from GeeksforGeeks website. 
    It returns location of x in given array arr if present, else returns -1.'''
    # Inputs:
    # arr : Each entry in the list is an entity name.
    # l : left index
    # r: right index
    # x: element that we are searching for in arr list
    while l <= r:
        mid = int(l + (r - l)/2);
        arr_mid = arr[mid]
        # Check if x is present at mid
        if arr_mid == x:
            return mid
        # If x is greater, ignore left half
        elif arr_mid < x:
            l = mid + 1
        # If x is smaller, ignore right half
        else:
            r = mid - 1
    # If we reach here, then the element
    # was not present
    return -1

def Similarity_And_FirstN(arr:'1D-list', x:'value', index:int, matches:list, first_n = 3, treshold = 0.84)->'list and a boolean indicating whether any matches were found':
    ''' This functions appends to the 'matches' list the 'index' if the arr[index] is similar to 'x'.
    This function then returns the updated 'matches' list and a boolean indicating whether the element at 
    'index' in the 'arr' list is similar to 'x'. '''
    temp = 0
    if(len(arr[index]) < first_n):
        temp = len(arr[index])
    elif(len(x) < first_n):
        temp = len(x)
    else:
        temp = first_n
    # Check if x is present at mid
    cond2 = (arr[index][0:temp] == x[0:temp])
    cond1 = Similar(arr[index], x) > treshold
    if cond1 and cond2:
        matches.append(index)
    
    return matches, cond1 and cond2

def Binary_Similarity_Search(arr:'1D-list', l:int, r:int, x:'value')->list:
    ''' It returns location of all values similar to x in given array arr if present, else returns -1.'''
    # Inputs:
    # arr : Each entry in the list is an entity name.
    # l : left index
    # r: right index
    # x: element that we are searching for in arr list

    matches = []
    # This value is set to true when a value to the left of 'middle' in the arr is not similar to x.
    lFlag = False
    # This value is set to true when a value to the right of 'middle' in the arr is not similar to x.
    rFlag = False
 
    while l <= r:
 
        mid = int(l + (r - l)/2);
        arr_mid = arr[mid]
        # Check if x is present at mid
        matches, match_found = Similarity_And_FirstN(arr, x, mid, matches)
        if(match_found):   
            # We can exploit the fact that the arr list is sorted. Since any elements in arr that are similar to 
            # x must have identical first n characters all matches to x in arr list must be direct neighbors of each other.
            # Therefore, once we find a single match, we can simply iterate to the left and to the 
            # right of this match to identify all other matches. 
            
            mid2 = mid
            while(not lFlag):
                mid2 = mid2 - 1
                if(mid2 < 0):
                    lFlag = True
                elif(not lFlag):
                    matches, match_found2 = Similarity_And_FirstN(arr, x, mid2, matches)
                # If we have not found a match stop traversing the arr to the left of mid.
                if(lFlag or not match_found2):
                    lFlag = True
            
            mid3 = mid            
            while(not rFlag):
                mid3 = mid3 + 1
                if(mid3 > (len(arr)-1)):
                    rFlag = True
                elif(not rFlag):
                    matches, match_found3 = Similarity_And_FirstN(arr, x, mid3, matches)
                # If we have not found a match stop traversing the arr to the right of mid.
                if(rFlag or not match_found3):
                    rFlag = True
            return matches
                
        # If x is greater, ignore left half
        elif arr_mid < x:
            l = mid + 1
 
        # If x is smaller, ignore right half
        else:
            r = mid - 1
     
    # If we reach here, then the element
    # was not present
    return -1     

def Generate_Result_File(AListerModule):
    f = open(Path(AListerModule.output_directory)/"result.txt", "w")
    f.close()
        
def Write_Query_And_Result_List(AListerModule):
    f = open(Path(AListerModule.output_directory)/"result.txt", "a")
    f.write("Query: " + AListerModule.query_s)
    f.write('\n')
    f.close()
    
    Write_Result_To_File(AListerModule.result, AListerModule.output_directory,
                         AListerModule.output_delim) 

# OUTPUT HELPER FUNCTIONS

def Print_String_With_Limited_Line_Length(s:str):      
    length = len(s)
    j = 0
    while j < length:
        if(j+125 < length):
            print(s[j:j+125])
        else:
            print(s[j:length])
        j += 125
        
def Write_Result_To_File(a:list, out_dir:str, out_delim:str):
    ''' This functions writes out a one dimensional list to the result file. '''
    
    f = open(Path(out_dir)/'result.txt', "a")
    f.write("Number of values: (" + str(len(a)) + ")")
    f.write('\n')
    i = 0
    for element in a:
        f.write(element)
        if(out_delim == 'tab'):
            if(i < (len(a))):
                f.write('\n')
        elif(out_delim == 'comma-row'):
            if(i < (len(a)-1)):
                f.write(',')
            elif(i == (len(a)-1)):
                f.write('\n')
        else:
            raise ValueError("The output delimiter must be tab or comma-row.")
        i = i + 1
    f.write('\n')
    f.close()    
    
def Translate_Name_To_Character(name:str):
    if(name == 'comma'):
        return ','
    elif(name == 'tab'):
        return '\t'
    elif(name == 'colon'):
        return ':'
    elif(name == 'semicolon'):
        return ';'
    elif(name == 'space'):
        return ' '
    else:
        raise ValueError("Invalid input delimiter.") 
    