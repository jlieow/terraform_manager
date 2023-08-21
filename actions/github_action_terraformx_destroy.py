import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from terraformx.terraformx import *
from utils.common import getcwd

def github_action_destroy_only(cwd, var_file, auto_approve, override_workflow, github_action_active_stages=""):
    if does_workflow_file_exist(cwd):

        print_warning("\n[WARNING] All stages will be auto approved regardless of the configuration present in workflow/config.yaml")
        github_action_stage_workflow_terraform_destroy(cwd, override_workflow=True, active_stages_statements=github_action_active_stages)
        return

    else:
        print("\ngithub_action no workflow")
        terraform_destroy(cwd, CUSTOM_VAR_FILE="", AUTO_APPROVE=True, github_action=True)
        return

def main():

    # top-level parser
    top_level_parser = argparse.ArgumentParser(description = "terraformx")
    top_level_parser.add_argument(Args_constants.ACTIVE_STAGES, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.ACTIVE_STAGES)

    args = top_level_parser.parse_args()
    
    active_stages = args.active_stages
    
    cwd = getcwd()

    if is_dir_a_terraform_root(cwd):
        print_error("\n[ERROR] Unable to locate Terraform root in the specified directory: \n%s" % cwd)
        return
    
    tfvars_settings(cwd) 
    terraform_init(cwd)
    # destroy_only(cwd, var_file="", auto_approve=False, override_workflow=False, github_action=True)
    github_action_destroy_only(cwd, var_file="", auto_approve=False, override_workflow=False, github_action_active_stages=active_stages)

if __name__ == "__main__":
    main()