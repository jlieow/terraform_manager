import os

from terraformx.terraformx_common import *
from terraformx.parser_blueprints import *
from utils import *

def state_rm(args):

    chdir = args.chdir
    stringvars = args.stringvars

    cwd = get_cwd(chdir)
    if len(cwd) == 0:
        if not os.path.exists(cwd):
            print_error("[ERROR] Unable to locate directory.")
            return 
        
    tfvars_settings(cwd) 

    terraform_state_rm(cwd, stringvars)
    
    return

def state(args):
    stringvars = args.stringvars

    if stringvars[0] == "rm":
        state_rm(args)