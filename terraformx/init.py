import os

from terraformx.terraformx_common import *
from utils import *

def init(args):

    chdir = args.chdir
    var_file = args.var_file

    cwd = get_cwd(chdir)
    if len(cwd) == 0:
        if not os.path.exists(cwd):
            print_error("[ERROR] Unable to locate directory.")
            return 

    tfvars_settings(cwd) 

    terraform_init(cwd, CUSTOM_VAR_FILE=var_file)