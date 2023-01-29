import csv

from .common import *
from .print_options import *

# ----- CONSTANTS ----- #

HISTORY_CSV_PATH = "./data/history/terraform_history.csv"

# ----- CONSTANTS ----- #

def add_history(cwd, stage_name="", unit_testing=False, unit_testing_path=""):

    path = HISTORY_CSV_PATH

    if unit_testing is True:
        path = unit_testing_path

    #Save results to CSV    
    with open(path, 'a', newline='') as f:  
        # using csv.writer method from CSV package
        write = csv.writer(f)
        
        write.writerow([cwd, stage_name])
        f.close()

def delete_latest_row_from_history(cwd, stage_name="", unit_testing=False, unit_testing_path=""):
    
    path = HISTORY_CSV_PATH

    if unit_testing is True:
        path = unit_testing_path

    history = []
    
    # Read the CSV contents to a list     
    with open(path, 'rt') as f:  
        for row in csv.reader(f):
            history.append(row)
            # print(row)

    for index in range(len(history)):
        
        reverseIndex = len(history)-index-1

        # print("reversed: %s, row: %s" %(history[reverseIndex][0], deleteRow))
        if history[reverseIndex] == [cwd, stage_name]:
            history.pop(reverseIndex)
            # print(reverseIndex)
            break

    # Write the rows back to the csv file
    with open(path, 'w', newline='') as f:  
        # using csv.writer method from CSV package
        write = csv.writer(f)
        
        write.writerows(history)
        f.close()

