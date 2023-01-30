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
            cwd = os.getcwd + dir
        if not os.path.exists(cwd):
            print_error("[ERROR] Unable to locate directory.")
            return ""

        return cwd