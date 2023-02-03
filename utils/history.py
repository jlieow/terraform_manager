import os
import csv
import sys

from .common import *
from .print_options import *

# ----- CONSTANTS ----- #

HISTORY_CSV_PATH = "/data/history/terraform_history.csv"

# ----- CONSTANTS ----- #

def list_history(histories, turn_high_alert_on=True):

    if len(histories) == 0:
        print_warning("\nThere is no record of anything being provisioned based on your history. The program will now exit.")
        return

    # ----- WARNING ----- #
    if turn_high_alert_on:
        print_high_alert("\n!!! THIS IS A DESTRUCTIVE ACTION !!!\
        \nContinuing will invoke \"terraform destroy --auto-approve\" on the folders in the following order:\n"
        )

    for i in range(len(histories)):
        reverseIndex = len(histories) - i - 1

        cwd = histories[reverseIndex][0]
        stage_name = histories[reverseIndex][1]

        if len(stage_name) == 0:  
            print("%d. %s" % (i+1, os.path.basename(cwd)))
        else:
            print("%d. %s - Stage \"%s\"" % (i+1, os.path.basename(cwd), stage_name))

def add_history(cwd, stage_name="", unit_testing=False, unit_testing_path=""):
    
    history_path = get_dir_of_terraform_manager_from_sys_executable() + HISTORY_CSV_PATH

    if unit_testing is True:
        history_path = unit_testing_path

    #Save results to CSV    
    with open(history_path, 'a', newline='') as f:  
        # using csv.writer method from CSV package
        write = csv.writer(f)
        
        write.writerow([cwd, stage_name])
        f.close()

def delete_latest_row_from_history(cwd, stage_name="", unit_testing=False, unit_testing_path=""):

    history_path = get_dir_of_terraform_manager_from_sys_executable_onefile(sys.executable) + HISTORY_CSV_PATH

    if not os.path.exists(history_path):
        history_path = get_dir_of_terraform_manager_from_sys_executable_onedir(sys.executable) + HISTORY_CSV_PATH


    if unit_testing is True:
        history_path = unit_testing_path

    history = []
    
    # Read the CSV contents to a list     
    with open(history_path, 'rt') as f:  
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
    with open(history_path, 'w', newline='') as f:  
        # using csv.writer method from CSV package
        write = csv.writer(f)
        
        write.writerows(history)
        f.close()

