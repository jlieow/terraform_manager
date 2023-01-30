import yaml
import hcl
import glob

from .terraform_commands import *
from .print_options import *
from .history import *

# ----- CONSTANTS ----- #

WORKFLOW_CONFIG_LOCATION = "/workflow/config.yaml"

TERRAFORM_COMMAND_PREFACE = "The following terraform commands can be invoked:\n"
TERRAFORM_COMMAND_OPTIONS = "\nWhich command would you like to invoke: "
LIST_TERRAFORM_COMMAND=[
    "terraform init",
    "terraform apply -target",
    "terraform destroy -target",
    "terraform destroy and apply -auto-approve",
    "terraform output",
    "terraform apply -refresh-only",
]
TERRAFORM_COMMAND_OPTIONS_DEFAULT = "\nWhich command would you like to invoke? The default is currently [%s]: "

WORKFLOW_CONFIG_DETECTED_MESSAGE = "\nA workflow config has been detected!\
                \nPlease note that when invoking \"terraform apply\" and \"terraform destroy\" commands, they will use targets as specified in the workflow/config.yaml\n"

# ----- CONSTANTS ----- #

def is_workflow_file_ignored(path):
    if os.path.exists(path):
        with open(path, 'r') as stream:
            data_loaded = yaml.safe_load(stream)

            # print(data_loaded)

            if "ignore" in data_loaded:
                if data_loaded["ignore"] == True:
                    return True

    return False

# Not being used currently
def is_stage_auto_approve(path):
    with open(path, 'r') as stream:
        data_loaded = yaml.safe_load(stream)

    for index in range(len(data_loaded["stages"])):
        if "auto_approve" in data_loaded["stages"][index]:
            auto_approve = data_loaded["stages"][index]["auto_approve"]
            print("auto_approve")
            print(auto_approve)

    print(data_loaded)
    if "auto_approve" in data_loaded:
        if data_loaded["auto_approve"] == True:
            return True

    return False

def does_stage_name_exist(cwd, stage_name):
    workflow_path =  cwd + WORKFLOW_CONFIG_LOCATION
    
    with open(workflow_path, 'r') as stream:
        data_loaded = yaml.safe_load(stream)

    stages = data_loaded["stages"]

    stage_names = [stages[index]["name"].strip() for index in range(len(stages)) ]
    
    if stage_name not in stage_names:
        return False
    else:
        return True

def get_active_stages_from_workflow(cwd):

    # does_stage_name_contain_special_characters(cwd)

    workflow_path =  cwd + WORKFLOW_CONFIG_LOCATION

    with open(workflow_path, 'r') as stream:
        data_loaded = yaml.safe_load(stream)

    active_stages = []
    # missing_stage_name = []
    # stage_names = []

    if "active_stages" in data_loaded:

        # Checks based on numbers
        active_statements = str(data_loaded["active_stages"])
        # Splits and Strips white spaces
        statements = [item.strip() for item in active_statements.split(",")]

        if "0" in statements:
            return [], True, "Active stages have to start from 1." 

        # numeric_statements = []
        # string_statements = []
        # for statement in statements:
        #     if "\"" in statement:
        #         string_statements.append(statement.strip("\""))
        #     else:
        #         numeric_statements.append(statement)

        for numeric_statement in statements:
            numeric_statement = numeric_statement.strip()

            if numeric_statement.isnumeric():
                active_stage = int(numeric_statement) - 1
                active_stages.append(active_stage)

            for element in ["-", "to"]:
                if element in numeric_statement:
                    start_end = numeric_statement.split(element)
                    start = start_end[0].strip()
                    end = start_end[1].strip()

                    if start.isnumeric() and end.isnumeric():
                        start = int(start) - 1
                        end = int(end)
                        active_stages =  active_stages + list(range(start, end))
        
        # Checks based on stage name
        # stages = data_loaded["stages"]

        # for index in range(len(stages)):
        #     stage = stages[index]
        #     stage_name = str(stage["name"]).strip()
        #     stage_names.append(stage_name)
        
        #     if stage_name in string_statements:
        #         active_stages.append(index)

        # print("stages")
        # print(stages)
        # print("string_statements")
        # print(string_statements)
        # #TODO refactor error checking

        # for string_statement in string_statements:
        #     if string_statement not in stage_names:
        #         missing_stage_name.append(string_statement)
    
    # Flag errors
    # if len(missing_stage_name) > 0:
    #     err_message = "\nThe following stage names are declared in the workflow's \"active\" field but they do not exist:"
    #     for stage_name in missing_stage_name:
    #         err_message = err_message + "\n%s" % stage_name

    #     err_message = err_message + "\n\nPlease fix the error(s) before continuing."

    #     err = True
    #     return [], err, err_message

    # if max(active_stages) > len(stages) - 1:
    #     err_message = "\nThere are only %d workflow stage(s). However, stage %d has been declared in the workflow's \"active\" field and is out of range." % (len(stages), max(active_stages) + 1)
    #     err_message = err_message + "\n\nPlease fix the error(s) before continuing."
    #     err = True
    #     return [], err, err_message

    # Removes duplicates
    active_stages = set(active_stages)
    active_stages = list(active_stages)

    err = False
    err_message = ""

    return active_stages, err, err_message

