# Import necessary libraries
#import pylab as plt #Making plots
import time #Keeping track of time
import os #Used for looping through folder 
#import matplotlib.pyplot as plt #used for Plots
import random

# Directory containing CNF files (EDIT for user specific files)
cnf_folder = "/Users/christopher/Desktop/XCode_Projects/PA3_Benchmarks/CNF Formulas/"
max_satisfied_clauses_list = []
current_dpll_times_list = []
# Function to read the CNF formula from a file
def read_cnf(file_name):
    cnf = []
    with open(file_name, 'r') as file:
        for line in file:
            # Skip over the c's and p's
            if line.startswith('c') or line.startswith('p'):
                continue
            #end when % is hit
            if line.startswith('%'):
                break
            clause = [int(x) for x in line.strip().split()[:-1]]
            cnf.append(clause)
    return cnf

# Function that returns the numbers of clauses that have at least one true in them
def clauses_true(clause_map, num_clauses):
    count = 0 # tracks true clauses
    for i in range(1, num_clauses+1): # iterates through every clause
        if any(clause_map[i]): # if any literal within clause is true
            count += 1 # increment count by 1
    return count # returns total clauses true

# Picks a random clause that has all literals equaling false
def rand_clause(clause_map, num_clauses):
    for i in range(1, num_clauses+1): # iterates through every clause
            if not any(clause_map[i]): # if any literal within clause is not true
                return clause_map[i], i # return clause and index of clause within clause_map

# creates/updates clause map to reflect current definition of literal map
# {num_clauses index: list of T/F values that reflects literal values}
def clause_map(clause_map, Literal_map):
    for i in range(0, num_clauses): # iterates through every clause and its literals

        if clauses[i][0] < 0: # if clauses literal is negative
            notneg = clauses[i][0] * -1 # multiplt by -1 to make positive 
            a = not Literal_map[notneg] # use positive value to find literal and flip its value to represent not symbol
        else: # if clauses literal is not negative
            a = Literal_map[clauses[i][0]] # use positive value to find literal value

        if clauses[i][1] < 0: # if clauses literal is negative
            notneg = clauses[i][1] * -1 # multiplt by -1 to make positive 
            b = not Literal_map[notneg] # use positive value to find literal and flip its value to represent not symbol
        else: # if clauses literal is not negative
            b = Literal_map[clauses[i][1]] # use positive value to find literal value

        if clauses[i][2] < 0: # if clauses literal is negative
            notneg = clauses[i][2] * -1 # multiplt by -1 to make positive 
            c = not Literal_map[notneg] # use positive value to find literal and flip its value to represent not symbol
        else: # if clauses literal is not negative
            c = Literal_map[clauses[i][2]] # use positive value to find value

        clause_map[i+1] = [a, b, c] # assign values for each literal for current index of clauses

    return clause_map # returns updated clause map 

