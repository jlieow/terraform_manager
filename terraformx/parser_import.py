import os

from terraformx.terraformx_common import *
from terraformx.parser_blueprints import *
from utils import *

def t_import(args):

    chdir = args.chdir
    var_file = args.var_file
    address = args.address
    id = args.id
    
    cwd = get_cwd(chdir)
    if len(cwd) == 0:
        if not os.path.exists(cwd):
            print_error("[ERROR] Unable to locate directory.")
            return 

    tfvars_settings(cwd) 

    ## For now var_file does not work
    if len(var_file) > 0:
        print_warning("\n[WARNING] -var-file flag will be ignored as a workflow file is detected. The -var-file referenced is located in config/settings.tfvars.")

    terraform_import(cwd, address, id)
    
    return