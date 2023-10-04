# Import necessary libraries
import seaborn as sns
import pandas as pd
import pylab as plt
import numpy as np
import itertools
import random
import time

# Function to read the CNF formula from a file
def read_cnf(file_name):
    cnf = []
    with open(file_name, 'r') as file:
        for line in file:
            # Skip comments and problem specification lines
            if line.startswith('c') or line.startswith('p'):
                continue
            # Break when '%' is encountered (end of clauses)
            if line.startswith('%'):
                break
            clause = set()  # Change to set
            literals = line.strip().split()[:-1]
            for literal in literals:
                value = int(literal)
                is_negated = False
                if value < 0:
                    value = abs(value)
                    is_negated = True
                clause.add((value, is_negated))  # Change to add
            cnf.append(clause)  # Append the set to cnf

    return cnf

# Function to select a literal from the CNF formula
def _select_literal(clauses, assignment):
    # Count the occurrences of each literal
    literal_counts = {}

    for clause in clauses:
        for literal in clause:
            if literal not in assignment:
                if literal in literal_counts:
                    literal_counts[literal] += 1
                else:
                    literal_counts[literal] = 1

    # Sort the literals by their occurrence count in descending order
    sorted_literals = sorted(literal_counts, key=lambda x: literal_counts[x], reverse=True)

    # Select the first unassigned literal
    for literal in sorted_literals:
        if literal not in assignment:
            return literal

    return None

# Function to check if a clause is true given an assignment
def is_clause_true(clause, assignment):
    for variable, is_negated in clause:
        if variable in assignment:
            if is_negated:
                value = not assignment[variable]
            else:
                value = assignment[variable]
            if value:
                return True
    return False

# DPLL algorithm for solving CNF formulas
def DPLL(cnf, assignment):
    # Check if all clauses are true with the current assignment
    #print("Check if all clauses are true with the current assignment")
    if all(is_clause_true(clause, assignment) for clause in cnf):
        print("All clauses are true, returning assignment")
        return assignment

    # Check if there is an empty clause, indicating a conflict
    if any(len(clause) == 0 for clause in cnf):
        print("Found an empty clause, backtracking")
        return None

    # Find an unassigned variable (v) in the first clause
    unassigned = next((v for clause in cnf for v, _ in clause if v not in assignment), None)


    # If no unassigned variable is found, the formula is satisfied
    if unassigned is None:
        #print("No unassigned variable found, returning")
        return None

    # Try assigning the variable (v) as True
    new_assignment = dict(assignment)
    new_assignment[unassigned] = True
    print(f"Trying {unassigned} = True")
    result = DPLL(cnf, new_assignment)
    if result is not None:
        return result

    # Try assigning the variable (v) as False
    new_assignment = dict(assignment)
    new_assignment[unassigned] = False
    print(f"Trying {unassigned} = False")
    result = DPLL(cnf, new_assignment)
    if result is not None:
        return result

    # If both True and False assignments lead to conflicts, backtrack
    return None


# Function to get the variable from a literal
def get_variable_from_literal(literal):
    return abs(literal)

# Read CNF formula from file
file_name = "/Users/christopher/Desktop/XCode_Projects/PA3_Benchmarks/CNF Formulas/uf20-0157.cnf"
cnf = read_cnf(file_name)  # Call read_cnf function

# Initialize assignment
assignment = {}

# Call DPLL with the CNF formula and initial assignment
result = DPLL(cnf, assignment)

# Print the result
if result is not None:
    print("Satisfying assignment:", result)
else:
    print("No satisfying assignment found.")
