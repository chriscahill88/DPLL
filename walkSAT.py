# Import necessary libraries 
# import pylab as plt #Making plots
import time #Keeping track of time
import os #Used for looping through folder 
# import matplotlib.pyplot as plt #used for Plots
import random # used to pick random literal/clause

# Directory containing CNF files (EDIT for user specific files)
cnf_folder = "/Users/christopher/Desktop/XCode_Projects/PA3_Benchmarks/CNF Formulas/"
max_satisfied_clauses_list = []
current_dpll_times_list = []

# Function to read the CNF formula from a file
def read_cnf(file_name):
    cnf = []
    with open(file_name, 'r') as file:
        for line in file:
            # Ski
            if line.startswith('c') or line.startswith('p'):
                continue
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
            notneg = clauses[i][0] * -1 # multiplt by -1 to use as key 
            a = not Literal_map[notneg] # use positive value to find literal and flip its value to represent not symbol
        else: # if clauses literal is not negative
            a = Literal_map[clauses[i][0]] # use positive value to find literal value

        if clauses[i][1] < 0: # if clauses literal is negative
            notneg = clauses[i][1] * -1 # multiplt by -1 to use as key 
            b = not Literal_map[notneg] # use positive value to find literal and flip its value to represent not symbol
        else: # if clauses literal is not negative
            b = Literal_map[clauses[i][1]] # use positive value to find literal value

        if clauses[i][2] < 0: # if clauses literal is negative
            notneg = clauses[i][2] * -1 # multiplt by -1 to use as key  
            c = not Literal_map[notneg] # use positive value to find literal and flip its value to represent not symbol
        else: # if clauses literal is not negative
            c = Literal_map[clauses[i][2]] # use positive value to find value

        clause_map[i+1] = [a, b, c] # assign values for each literal for current index of clauses

    return clause_map # returns updated clause map 

