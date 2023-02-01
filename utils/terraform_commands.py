import os
import glob
import subprocess

from .common import *
from .history import *

# ----- CONSTANTS ----- #

class Terraform_commands_constants:
    TERRAFORM_PARSER = 'terraform'
    BACKEND_CONFIG_FILE = 'backend.tfvars'
    TERRAFORMX_VAR_FILE = 'config/settings.tfvars'

    INIT = 'init'
    APPLY = 'apply'
    DESTROY = 'destroy'
    PLAN = 'plan'
    AUTO_APPROVE = '-auto-approve'
    REFRESH_ONLY = '-refresh-only'


    INIT_PROCESS = [TERRAFORM_PARSER, INIT, '-backend-config=%s' % BACKEND_CONFIG_FILE]
    OUTPUT_PROCESS = [TERRAFORM_PARSER, 'output']
    APPLY_PROCESS = [TERRAFORM_PARSER, APPLY, '-var-file=%s' % TERRAFORMX_VAR_FILE]
    APPLY_AUTO_APPROVE_PROCESS = [TERRAFORM_PARSER, APPLY, '-var-file=%s' % TERRAFORMX_VAR_FILE, AUTO_APPROVE]
    DESTROY_PROCESS = [TERRAFORM_PARSER, DESTROY, '-var-file=%s' % TERRAFORMX_VAR_FILE]
    DESTROY_AUTO_APPROVE_PROCESS = [TERRAFORM_PARSER, DESTROY, '-var-file=%s' % TERRAFORMX_VAR_FILE, AUTO_APPROVE]
    APPLY_REFRESH_PROCESS = [TERRAFORM_PARSER, APPLY, REFRESH_ONLY, '-var-file=%s' % TERRAFORMX_VAR_FILE]
    APPLY_REFRESH_AUTO_APPROVE_PROCESS = [TERRAFORM_PARSER, APPLY, REFRESH_ONLY, '-var-file=%s' % TERRAFORMX_VAR_FILE, AUTO_APPROVE]
    PLAN_REFRESH_PROCESS = [TERRAFORM_PARSER, PLAN, REFRESH_ONLY, '-var-file=%s' % TERRAFORMX_VAR_FILE]

    TERRAFORM_COMMAND_PREFACE = "The following terraform commands can be invoked:\n"
    TERRAFORM_COMMAND_OPTIONS = "\nWhich command would you like to invoke: "
    LIST_TERRAFORM_COMMAND=[
        "terraform init",
        "terraform apply",
        "terraform destroy",
        "terraform destroy and apply -auto-approve",
        "terraform output",
        "terraform apply -refresh-only",
        "terraform plan -refresh-only",
    ]

# ----- CONSTANTS ----- #

