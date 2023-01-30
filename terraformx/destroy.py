import os

from terraformx_common import *
from utils import *

def destroy(args):
    print("terraformx destroy")
    print(args)
    print(args.auto_approve)
    print(args.refresh_only)

    dir = args.dir
    auto_approve = args.auto_approve
    override_workflow = args.override_workflow
    refresh_only = args.refresh_only

    cwd = get_cwd(dir)
    if len(cwd) == 0:
        if not os.path.exists(cwd):
            print_error("[ERROR] Unable to locate directory.")
            return 

    workflow_file_exists = does_workflow_file_exist(cwd)

    tfvars_settings(cwd) 

    if workflow_file_exists:

        if not auto_approve:
            stage_workflow_terraform_destroy(cwd)

        if auto_approve and not override_workflow:
            print_warning("\n[WARNING] -auto-approve should be configured through workflow config.yaml when it is present.")
            print_warning("You may also include -override-workflow to override workflow stages auto_approve keys and auto approve every stage.")
            stage_workflow_terraform_destroy(cwd)

        if auto_approve and override_workflow:
            print_warning("\n[WARNING] All stages will be auto approved as -auto-approve and -override-workflow flags are present in the terraformx command.")
            stage_workflow_terraform_destroy(cwd, override_workflow)
            
    else:
        terraform_destroy(cwd, AUTO_APPROVE=auto_approve)