def get_active_stage_names_from_workflow(cwd):

    # does_stage_name_contain_special_characters(cwd)

    workflow_path =  cwd + WORKFLOW_CONFIG_LOCATION

    with open(workflow_path, 'r') as stream:
        data_loaded = yaml.safe_load(stream)

    active_stages = []
    missing_stage_name = []
    stage_names = []

    if "active_stage_names" in data_loaded:

        # Checks based on numbers
        active_statements = data_loaded["active_stage_names"]
        
        # Python detects "active_stage_names: " as type None
        # Python detects "active_stage_names: None" as string None
        # TODO consider implementing this in get_active_stages_from_workflow() too 
        if active_statements is None:
            return [], False, ""
        
        active_statements = str(data_loaded["active_stage_names"])

        # Splits and Strips white spaces
        statements = [item.strip() for item in active_statements.split(",")]

        # Checks based on stage name
        stages = data_loaded["stages"]

        for index in range(len(stages)):
            stage = stages[index]
            stage_name = str(stage["name"]).strip()
            stage_names.append(stage_name)
        
            if stage_name in statements:
                active_stages.append(index)

        #TODO refactor error checking

        for string_statement in statements:
            if string_statement not in stage_names:
                missing_stage_name.append(string_statement)
    
    # Flag errors
    if len(missing_stage_name) > 0:
        err_message = "\nThe following stage names are declared in the workflow's \"active\" field but they do not exist:"
        for stage_name in missing_stage_name:
            err_message = err_message + "\n%s" % stage_name

        err_message = err_message + "\n\nPlease fix the error(s) before continuing."

        err = True
        return [], err, err_message


    # Removes duplicates
    active_stages = set(active_stages)
    active_stages = list(active_stages)

    err = False
    err_message = ""

    return active_stages, err, err_message

def get_active_stages_and_stage_names_from_workflow(cwd):
    active_stages, err, err_message = get_active_stages_from_workflow(cwd)

    if err:
        return active_stages, err, err_message

    active_stage_names, err, err_message = get_active_stage_names_from_workflow(cwd)

    if err:
        return active_stage_names, err, err_message

    active = set(active_stages + active_stage_names)
    active = list(active)
    
    err = False
    err_message = ""

    return active, err, err_message

def get_stages_to_apply_from_active_stages(active_stages, stages):
    
    if len(active_stages) == 0:
        return stages

    if max(active_stages) > len(stages):
        print_warning("\n[WARNING] The number of declared active stages are higher than the actual number of workflow stages! So active stages will be ignored.")
        return stages

    new_stages = []

    for level in active_stages:
        new_stages = new_stages + [stages[level]]

    return new_stages

def does_workflow_file_exist(cwd):
    # Get csv files from blueprints directory
    path =  cwd + WORKFLOW_CONFIG_LOCATION
    workflow = glob.glob(path)
    
    if is_workflow_file_ignored(path):
        return False

    if len(workflow) > 0:
        return True

    return False

def get_number_of_resources_from_workflow(workflow_config_path):
    with open(workflow_config_path, 'r') as stream:
        data_loaded = yaml.safe_load(stream)

    number_of_resources = 0
    for stage in data_loaded["stages"]:
        for resource in stage["targets"]:
            # print("resource:%s" % resource)
            for item in resource:
                # print("item:%s" % item)
                # print("len(resource[item]:%s" % len(resource[item]))
                number_of_resources += len(resource[item])
    return number_of_resources

def get_number_of_resources_from_maintf(main_tf_path):
    with open(main_tf_path, 'r') as fp:
        obj = hcl.load(fp)
    
    number_of_resources = 0
    
    # Add number of modules 
    if "module" in obj:
        number_of_resources += len(obj["module"])
    # Add number of resources
    if "resource" in obj:
        for resource in obj["resource"]: 
            number_of_resources += len(obj["resource"][resource])

    return number_of_resources

