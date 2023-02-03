import os

from terraformx.terraformx_common import *
from utils import *

def apply_rebuild_true(cwd, var_file):

    print_warning("\n[WARNING] terraformx will rebuild the resources by first destroying and then applying the Terraform script.")

    if does_workflow_file_exist(cwd):

        if len(var_file) > 0:
                print_warning("\n[WARNING] -var-file flag will be ignored as a workflow file is detected. The -var-file referenced is located in config/settings.tfvars.")
                
        stage_workflow_terraform_destroy(cwd, override_workflow=True)
        stage_workflow_terraform_apply(cwd, override_workflo=True)
        return
    else:
        terraform_destroy(cwd, CUSTOM_VAR_FILE=var_file)
        terraform_apply(cwd, CUSTOM_VAR_FILE=var_file, AUTO_APPROVE=True)
        return

def apply_rebuild_false(cwd, var_file, auto_approve, override_workflow):
    if does_workflow_file_exist(cwd):

            if len(var_file) > 0:
                print_warning("\n[WARNING] -var-file flag will be ignored as a workflow file is detected. The -var-file referenced is located in config/settings.tfvars.")

            if not auto_approve:
                stage_workflow_terraform_apply(cwd)

            if auto_approve and not override_workflow:
                print_warning("\n[WARNING] -auto-approve should be configured through workflow config.yaml when it is present.")
                print_warning("You may also include -override-workflow to override workflow stages auto_approve keys and auto approve every stage.")
                stage_workflow_terraform_apply(cwd)

            if auto_approve and override_workflow:
                print_warning("\n[WARNING] All stages will be auto approved as -auto-approve and -override-workflow flags are present in the terraformx command.")
                stage_workflow_terraform_apply(cwd, override_workflow)
            
            return

    else:
        terraform_apply(cwd, CUSTOM_VAR_FILE=var_file, AUTO_APPROVE=auto_approve)
        return



def apply(args):

    chdir = args.chdir
    var_file = args.var_file
    auto_approve = args.auto_approve
    override_workflow = args.override_workflow
    refresh_only = args.refresh_only
    rebuild = args.rebuild
    

    cwd = get_cwd(chdir)
    if len(cwd) == 0:
        if not os.path.exists(cwd):
            print_error("[ERROR] Unable to locate directory.")
            return 

    tfvars_settings(cwd) 

    if rebuild:
        apply_rebuild_true(cwd, var_file)
        return
    else:
        apply_rebuild_false(cwd, var_file, auto_approve, override_workflow)
        return