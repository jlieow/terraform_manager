import csv
import os 
import sys
import time

class Common_constants:
    TERRAFORM_MANAGER = "terraform_manager"

# def get_dir_of_terraform_manager_from_sys_executable():
#     terraform_manager_path = get_dir_of_terraform_manager_from_sys_executable_onefile(sys.executable)

#     if not os.path.exists(terraform_manager_path):
#         terraform_manager_path = get_dir_of_terraform_manager_from_sys_executable_onedir(sys.executable)
    
#     while not os.path.basename(terraform_manager_path) == Common_constants.TERRAFORM_MANAGER:
#         terraform_manager_path = os.path.dirname(terraform_manager_path)

#         if len(terraform_manager_path) < len(Common_constants.TERRAFORM_MANAGER):
#             return

#     return terraform_manager_path


def check_if_terraform_manager_root_is_valid(directory):
    while not os.path.basename(directory) == Common_constants.TERRAFORM_MANAGER:
        directory = os.path.dirname(directory)

        if len(directory) < len(Common_constants.TERRAFORM_MANAGER):
                return ""
    
    if os.path.exists(os.path.join(directory, "utils")) and os.path.exists(os.path.join(directory, "data")) and os.path.exists(os.path.join(directory, "terraformx")):
        return directory
    
    return ""
        

def get_dir_of_terraform_manager():

    # Returns root dir where python script or exe is run from
    FILE_PATH = os.path.realpath(__file__)
    EXE_PATH = sys.executable

    if len(check_if_terraform_manager_root_is_valid(FILE_PATH)) > 0:
        terraform_manager_path = FILE_PATH
    elif len(check_if_terraform_manager_root_is_valid(EXE_PATH)) > 0:
        terraform_manager_path = EXE_PATH
    else:
        return ""

    while not os.path.basename(terraform_manager_path) == Common_constants.TERRAFORM_MANAGER:
        terraform_manager_path = os.path.dirname(terraform_manager_path)

        if len(terraform_manager_path) < len(Common_constants.TERRAFORM_MANAGER):
            return

    return terraform_manager_path

# def get_dir_of_terraform_manager_from_sys_executable_onefile(directory):
#     return os.path.dirname(os.path.dirname(os.path.dirname(directory)))

# def get_dir_of_terraform_manager_from_sys_executable_onedir(directory):
#     return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(directory))))

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

def getcwd():
    # getcwd()() breaks when used in an exe created by pyinstaller
    # determine if application is a script file or frozen exe and use correct path
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    elif __file__:
        return os.path.dirname(__file__)
    
def get_env_object():
    if sys.platform == "win32":
        import nt
        return nt.environ
    else:
        return os.environ
