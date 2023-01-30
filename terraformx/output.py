import os
from utils import *

def output(args):
    print("terraformx output")

    dir = args.dir

    # Determine which directory to use
    # Use current directory
    # Use specified directory from sub path
    # Use specified directory with full path
    if len(dir) == 0:
        cwd = os.getcwd()
    else:
        cwd = dir
        if not os.path.exists(cwd):
            cwd = os.getcwd + dir
        if not os.path.exists(cwd):
            print_error("[ERROR] Unable to locate directory.")
            return 

    tfvars_settings(cwd) 

    terraform_init(cwd)