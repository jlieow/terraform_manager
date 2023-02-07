import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from actions.github_action_terraformx_apply import *
from actions.github_action_terraformx_destroy import *

def main():

    # top-level parser
    top_level_parser = argparse.ArgumentParser(description = "terraformx")
    top_level_parser.add_argument(Args_constants.ACTIVE_STAGES, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.ACTIVE_STAGES)

    args = top_level_parser.parse_args()
    
    active_stages = args.active_stages

    cwd = os.getcwd()

    if not os.path.exists(cwd + "/backend.tf"):
        print_error("\n[ERROR] Unable to locate Terraform root in the specified directory: \n%s" % cwd)
        return
    
    tfvars_settings(cwd) 
    terraform_init(cwd)
    # destroy_only(cwd, var_file="", auto_approve=False, override_workflow=False, github_action=True)
    # apply_only(cwd, var_file="", auto_approve=False, override_workflow=False, github_action=True)

    github_action_destroy_only(cwd, var_file="", auto_approve=False, override_workflow=False, github_action_active_stages=active_stages)
    github_action_apply_only(cwd, var_file="", auto_approve=False, override_workflow=False, github_action_active_stages=active_stages)

if __name__ == "__main__":
    main()