import os
import glob
import subprocess

from utils.common import *
from utils.history import *
from utils.common import getcwd

# ----- CONSTANTS ----- #

class Terraform_commands_constants:
    TERRAFORM_PARSER = 'terraform'
    BACKEND_CONFIG_FILE = 'backend.tfvars'
    TERRAFORMX_VAR_FILE = os.path.join('config', 'settings.tfvars')

    INIT = 'init'
    MIGRATE_STATE = '-migrate-state'
    APPLY = 'apply'
    DESTROY = 'destroy'
    PLAN = 'plan'
    IMPORT = 'import'
    STATE = 'state'
    AUTO_APPROVE = '-auto-approve'
    REFRESH_ONLY = '-refresh-only'

    ENV = get_env_object()

    INIT_PROCESS = [TERRAFORM_PARSER, INIT]
    OUTPUT_PROCESS = [TERRAFORM_PARSER, 'output']
    APPLY_PROCESS = [TERRAFORM_PARSER, APPLY, '-var-file=%s' % TERRAFORMX_VAR_FILE]
    APPLY_AUTO_APPROVE_PROCESS = [TERRAFORM_PARSER, APPLY, '-var-file=%s' % TERRAFORMX_VAR_FILE, AUTO_APPROVE]
    DESTROY_PROCESS = [TERRAFORM_PARSER, DESTROY, '-var-file=%s' % TERRAFORMX_VAR_FILE]
    DESTROY_AUTO_APPROVE_PROCESS = [TERRAFORM_PARSER, DESTROY, '-var-file=%s' % TERRAFORMX_VAR_FILE, AUTO_APPROVE]
    REFRESH_PROCESS = [TERRAFORM_PARSER, APPLY, REFRESH_ONLY, '-var-file=%s' % TERRAFORMX_VAR_FILE]
    REFRESH_AUTO_APPROVE_PROCESS = [TERRAFORM_PARSER, APPLY, REFRESH_ONLY, '-var-file=%s' % TERRAFORMX_VAR_FILE, AUTO_APPROVE]
    PLAN_REFRESH_PROCESS = [TERRAFORM_PARSER, PLAN, REFRESH_ONLY, '-var-file=%s' % TERRAFORMX_VAR_FILE]
    IMPORT_PROCESS = [TERRAFORM_PARSER, IMPORT,'-var-file=%s' % TERRAFORMX_VAR_FILE]
    STATE_PROCESS = [TERRAFORM_PARSER, STATE]

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
    if not is_dir_a_terraform_root(cwd):
        return

    filenames = glob.glob(os.path.join(cwd, "*.tfvars"))   

    if not os.path.exists(os.path.join(cwd, "config")):
        os.mkdir(os.path.join(cwd, "config"))

    with open(os.path.join(cwd, Terraform_commands_constants.TERRAFORMX_VAR_FILE), 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
                #Add a newline so that variables are separated
                outfile.write("\n")
                # Remove newline at the end of the file
                infile.read().rstrip('\n')  

def terraform_init(cwd, migrate_state, CUSTOM_VAR_FILE="", set_stdin=None, set_stdout=None, set_stderr=None):

    init_process = Terraform_commands_constants.INIT_PROCESS
    if migrate_state:
        init_process = Terraform_commands_constants.INIT_MIGRATE_STATE_PROCESS

    # Assign default backend file but use custom backend file if it exists
    backend_tfvars = glob.glob(os.path.join(cwd, "backend.tfvars"))
    if len(backend_tfvars) > 0:
        init_process = [Terraform_commands_constants.TERRAFORM_PARSER, 'init', '-backend-config=%s' % Terraform_commands_constants.BACKEND_CONFIG_FILE]

    if len(CUSTOM_VAR_FILE) > 0:   
        init_process = [Terraform_commands_constants.TERRAFORM_PARSER, 'init', '-backend-config=%s' % CUSTOM_VAR_FILE]

    subprocess.Popen(init_process, cwd=cwd, stdin=set_stdin, stdout=set_stdout, stderr=set_stderr, env=Terraform_commands_constants.ENV).wait()

def terraform_apply(cwd, CUSTOM_VAR_FILE="", AUTO_APPROVE=False, github_action=False, set_stdin=None, set_stdout=None, set_stderr=None):

    tfvars_settings(cwd)
    
    if not github_action:
        add_history(cwd)

    apply_auto_approve_process = Terraform_commands_constants.APPLY_AUTO_APPROVE_PROCESS
    apply_process = Terraform_commands_constants.APPLY_PROCESS
    if len(CUSTOM_VAR_FILE) > 0:   
        apply_auto_approve_process = [Terraform_commands_constants.TERRAFORM_PARSER, Terraform_commands_constants.APPLY, '-var-file=%s' % CUSTOM_VAR_FILE, Terraform_commands_constants.AUTO_APPROVE]
        apply_process = [Terraform_commands_constants.TERRAFORM_PARSER, Terraform_commands_constants.APPLY, '-var-file=%s' % CUSTOM_VAR_FILE]
    
    if AUTO_APPROVE:
        process = subprocess.Popen(apply_auto_approve_process, cwd=cwd, stdin=set_stdin, stdout=set_stdout, stderr=set_stderr, env=Terraform_commands_constants.ENV).wait()
    else:
        process = subprocess.Popen(apply_process, cwd=cwd, stdin=set_stdin, stdout=set_stdout, stderr=set_stderr, env=Terraform_commands_constants.ENV).wait()

    if process == 1:
        # If the process experiences an error, skip the remaining commands
        return 1

    print("\nPerforming apply -refresh-only to sync statefile and match the current provisioned state")
    terraform_refresh(cwd, AUTO_APPROVE=True)

def terraform_destroy(cwd, CUSTOM_VAR_FILE="", AUTO_APPROVE=False, github_action=False, set_stdin=None, set_stdout=None, set_stderr=None):

    tfvars_settings(cwd)

    destroy_auto_approve_process = Terraform_commands_constants.DESTROY_AUTO_APPROVE_PROCESS
    destroy_process = Terraform_commands_constants.DESTROY_PROCESS
    if len(CUSTOM_VAR_FILE) > 0:   
        destroy_auto_approve_process = [Terraform_commands_constants.TERRAFORM_PARSER, Terraform_commands_constants.DESTROY, '-var-file=%s' % CUSTOM_VAR_FILE, Terraform_commands_constants.AUTO_APPROVE]
        destroy_process = [Terraform_commands_constants.TERRAFORM_PARSER, Terraform_commands_constants.DESTROY, '-var-file=%s' % CUSTOM_VAR_FILE]

    if AUTO_APPROVE:
        process = subprocess.Popen(destroy_auto_approve_process, cwd=cwd, stdin=set_stdin, stdout=set_stdout, stderr=set_stderr, env=Terraform_commands_constants.ENV).wait()
    else:
        process = subprocess.Popen(destroy_process, cwd=cwd, stdin=set_stdin, stdout=set_stdout, stderr=set_stderr, env=Terraform_commands_constants.ENV).wait()

    if process == 1:
        # If the process experiences an error, skip the remaining commands
        return 1
    # Do not delete history if command is invoked from github action
    # Github action does not store the terraform history directory or file
    if not github_action:
        delete_latest_row_from_history(cwd)

def terraform_output(cwd, set_stdin=None, set_stdout=None, set_stderr=None):
    tfvars_settings(cwd)
    subprocess.Popen(Terraform_commands_constants.OUTPUT_PROCESS, cwd=cwd, stdin=set_stdin, stdout=set_stdout, stderr=set_stderr, env=Terraform_commands_constants.ENV).wait()

def terraform_refresh(cwd, AUTO_APPROVE=False):
    tfvars_settings(cwd)
    if AUTO_APPROVE:
        process = subprocess.Popen(Terraform_commands_constants.REFRESH_AUTO_APPROVE_PROCESS, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=Terraform_commands_constants.ENV).wait()
    else:
        process = subprocess.Popen(Terraform_commands_constants.REFRESH_PROCESS, cwd=cwd, env=Terraform_commands_constants.ENV).wait()

    if process == 1:
        # If the process experiences an error, skip the remaining commands
        return 1

def terraform_plan_refresh(cwd):
    tfvars_settings(cwd)
    return subprocess.Popen(Terraform_commands_constants.PLAN_REFRESH_PROCESS, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=Terraform_commands_constants.ENV)

def is_dir_a_terraform_root(base_dir):
    path = os.path.join(base_dir, "*.tf")

    tf_files = glob.glob(path)
    if len(tf_files) != 0:
        return True
    
    return False

def locate_terraform_root_directories(root_directory):
    
    # root_directory = os.path.dirname(getcwd())
    list_terraform_root_dir = []

    # Get list of directories present in root directory
    # Check if directory is a terraform root
    # If it is, append it to a list
    for directory in os.listdir(root_directory):
        base_dir = os.path.join(root_directory, directory)
        
        if is_dir_a_terraform_root(base_dir):
            list_terraform_root_dir.append(base_dir)

    list_terraform_root_dir.sort()

    return list_terraform_root_dir

def terraform_import(cwd, stringvars):

    import_process = Terraform_commands_constants.IMPORT_PROCESS + stringvars

    subprocess.Popen(import_process, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=Terraform_commands_constants.ENV).wait()

def terraform_state_rm(cwd, stringvars):

    if stringvars[0] != "rm":
        print_error("Performing terraform state rm, but we have detected an issue with the command.")
        return

    state_rm_process = Terraform_commands_constants.STATE_PROCESS + stringvars

    subprocess.Popen(state_rm_process, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=Terraform_commands_constants.ENV).wait()