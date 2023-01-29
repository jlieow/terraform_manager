import os
from utils import *

def terraform_apply():
    print("workflow_apply")

def workflow_apply():
    print("workflow_apply")

def apply(args):
    # print("terraformx apply")
    # print(args)
    # print(args.var_file)
    # print(args.auto_approve)
    # print(args.refresh_only)

    var_file = args.var_file
    auto_approve = args.auto_approve
    refresh_only = args.refresh_only

    cwd = os.getcwd()
    workflow_file_exists = does_workflow_file_exist(cwd)

    if workflow_file_exists:
        stage_workflow_terraform_apply(cwd)
    else:
        terraform_apply(cwd)