def get_list_of_resources_from_workflow(workflow_config_path):
    with open(workflow_config_path, 'r') as stream:
        data_loaded = yaml.safe_load(stream)

    list_of_resources = []

    if "stages" in data_loaded:
        for stage in data_loaded["stages"]:
            # print("stage:%s" % stage)
            if "targets" in stage:
                for target in stage["targets"]:
                    # print("target:%s" % target)
                    for resource in target:
                        # print("resource:%s" % resource)
                        for item in target[resource]:
                            # print("item:%s" % item)

                            list_of_resources.append("%s.%s" % (resource,item))
                
    return list_of_resources

def get_list_of_resources_from_maintf(maintf_path):
    with open(maintf_path, 'r') as fp:
        obj = hcl.load(fp)
    
    list_of_resources = []
    
    # Add modules to list 
    if "module" in obj:
        for item in obj["module"]:
            list_of_resources.append("module.%s" % item)
    # Add resources to list 
    if "resource" in obj:
        for resource in obj["resource"]: 
            for item in obj["resource"][resource]:
                list_of_resources.append("resource.%s.%s" % (resource,item))

    return list_of_resources

def does_workflow_file_contain_duplicates(workflow_resources):
    # Check if config.yaml contains duplicate terraform objects
    if len(workflow_resources) != len(set(workflow_resources)):
        # Get duplicates with set so that only one copy of the duplicated element is saved
        # Convert set to list as sets do not support indexing
        dup = {x for x in workflow_resources if workflow_resources.count(x) > 1}
        dup = list(dup)

        print_error("\n[ERROR] Please check config.yaml. The following duplicate terraform objects are found in config.yaml:")
        for index in range(len(dup)):
            print("%d. %s" % (index+1, dup[index]))
        
        return True
    return False

def does_workflow_objects_exist_in_maintf(workflow_resources, maintf_resources, disable_print=False):
    # Check if terraform objects in config.yaml exist in main.tf
    # If they do not, it will result in either an error during provisioning or objects that are not provisioned

    diff = set(workflow_resources) - set(maintf_resources)
    diff = list(diff)

    if len(diff) > 0:
        print_error("\n[ERROR] Please check your config.yaml as it would result in an error when performing \"terraform apply\".\
            \nThe following terraform objects in config.yaml do not exist in main.tf:", disable_print)
        
        for index in range(len(diff)):
            print_error("%d. %s" % (index+1, diff[index]), disable_print)

        return False
    
    return True

def does_workflow_contain_error_and_warnings(cwd, disable_print=False):
    workflow_path =  cwd + WORKFLOW_CONFIG_LOCATION
    maintf_path =  cwd + "/main.tf"
    
    number_of_workflow_resources = get_number_of_resources_from_workflow(workflow_path)
    number_of_maintf_resources = get_number_of_resources_from_maintf(maintf_path)

    workflow_resources = get_list_of_resources_from_workflow(workflow_path)
    maintf_resources = get_list_of_resources_from_maintf(maintf_path)

    workflow_resources.sort()
    maintf_resources.sort()
    
    # print(workflow_resources)
    # print(maintf_resources)

    # --- error --- #
    if does_workflow_file_contain_duplicates(workflow_resources):
        return True
    # print("passed duplicate check")

    if does_workflow_objects_exist_in_maintf(workflow_resources, maintf_resources) == False:
        return True
    # print("workflow objects exist in main.tf")

    _, stages_errors = get_stages(cwd)

    if check_stages_errors(stages_errors):
        return True

    # --- warnings --- #
    if number_of_workflow_resources < number_of_maintf_resources:
        print_warning("[WARNING] Please check your config.yaml.\
            \nIt is detected that the following resource(s) in main.tf are not present in config.yaml.\n")

        index = 1
        for resource in maintf_resources:
            if resource not in workflow_resources:
                print_warning("%d. %s" % (index, resource)) 
                index += 1

        print_warning("\nProceeding means that some objects may not be provisioned.\n")

    return False

def get_targets(test):
    targets = []
    for target in test:
        for key in target:
            for value in target[key]:
                targets.append("%s.%s" % (key, value))
                # targets.append("-target=\"%s.%s\"" % (key, value))
                # Applying "-target="" can be performed here instead of a separate function applyTargetResources()
    return targets

