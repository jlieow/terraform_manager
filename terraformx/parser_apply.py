import os

from terraformx.terraformx_common import *
from terraformx.parser_blueprints import *
from utils import *

def apply_rebuild_true(cwd, var_file):

    warning_message_describing_terraformx_rebuild = "\n[WARNING] terraformx will rebuild the resources by first destroying and then applying the Terraform script."

    warning_message_initiating_destroy = "\n Terrafrom destroying..."
    warning_message_initiating_apply = "\n Terrafrom applying..."

    print_warning(warning_message_describing_terraformx_rebuild)

    if does_workflow_file_exist(cwd):

        if len(var_file) > 0:
                print_warning("\n[WARNING] -var-file flag will be ignored as a workflow file is detected. The -var-file referenced is located in config/settings.tfvars.")
        
        print_warning(warning_message_initiating_destroy)
        stage_workflow_terraform_destroy(cwd, override_workflow=True)

        print_warning(warning_message_initiating_apply)
        stage_workflow_terraform_apply(cwd, override_workflow=True)
        return
    else:
        print_warning(warning_message_initiating_destroy)
        terraform_destroy(cwd, CUSTOM_VAR_FILE=var_file, github_action=True)

        print_warning(warning_message_initiating_apply)
        terraform_apply(cwd, CUSTOM_VAR_FILE=var_file, AUTO_APPROVE=True, github_action=True)
        return

def apply_only(cwd, var_file, auto_approve, override_workflow):

    if does_workflow_file_exist(cwd):

        if len(var_file) > 0:
            print_warning("\n[WARNING] -var-file flag will be ignored as a workflow file is detected. The -var-file referenced is located in config/settings.tfvars.")

        if not auto_approve:
            stage_workflow_terraform_apply(cwd)
            return

        if auto_approve and not override_workflow:
            print_warning("\n[WARNING] -auto-approve should be configured through workflow config.yaml when it is present.")
            print_warning("You may also include -override-workflow to override workflow stages auto_approve keys and auto approve every stage.")
            stage_workflow_terraform_apply(cwd)
            return

        if auto_approve and override_workflow:
            print_warning("\n[WARNING] All stages will be auto approved as -auto-approve and -override-workflow flags are present in the terraformx command.")
            stage_workflow_terraform_apply(cwd, override_workflow)
            return

    else:
        terraform_apply(cwd, CUSTOM_VAR_FILE=var_file, AUTO_APPROVE=auto_approve, github_action=True)
        return

def blueprints(blueprint_file, create):

    blueprint_path = get_full_path_else_return_empty_str(blueprint_file, ".csv")

    if not os.path.exists(blueprint_path):
        if input("\nBlueprint file not found. Enter \"Y\" to create a blueprint: ").upper() == "Y":
            blueprint_path = os.getcwd() + "/" + blueprint_file + ".csv"
            create_blueprint(blueprint_path)
        return
    
    if create:
        create_blueprint(blueprint_path)
        return
    else:
        apply_blueprint(blueprint_path)
        return

def apply(args):

    chdir = args.chdir
    var_file = args.var_file
    auto_approve = args.auto_approve
    override_workflow = args.override_workflow
    refresh_only = args.refresh_only
    rebuild = args.rebuild
    blueprint = args.blueprint
    create = args.create
    

    cwd = get_cwd(chdir)
    if len(cwd) == 0:
        if not os.path.exists(cwd):
            print_error("[ERROR] Unable to locate directory.")
            return 

    tfvars_settings(cwd) 

    if len(blueprint) > 0:
        blueprints(blueprint, create)
        return

    if rebuild:
        apply_rebuild_true(cwd, var_file)
        return
    else:
        apply_only(cwd, var_file, auto_approve, override_workflow)
        return