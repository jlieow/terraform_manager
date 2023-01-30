import os
from utils import *

def apply(args):
    # print("terraformx apply")
    # print(args)
    # print(args.var_file)
    # print(args.auto_approve)
    # print(args.refresh_only)

    dir = args.dir
    auto_approve = args.auto_approve
    refresh_only = args.refresh_only

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

    if does_workflow_file_exist(cwd):

        if auto_approve:
            print_warning("-auto-approve must be configured through workflow config.yaml when it is present.")

        stage_workflow_terraform_apply(cwd)
    else:
        terraform_apply(cwd, AUTO_APPROVE=auto_approve)