# function that implements walkSAT Algorithm
# Parameters: clauses[][], input p value, input max flips value, number of clauses, number of literals, file name
def WALKSAT (clauses, p_val, max_flips, num_clauses, num_vars, file_name):

    global max_satisfied_clauses  # Define a global variable to keep track of max satisfied clauses
    max_satisfied_clauses = 0  # Initialize max_satisfied_clauses

    Literal_map = {} # initializes literal map {number of literals: value T/F}
    for i in range(1, num_vars+1): # iterates through every literal (works because they are in numerical order)
        Literal_map[i] = random.choice([True, False]) # randomly assigns the value to be T/F

    clause_maps = {} # initializes clause map {num_clauses index: list of T/F values that reflects literal values}
    clause_maps = clause_map(clause_maps, Literal_map) # calls function to update clause map based on literal values

    # tells user initial clauses that are true out of number of clauses
    print(f"initial true clauses: {clauses_true(clause_maps, num_clauses)}/{num_clauses}")

    for i in range(1, max_flips+1): # iterates through max number of flips, each loop is 1 flip

        # checks if solved
        if clauses_true(clause_maps, num_clauses) == num_clauses:
            print(f"solution found for: {file_name}")
            print(f"final true clauses: {clauses_true(clause_maps, num_clauses)}/{num_clauses}")
            # keeps track of satisfied clauses for graph purposes
            num_satisfied_clauses = clauses_true(clause_maps, num_clauses) 
            max_satisfied_clauses = max(max_satisfied_clauses, num_satisfied_clauses) #
            return Literal_map # returns solution set of literals

        random_clause, s = rand_clause(clause_maps, num_clauses) # selects random clause with all falses {False, False, False}
        index = random.randint(0, 2) # generate random # from 0 to the index of literals per clause minus 1

        # print(f"random clause values: {random_clause}, index in num_clauses: {s}") # random clause of falses and its index within num_clauses
        # print(f"clause: {clauses[s-1]}, index on random literal: {index}") # random index 0-range of literals 
        # print(f"random literal: {clauses[s-1][index]}\n")
        # print(f"value of literal(+): {Literal_map.get(clauses[s-1][index])}") # {random Literal: boolean value} = True or False
        # print(f"value of literal(-): {Literal_map.get(-1*(clauses[s-1][index]))}")   
        # print(f"literal map: {Literal_map}\n")

        if random.random() < p_val: # if random value ranging from 0.0-1.0 is less than p value

            print(f"flip {i}: Random flip") # tracks current flip and says its random

            if clauses[s-1][index] > 0: # if literal is positive

                # print(clause_maps)
                # print(f"run: {i}, start clauses true: {clauses_true(clause_maps, num_clauses)}")

                Literal_map[clauses[s-1][index]] = not Literal_map[clauses[s-1][index]] # flip literals value
                clause_maps = clause_map(clause_maps, Literal_map) # update clause map

                # print(f"run: {i}, result clauses true: {clauses_true(clause_maps, num_clauses)}")
                #print(clause_maps)

            elif clauses[s-1][index] < 0: # if literal is negative 

                #print(clause_maps)
                # print(f"run: {i}, start clauses true: {clauses_true(clause_maps, num_clauses)}")

                a = clauses[s-1][index] * -1 # set to positive to use as key
                Literal_map[a] = not Literal_map[a] # flip literals value
                clause_maps = clause_map(clause_maps, Literal_map) # update clause map

                # print(f"run: {i}, result clauses true: {clauses_true(clause_maps, num_clauses)}")
                #print(clause_maps)

        else: # if random value is larger than p 

            print(f"flip {i}: Greedy flip") # tracks current flip and says its greedy

            temp, save_k = 0, 0 # tracks largest value of true clauses and index of the literal that achieved that
            for k in range(1, num_vars+1): # iterate through every literal
                
                Literal_map_temp = {} # empty temp literal map
                Literal_map_temp = Literal_map.copy() # assign it to actual literal map
                Literal_map_temp[k] = not Literal_map_temp[k] # invert current literal in temp literal map

                clause_maps_temp = {} # create temp clause map to test current set of literals
                clause_maps_temp = clause_maps.copy() # assign it to actual clause map
                clause_maps_temp = clause_map(clause_maps_temp, Literal_map_temp) # update temp clause map to represent temp literal

                if clauses_true(clause_maps_temp, num_clauses) > temp: # if current literals true clauses result is larger than previous
                    temp = clauses_true(clause_maps_temp, num_clauses) # update temp to equal newest max clauses achieved
                    save_k = k # update to current index of literal that achieved it
                    # print(f"k is: {save_k}, flip val at k to: {Literal_map_temp[k]}, results in clauses true: {temp}")

    print(f"no solution found for: {file_name}") # if solution is never found in previous loop and it is exited, return this by default
    print(f"final true clauses: {clauses_true(clause_maps, num_clauses)}/{num_clauses}") # show resulting clauses true achieved
    return None # returned by default if no solution 

# Loops through all files in cnf folder
for file_name in os.listdir(cnf_folder): 
    if file_name.startswith("uf20-0"): # only loop through files that start with "uf20-0"
        cnf_path = os.path.join(cnf_folder, file_name) 
        clauses = read_cnf(cnf_path) # set clauses = to the cnf found in current file
        num_vars = max(max(abs(lit) for lit in clause) for clause in clauses) # num of literals
        num_clauses = len(clauses) # num of clauses

        assignment = {} # make empty clause
        print(f"\nProcessing file: {file_name}") # tracks current file being solved

        # Run DPLL algorithm and record time
        start = time.time() # start time
        result = WALKSAT(clauses, 0.7, 100, num_clauses, num_vars, file_name) # calls walkSAT algorithm, set p: 0.7, max flip: 100
        stop = time.time() # stop time
        current_dpll_times = stop - start # total time

        if result is not None: # if solved
            # used for graphing purposes
            num_satisfied_clauses = sum(1 for clause in clauses )
            max_satisfied_clauses_list.append(num_satisfied_clauses)

        # add times to list for graphing purposes
        current_dpll_times_list.append(current_dpll_times)

'''
# making Graph
print("Size of max_satisfied_clauses_list:", len(max_satisfied_clauses_list))
print("Size of current_dpll_times_list:", len(current_dpll_times_list))
plt.figure(figsize=(10, 6))
plt.scatter(max_satisfied_clauses_list, current_dpll_times_list)
plt.xlabel('Max Satisfied Clauses')
plt.ylabel('Time (seconds)')
plt.title('DPLL Performance')
plt.show()
'''