# function that implements walkSAT Algorithm
# parameters: clauses[][], user inout max tries, user input max flips
def GSAT (clauses, Max_Tries, Max_Flips): 

    for i in range(1, Max_Tries+1): # Loop Max_Tries number of times
        
        s = i
        Literal_map = {} # initializes literal map {number of literals: value T/F}
        for i in range(1, num_vars+1): # iterates through every literal (works because they are in numerical order)
            Literal_map[i] = random.choice([True, False]) # randomly assigns the value to be T/F


        # initialize clause map and set each literal in clauses value based on +/- sign
        clause_maps = {} # initializes clause map {num_clauses index: list of T/F values that reflects literal values}
        clause_maps = clause_map(clause_maps, Literal_map) # calls function to update clause map based on literal values

        for j in range(1, Max_Flips+1): # Loop Max_Flips number of times per current set of literals
            
            print("\nATTEMPTING NEW FLIP:") #New Flip
            print(f"current try (i): {s}") #prints current try
            print(f"current flip (j): {j}") #prints current flip

            #testing to see if solution was found
            if clauses_true(clause_maps, num_clauses) == num_clauses: # if clauses true is max, return literals
                print("\n!!! solution found !!!\n") 
                return Literal_map 

            # Find the variable that, when flipped, will result in 
            # the maximum increase in the number of satisfied clauses

            # which flipped literal results in the highest number for clauses_true
            temp, save_k = 0, 0
            #Printing how many clauses are true Before flip
            print(f"current tries initial clauses true: {clauses_true(clause_maps, num_clauses)}\n")
            #Pick flip that gives more true clauses
            print("PICKING BEST FLIPPED LITERAL:")
            for k in range(2, num_vars+1): # for the current literal (1 through num_vars)
                
                Literal_map_temp = {} # empty temp literal map
                Literal_map_temp = Literal_map.copy() # assign it to actual literal map
                Literal_map_temp[k] = not Literal_map_temp[k] # invert current literal in temp literal map

                clause_maps_temp = {} # create temp clause map to test current set of literals
                clause_maps_temp = clause_maps.copy()#copy map
                clause_maps_temp = clause_map(clause_maps_temp, Literal_map_temp) # update temp clause map to represent temp literal

                if clauses_true(clause_maps_temp, num_clauses) > temp:#Finding flip that gives the most true clauses
                    temp = clauses_true(clause_maps_temp, num_clauses) #marking the most amount of true clauses to compare to other flips
                    save_k = k #Saving the index that gives the most correct clauses
                    print(f"k is: {save_k}, flip val at k to: {Literal_map_temp[k]}, results in clauses true: {temp}") #Print which index gave the most true clauses and how many true clauses
            
            # Invert the value of the key `save_k` in the `Literal_map` dictionary
            Literal_map[save_k] = not Literal_map[save_k] 
            # Update `clause_maps` using the modified `Literal_map`
            clause_maps = clause_map(clause_maps, Literal_map)
            # Print the number of clauses that are currently true
            print(f"clauses true: {clauses_true(clause_maps, num_clauses)}")
            # Check if this is the last try and flip
            if s == Max_Tries and j == Max_Flips:
                if clauses_true(clause_maps, num_clauses) == num_clauses: #If the solution was found
                    print("\n!!! solution found !!!\n")
                    # If all clauses are true, return the current Literal_map as a solution
                    return Literal_map
                else:
                    print("\n!!! max tries and flips reached; no solution found !!!\n")
                    #If max tries and flips are reached and not all clauses are true, return None (no solution found)
                    return None
#Loops through all the files in CNF Formula
for file_name in os.listdir(cnf_folder):
    if file_name.startswith("uf20-0"):#Only looping through files that start with uf20-0
        cnf_path = os.path.join(cnf_folder, file_name)
        clauses = read_cnf(cnf_path) #Set clauses equal to the CNF found in the current file
        num_vars = max(max(abs(lit) for lit in clause) for clause in clauses)
        num_clauses = len(clauses) #num of clauses

        assignment = {}#Make empty array
        print(f"Processing file: {file_name}")#Used to track which file is currently being solved

        # Run DPLL algorithm and record time
        start = time.time()#start time
        result = GSAT(clauses, 50, 2000) #Run GSAT (CNF,Max Tries, Max Flips) Max Tries and Max flips can be edited higher so it always solve
        stop = time.time()#Stop time
        current_dpll_times = stop - start #Calculate runtime

        if result is not None: #If solved
            #Used for graphing purposes
            num_satisfied_clauses = sum(1 for clause in clauses )
            max_satisfied_clauses_list.append(num_satisfied_clauses)

        current_dpll_times_list.append(current_dpll_times)# Add Times to list for graphing purposes

'''
#making Graph
plt.figure(figsize=(10, 6))
plt.scatter(max_satisfied_clauses_list, current_dpll_times_list)
plt.xlabel('Max Satisfied Clauses')
plt.ylabel('Time (seconds)')
plt.title('GSAT Performance')
plt.show()
'''