def get_stage(cwd, stage_name):

    workflow_path = cwd + "/workflow/config.yaml"

    error = False

    stage_auto_approve_error_message = ""

    with open(workflow_path, 'r') as stream:
        data_loaded = yaml.safe_load(stream)

    for stage in data_loaded["stages"]:

        if "name" in stage:
            if stage["name"] == stage_name:
                try: 
                    if stage["auto_approve"] is not True or False or None:
                        raise TypeError
                    else:
                        stage_auto_approve = stage["auto_approve"] if "auto_approve" in stage and stage["auto_approve"] is not None else False
                except:
                    stage_auto_approve_error_message = "[ERROR] The value for key \"auto_approve\" in workflow config yaml needs to be a boolean."
                    error = True
                    stage_auto_approve = False 

                stage_targets = get_targets(stage["targets"])

    stage = {
            "stage_name":stage_name,
            "stage_auto_approve":stage_auto_approve,
            "stage_targets":stage_targets,
            }

    stage_errors = {
            "error": error,
            "stage_name": "",
            "stage_auto_approve": stage_auto_approve_error_message,
            "stage_targets": "",
            }

    return stage

def get_stages(cwd):

    workflow_path =  cwd + WORKFLOW_CONFIG_LOCATION

    with open(workflow_path, 'r') as stream:
        data_loaded = yaml.safe_load(stream)

    stages = []
    stages_errors = []
    error = False

    stage_auto_approve_error_message = ""

    for stage in data_loaded["stages"]:
        
        stage_name = stage["name"] if "name" in stage else None

        try: 
            stage_auto_approve = stage["auto_approve"] if "auto_approve" in stage and stage["auto_approve"] is not None else False
            if not (isinstance(stage_auto_approve, bool) or stage_auto_approve == None):
                raise TypeError

        except Exception as e:
            stage_auto_approve_error_message = "[ERROR] The value for key \"auto_approve\" in workflow config yaml needs to be a boolean."
            error = True
            stage_auto_approve = False

        stage_targets = get_targets(stage["targets"])

        stages.append({
            "stage_name":stage_name,
            "stage_auto_approve": stage_auto_approve,
            "stage_targets":stage_targets,
            })
        
        stages_errors.append({
            "error": error,
            "stage_name": stage_name,
            "stage_auto_approve_error_message": stage_auto_approve_error_message,
            "stage_targets": "",
            })

    return stages, stages_errors

def workflow_terraform_apply(cwd, stage_targets, stage_name, VAR_FILE="", AUTO_APPROVE=False):
    tfvars_settings(cwd)
    
    add_history(cwd, stage_name)
    
    target_process = ["-target=" + sub for sub in stage_targets]

    if len(VAR_FILE) > 0:
        apply_auto_approve_process = [TERRAFORM_PATH, 'apply', '-var-file=%s' % VAR_FILE, '-auto-approve']
        apply_process = [TERRAFORM_PATH, 'apply', '-var-file=%s' % VAR_FILE]
    else:
        apply_auto_approve_process = APPLY_AUTO_APPROVE_PROCESS
        apply_process = APPLY_PROCESS

    if AUTO_APPROVE:
        workflow_apply_auto_approve_target_process = apply_auto_approve_process + target_process
        process = subprocess.Popen(workflow_apply_auto_approve_target_process, cwd=cwd).wait()
    else:
        workflow_apply_target_process = apply_process + target_process
        process = subprocess.Popen(workflow_apply_target_process, cwd=cwd).wait()

    if process == 1:
        # If the process experiences an error, skip the remaining commands
        return 1

    # workflow_apply_auto_approve_refresh_target_process = APPLY_REFRESH_AUTO_APPROVE_PROCESS + ["-target=" + sub for sub in stage_targets]
    # print("\nPerforming -apply-refresh to sync statefile and match the current provisioned state")
    # subprocess.Popen(workflow_apply_auto_approve_refresh_target_process, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()

    terraform_apply_auto_approve_refresh(cwd, VAR_FILE)

def workflow_terraform_destroy(cwd, stage_targets, stage_name, VAR_FILE="", AUTO_APPROVE=False):

    tfvars_settings(cwd)

    target_process = ["-target=" + sub for sub in stage_targets]

    if len(VAR_FILE) > 0:
        destroy_auto_approve_process = [TERRAFORM_PATH, 'apply', '-var-file=%s' % VAR_FILE, '-auto-approve']
        destroy_process = [TERRAFORM_PATH, 'apply', '-var-file=%s' % VAR_FILE]
    else:
        destroy_auto_approve_process = DESTROY_AUTO_APPROVE_PROCESS
        destroy_process = DESTROY_PROCESS

    if AUTO_APPROVE:
        workflow_destroy_auto_approve_target_process = destroy_auto_approve_process + target_process
        process = subprocess.Popen(workflow_destroy_auto_approve_target_process, cwd=cwd).wait()
    else:
        workflow_destroy_target_process = destroy_process + target_process
        process = subprocess.Popen(workflow_destroy_target_process, cwd=cwd).wait()

    if process == 1:
        # If the process experiences an error, skip the remaining commands
        return 1

    delete_latest_row_from_history(cwd, stage_name)

