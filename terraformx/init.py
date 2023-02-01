import os

from terraformx.terraformx_common import *
from utils import *

def init(args):

    dir = args.dir
    var_file = args.var_file

    cwd = get_cwd(dir)
    if len(cwd) == 0:
        if not os.path.exists(cwd):
            print_error("[ERROR] Unable to locate directory.")
            return 

    tfvars_settings(cwd) 

    terraform_init(cwd, VAR_FILE=var_file)