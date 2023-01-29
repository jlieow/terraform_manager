import yaml
import hcl

import os

from .workflow import *

# ----- CONSTANTS ----- #

CHAOS_TEST_CONFIG_LOCATION = "/chaos_test/config.yaml"

# ----- CONSTANTS ----- #

def is_chaos_test_file_ignored(path):
    if os.path.exists(path):
        with open(path, 'r') as stream:
            data_loaded = yaml.safe_load(stream)

            # print(data_loaded)

            if "chaos_test" in data_loaded:
                if data_loaded["chaos_test"] == True:
                    return True

    return False

def does_chaos_test_file_exist(cwd):
    # Get csv files from blueprints directory
    path =  cwd + CHAOS_TEST_CONFIG_LOCATION
    workflow = glob.glob(path)

    if is_workflow_file_ignored(path):
        return False

    if len(workflow) > 0:
        return True
    return False

def locate_chaos_test_directories(root_directory):
    
    # root_directory = get_parent_dir(os.getcwd())
    list_chaos_test_dir = []

    # Get list of files and directories present in root directory
    # Search for backend.tf file in the directory
    # If backend.tf exists, get its parent directory and append it to a list
    for directory in os.listdir(root_directory):
        
        path = root_directory + "/" + directory + "/chaos_test/config.yaml"

        does_chaos_test_config_yaml_exist = glob.glob(path)
        if len(does_chaos_test_config_yaml_exist) != 0:
            list_chaos_test_dir.append(get_parent_dir(get_parent_dir(does_chaos_test_config_yaml_exist[0])))

    list_chaos_test_dir.sort()

    return list_chaos_test_dir

def get_chaos_test_stages(chaos_test_path):

    with open(chaos_test_path, 'r') as stream:
        data_loaded = yaml.safe_load(stream)

    chaos_test_stages = []
    chaos_test_stages_errors = []
    error = False

    stage_auto_approve_error_message = ""
    destroy_disabled_error_message = ""
    delay_before_execution_error_message = ""
    delay_after_execution_error_message = ""
    repeat_error_message = ""

    for stage in data_loaded["stages"]:

        stage_name = stage["name"] if "name" in stage else None

        #TODO needs to be fixed, now cannot be None
        try: 
            stage_auto_approve = stage["auto_approve"] if "auto_approve" in stage and stage["auto_approve"] is not None else False
            if not (isinstance(stage_auto_approve, bool) or stage_auto_approve == None):
                raise TypeError
                
        except:
            stage_auto_approve_error_message = "[ERROR] The value for key \"auto_approve\" in chaos testing config yaml needs to be a boolean."
            error = True
            stage_auto_approve = False

        try:
            destroy_disabled = stage["destroy_disabled"] if "destroy_disabled" in stage and stage["destroy_disabled"] is not None else False
            if not (isinstance(destroy_disabled, bool) or destroy_disabled == None):
                raise TypeError
        
        except:
            destroy_disabled_error_message = "[ERROR] The value for key \"destroy_disabled\" in chaos testing config yaml needs to be a boolean."
            error = True
            destroy_disabled = False

        try: 
            delay_before_execution = int(stage["delay_before_execution"]) if "delay_before_execution" in stage and stage["delay_before_execution"] is not None else 0
        except:
            delay_before_execution_error_message = "[ERROR] The value for key \"delay_before_execution\" in chaos testing config yaml needs to be an integer."
            error = True
            delay_before_execution = 0
        
        try: 
            delay_after_execution = int(stage["delay_after_execution"]) if "delay_after_execution" in stage and stage["delay_after_execution"] is not None else 0
        except:
            delay_after_execution_error_message = "[ERROR] The value for key \"delay_after_execution\" in chaos testing config yaml needs to be an integer."
            error = True
            delay_after_execution = 0
        
        try:
            repeat = int(stage["repeat"]) if "repeat" in stage and stage["repeat"] is not None else 1
        except:
            repeat_error_message = "[ERROR] The value for key \"repeat\" in chaos testing config yaml needs to be an integer."
            error = True
            repeat = 1
        
        stage_targets = get_targets(stage["targets"])

        chaos_test_stages.append({
            "stage_name": stage_name,
            "stage_auto_approve": stage_auto_approve,
            "destroy_disabled": destroy_disabled,
            "delay_before_execution": delay_before_execution,
            "delay_after_execution": delay_after_execution,
            "repeat": repeat,
            "stage_targets": stage_targets,
            })

        chaos_test_stages_errors.append({
            "error": error,
            "stage_name": stage_name,
            "stage_auto_approve_error_message": stage_auto_approve_error_message,
            "destroy_disabled_error_message": destroy_disabled_error_message,
            "delay_before_execution_error_message": delay_before_execution_error_message,
            "delay_after_execution_error_message": delay_after_execution_error_message,
            "repeat_error_message": repeat_error_message,
            "stage_targets_error_message": "",
            })
        

    return chaos_test_stages, chaos_test_stages_errors

# def get_number_of_repeat():
# def get_delay_before_execution():
# def get_delay_after_execution():

def is_stage_destroy_disabled(path, stage_name):

    is_destroy_disabled = False

    if os.path.exists(path):
        with open(path, 'r') as stream:
            data_loaded = yaml.safe_load(stream)

            # print(data_loaded)

            if "stages" in data_loaded:
                stages =  data_loaded["stages"] 

                for stage in stages:
                    if "destroy_disabled" in stage and stage_name == stage["name"]:
                        is_destroy_disabled = stage["destroy_disabled"]
    
    return is_destroy_disabled


