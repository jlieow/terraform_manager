import os

from utils import *

# Determine which directory to use
# Use current directory
# Use specified directory from sub path
# Use specified directory with full path
# Returns empty string if no cwd found
def get_cwd(dir):

    if len(dir) == 0:
        return os.getcwd()
    else:
        cwd = dir
        if not os.path.exists(cwd):
            cwd = os.path.join(os.getcwd(), dir)
        if not os.path.exists(cwd):
            print_error("[ERROR] Unable to locate directory.")
            return ""

        return cwd

def get_full_path_else_return_empty_str(path, optional_ext=""):

    # Check if it is a full path
    # Check if it is a relative directory with a starting "/"
    # Check if it is a relative directory without a starting "/"
    
    working_path = path
    if not os.path.exists(working_path):
        working_path = os.path.join(getcwd(), path)
    if not os.path.exists(working_path):
        working_path = os.path.join(getcwd(), path + optional_ext)
    if not os.path.exists(working_path):
        return ""

    return os.path.abspath(working_path)