# Find all tfvars files in the terraform root
# Concat all the located tfvars files
# Place the results in /config/settings.tfvars
def tfvars_settings(cwd):
    filenames = glob.glob(cwd + "/*.tfvars")   

    if not os.path.exists(cwd + "/config"):
        os.mkdir(cwd + "/config")

    with open(cwd + "/" + Terraform_commands_constants.TERRAFORMX_VAR_FILE, 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
                #Add a newline so that variables are separated
                outfile.write("\n")
                # Remove newline at the end of the file
                infile.read().rstrip('\n')  

def terraform_init(cwd, CUSTOM_VAR_FILE="", set_stdin=None, set_stdout=None, set_stderr=None):

    init_process = Terraform_commands_constants.INIT_PROCESS
    if len(CUSTOM_VAR_FILE) > 0:   
        init_process = [Terraform_commands_constants.TERRAFORM_PARSER, 'init', '-backend-config=%s' % CUSTOM_VAR_FILE]

    subprocess.Popen(init_process, cwd=cwd, stdin=set_stdin, stdout=set_stdout, stderr=set_stderr).wait()

def terraform_apply(cwd, CUSTOM_VAR_FILE="", AUTO_APPROVE=False, set_stdin=None, set_stdout=None, set_stderr=None):

    tfvars_settings(cwd)

    add_history(cwd)

    apply_auto_approve_process = Terraform_commands_constants.APPLY_AUTO_APPROVE_PROCESS
    apply_process = Terraform_commands_constants.APPLY_PROCESS
    if len(CUSTOM_VAR_FILE) > 0:   
        apply_auto_approve_process = [Terraform_commands_constants.TERRAFORM_PARSER, Terraform_commands_constants.APPLY, '-var-file=%s' % CUSTOM_VAR_FILE, AUTO_APPROVE]
        apply_process = [Terraform_commands_constants.TERRAFORM_PARSER, Terraform_commands_constants.APPLY, '-var-file=%s' % CUSTOM_VAR_FILE]
    
    if AUTO_APPROVE:
        process = subprocess.Popen(apply_auto_approve_process, cwd=cwd, stdin=set_stdin, stdout=set_stdout, stderr=set_stderr).wait()
    else:
        process = subprocess.Popen(apply_process, cwd=cwd, stdin=set_stdin, stdout=set_stdout, stderr=set_stderr).wait()

    if process == 1:
        # If the process experiences an error, skip the remaining commands
        return 1

    terraform_apply_auto_approve_refresh(cwd)

def terraform_destroy(cwd, CUSTOM_VAR_FILE="", AUTO_APPROVE=False, set_stdin=None, set_stdout=None, set_stderr=None):

    tfvars_settings(cwd)

    destroy_auto_approve_process = Terraform_commands_constants.DESTROY_AUTO_APPROVE_PROCESS
    destroy_process = Terraform_commands_constants.DESTROY_PROCESS
    if len(CUSTOM_VAR_FILE) > 0:   
        destroy_auto_approve_process = [Terraform_commands_constants.TERRAFORM_PARSER, Terraform_commands_constants.DESTROY, '-var-file=%s' % CUSTOM_VAR_FILE, AUTO_APPROVE]
        destroy_process = [Terraform_commands_constants.TERRAFORM_PARSER, Terraform_commands_constants.DESTROY, '-var-file=%s' % CUSTOM_VAR_FILE]

    if AUTO_APPROVE:
        process = subprocess.Popen(destroy_auto_approve_process, cwd=cwd, stdin=set_stdin, stdout=set_stdout, stderr=set_stderr).wait()
    else:
        process = subprocess.Popen(destroy_process, cwd=cwd, stdin=set_stdin, stdout=set_stdout, stderr=set_stderr).wait()

    if process == 1:
        # If the process experiences an error, skip the remaining commands
        return 1

    delete_latest_row_from_history(cwd)

def terraformOutput(cwd, set_stdin=None, set_stdout=None, set_stderr=None):
    tfvars_settings(cwd)
    subprocess.Popen(Terraform_commands_constants.OUTPUT_PROCESS, cwd=cwd, stdin=set_stdin, stdout=set_stdout, stderr=set_stderr).wait()

def terraform_apply_refresh(cwd, AUTO_APPROVE=False):
    tfvars_settings(cwd)
    if AUTO_APPROVE:
        process = subprocess.Popen(Terraform_commands_constants.APPLY_REFRESH_AUTO_APPROVE_PROCESS, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()
    else:
        process = subprocess.Popen(Terraform_commands_constants.APPLY_REFRESH_PROCESS, cwd=cwd).wait()

    if process == 1:
        # If the process experiences an error, skip the remaining commands
        return 1

def terraform_plan_refresh(cwd):
    tfvars_settings(cwd)
    return subprocess.Popen(Terraform_commands_constants.PLAN_REFRESH_PROCESS, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def terraform_apply_auto_approve_refresh(cwd):
    tfvars_settings(cwd)
    
    print("\nPerforming -apply-refresh to sync statefile and match the current provisioned state")
    subprocess.Popen(Terraform_commands_constants.APPLY_REFRESH_AUTO_APPROVE_PROCESS, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()

    # if input("\nEnter Y if you would you like to invoke \"terraform apply -refresh-only\" to the drifted Terraform Roots' state to match the current provisioned state: ").upper() == "Y":
    #     for index in range(len(drifted_terraform_roots)):
    #         cwd = drifted_terraform_roots[index]

    #         print("Invoking -refresh-only on %s" % os.path.basename(cwd))
    #         terraform_apply_refresh(cwd)
            # subprocess.Popen(APPLY_REFRESH_PROCESS, cwd=cwd).wait()

def locate_terraform_root_directories(root_directory):
    
    # root_directory = get_parent_dir(os.getcwd())
    list_terraform_root_dir = []

    # Get list of files and directories present in root directory
    # Search for backend.tf file in the directory
    # If backend.tf exists, get its parent directory and append it to a list
    for directory in os.listdir(root_directory):
        
        path = root_directory + "/" + directory + "/backend.tf"

        does_backend_tf_exist = glob.glob(path)
        if len(does_backend_tf_exist) != 0:
            list_terraform_root_dir.append(get_parent_dir(does_backend_tf_exist[0]))

    list_terraform_root_dir.sort()

    return list_terraform_root_dir