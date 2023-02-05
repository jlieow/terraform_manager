import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from terraformx.parser_destroy import *

def main():
    cwd = os.getcwd()

    if not os.path.exists(cwd + "/backend.tf"):
        print_error("\n[ERROR] Unable to locate Terraform root in the specified directory: \n%s" % cwd)
        return
    
    tfvars_settings(cwd) 
    terraform_init(cwd)
    destroy_only(cwd, var_file="", auto_approve=False, override_workflow=False, github_action=True)

if __name__ == "__main__":
    main()