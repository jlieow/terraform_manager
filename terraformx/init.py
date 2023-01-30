import os

from terraformx_common import *
from utils import *

def init(args):
    print("terraformx init")

    dir = args.dir

    cwd = get_cwd(dir)
    if len(cwd) == 0:
        if not os.path.exists(cwd):
            print_error("[ERROR] Unable to locate directory.")
            return 

    tfvars_settings(cwd) 

    terraform_init(cwd)