def workflow_terraform_apply_refresh(cwd, stage_targets, AUTO_APPROVE=False):
    tfvars_settings(cwd)
    
    if AUTO_APPROVE:
        workflow_apply_auto_approve_target_process = APPLY_REFRESH_AUTO_APPROVE_PROCESS + ["-target=" + sub for sub in stage_targets]
        process = subprocess.Popen(workflow_apply_auto_approve_target_process, cwd=cwd).wait()
    else:
        workflow_apply_target_process = APPLY_REFRESH_PROCESS + ["-target=" + sub for sub in stage_targets]
        process = subprocess.Popen(workflow_apply_target_process, cwd=cwd).wait()

    if process == 1:
        # If the process experiences an error, skip the remaining commands
        return 1

    terraform_apply_auto_approve_refresh(cwd)
    
def workflow_terraform_plan_refresh(cwd, stage_targets):
    tfvars_settings(cwd)
    
    workflow_apply_auto_approve_target_process = PLAN_REFRESH_PROCESS + ["-target=" + sub for sub in stage_targets]
    return subprocess.Popen(workflow_apply_auto_approve_target_process, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def check_stages_errors(stages_errors):

    error = False

    for stage_errors in stages_errors:
        if stage_errors["error"] == True:
            error = True

            print_error("\nStage \"%s\" has an error in its workflow config.yaml:" % stage_errors["stage_name"])
            for key, value in stage_errors.items():
                if key != "error" and key != "stage_name" and len(value) > 0:
                    print_error(value)

    return error

def stage_workflow_terraform_apply(cwd, var_file=""):
    stages, stages_errors = get_stages(cwd)

    active_stages, err, err_message = get_active_stages_from_workflow(cwd)

    if err:
        print_error(err_message)
        return

    stages = get_stages_to_apply_from_active_stages(active_stages, stages)
    
    for stage in stages:

        stage_name = stage["stage_name"]
        stage_auto_approve = stage["stage_auto_approve"]
        stage_targets = stage["stage_targets"]

        print("\nApplying Stage \"%s\"" % stage_name)
        
        if stage_auto_approve:
            print("\nPerforming \"terraform apply -auto-approve\" on the following target(s):")
        else:
            print("\nPerforming \"terraform apply\" on the following target(s):")
            
        for index in range(len(stage_targets)):
            print("%s. %s" % (index+1, stage_targets[index]))

        # Prepare terraform command
        workflow_terraform_apply(cwd, stage_targets, stage_name, stage_auto_approve, VAR_FILE=var_file)

def stage_workflow_terraform_destroy(cwd, var_file=""):
    stages, stages_errors = get_stages(cwd)

    active_stages, err, err_message = get_active_stages_from_workflow(cwd)

    if err:
        print_error(err_message)
        return
        
    stages = get_stages_to_apply_from_active_stages(active_stages, stages)
    
    stages.reverse()

    for stage in stages:

        stage_name = stage["stage_name"]
        stage_auto_approve = stage["stage_auto_approve"]
        stage_targets = stage["stage_targets"]

        print("\nDestroying Stage \"%s\"" % stage_name)
        
        if stage_auto_approve:
            print("\nPerforming \"terraform destroy -auto-approve\" on the following target(s):")
        else:
            print("\nPerforming \"terraform destroy\" on the following target(s):")
            
        for index in range(len(stage_targets)):
            print("%s. %s" % (index+1, stage_targets[index]))
        
        # Prepare terraform command
        workflow_terraform_destroy(cwd, stage_targets, stage_name, stage_auto_approve, VAR_FILE=var_file)

def stage_workflow_terraform_apply_refresh(cwd):
    stages, stages_errors = get_stages(cwd)

    active_stages, err, err_message = get_active_stages_from_workflow(cwd)

    if err:
        print_error(err_message)
        return

    stages = get_stages_to_apply_from_active_stages(active_stages, stages)
    
    for stage in stages:

        stage_name = stage["stage_name"]
        stage_auto_approve = stage["stage_auto_approve"]
        stage_targets = stage["stage_targets"]

        print("\nApplying Stage \"%s\"" % stage_name)
        
        if stage_auto_approve:
            print("\nPerforming \"terraform apply -refresh-only -auto-approve\" on the following target(s):")
        else:
            print("\nPerforming \"terraform apply -refresh-only\" on the following target(s):")
            
        for index in range(len(stage_targets)):
            print("%s. %s" % (index+1, stage_targets[index]))

        # Prepare terraform command
        workflow_terraform_apply_refresh(cwd, stage_targets, stage_auto_approve)