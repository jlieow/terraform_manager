import csv
import os 
import sys

def get_dir_of_terraform_manager_from_sys_executable():
    terraform_manager_path = get_dir_of_terraform_manager_from_sys_executable_onefile(sys.executable)

    if not os.path.exists(terraform_manager_path):
        terraform_manager_path = get_dir_of_terraform_manager_from_sys_executable_onedir(sys.executable)
    
    while not os.path.basename(terraform_manager_path) == "terraform_manager":
        terraform_manager_path = os.path.dirname(terraform_manager_path)

    return terraform_manager_path


def get_dir_of_terraform_manager_from_sys_executable_onefile(directory):
    return os.path.dirname(os.path.dirname(os.path.dirname(directory)))

def get_dir_of_terraform_manager_from_sys_executable_onedir(directory):
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(directory))))

def input_options(preface, options, input_question, return_input=False, use_prev_as_default=False, choice=None, allow_special_break=False, special_break = ""):
    print(preface)
    for i in range(len(options)):
        print("%d. %s" % (i+1, options[i]))
     
    if choice != None:
        choice += 1
    
    while True:
        try:
            # Place a %s expression in your input question to print the default
            if use_prev_as_default:
                choice = input(input_question % choice) or choice
            else:
                choice = input(input_question)

            # Allows users a special return for custom behaviours such as breaking out of a loop
            if allow_special_break and choice == special_break:
                return special_break

            # Use to raise TypeError()
            choice = int(choice)

            # If input is more than len of array, throw exception
            if choice > len(options):
                raise ValueError()

        except (ValueError, TypeError):
            print("Please key in a numeric value up to %d." % len(options))
            continue
        else:
            break
            
    if return_input:
        return choice
    return choice - 1

def get_rows_as_list(path):
    rows = []
    # Read the CSV contents to a list     
    with open(path, 'rt') as f:  
        for row in csv.reader(f):
            rows.append(row)
    
    return rows
