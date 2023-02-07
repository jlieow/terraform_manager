import os

from terraformx.terraformx_common import *
from utils import *

def github_action_destroy_only(cwd, var_file, auto_approve, override_workflow, github_action_active_stages=""):
    if does_workflow_file_exist(cwd):

        print_warning("\n[WARNING] All stages will be auto approved regardless of the configuration present in workflow/config.yaml")
        github_action_stage_workflow_terraform_destroy(cwd, override_workflow=True, active_stages_statements=github_action_active_stages)
        return

    else:
        print("\ngithub_action no workflow")
        terraform_destroy(cwd, CUSTOM_VAR_FILE="", AUTO_APPROVE=True, github_action=True)
        return

def destroy_only(cwd, var_file, auto_approve, override_workflow, github_action=False):

    if github_action:
        if does_workflow_file_exist(cwd):

            print_warning("\n[WARNING] All stages will be auto approved regardless of the configuration present in workflow/config.yaml")
            stage_workflow_terraform_destroy(cwd, override_workflow=True, github_action=True)
            return

        else:
            print("\ngithub_action no workflow")
            terraform_destroy(cwd, CUSTOM_VAR_FILE="", AUTO_APPROVE=True, github_action=True)
            return

    if does_workflow_file_exist(cwd):

        if len(var_file) > 0:
            print_warning("\n[WARNING] -var-file flag will be ignored as a workflow file is detected. The -var-file referenced is located in config/settings.tfvars.")

        if not auto_approve:
            stage_workflow_terraform_destroy(cwd)
            return

        if auto_approve and not override_workflow:
            print_warning("\n[WARNING] -auto-approve should be configured through workflow config.yaml when it is present.")
            print_warning("You may also include -override-workflow to override workflow stages auto_approve keys and auto approve every stage.")
            stage_workflow_terraform_destroy(cwd)
            return

        if auto_approve and override_workflow:
            print_warning("\n[WARNING] All stages will be auto approved as -auto-approve and -override-workflow flags are present in the terraformx command.")
            stage_workflow_terraform_destroy(cwd, override_workflow)
            return
            
    else:
        terraform_destroy(cwd, CUSTOM_VAR_FILE=var_file, AUTO_APPROVE=auto_approve)
        return

def destroy(args):

    chdir = args.chdir
    var_file = args.var_file
    auto_approve = args.auto_approve
    override_workflow = args.override_workflow
    refresh_only = args.refresh_only
    destroy_history = args.destroy_history

    cwd = get_cwd(chdir)
    if len(cwd) == 0:
        if not os.path.exists(cwd):
            print_error("[ERROR] Unable to locate directory.")
            return 

    tfvars_settings(cwd) 

    if destroy_history:
        terraform_destroy_from_history()
        return

    destroy_only(cwd, var_file, auto_approve, override_workflow, github_action=False)