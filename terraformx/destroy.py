import os
from utils import *

def destroy(args):
    print("terraformx destroy")
    print(args)
    print(args.var_file)
    print(args.auto_approve)
    print(args.refresh_only)

    dir = args.dir
    var_file = args.var_file
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

    workflow_file_exists = does_workflow_file_exist(cwd)

    tfvars_settings(cwd) 

    if workflow_file_exists:

        if auto_approve:
            print_warning("-auto-approve must be configured through workflow config.yaml when it is present.")
            
        stage_workflow_terraform_destroy(cwd, VAR_FILE=var_file)
    else:
        terraform_destroy(cwd, AUTO_APPROVE=auto_approve, VAR_FILE=var_file)