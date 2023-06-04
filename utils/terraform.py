import os
import glob
import subprocess

from utils.common import *
from utils.terraform_commands import *
from utils.workflow import *
from utils.print_options import *
from utils.drift import *
from utils.blueprints import *

# ----- CONSTANTS ----- #

class Terraform_constants:
    TERRAFORM_PATH = 'terraform'
    WAITING_MESSAGE = "Please wait..."

# ----- CONSTANTS ----- #

# def tfvars_settings(cwd):
#     filenames = glob.glob(cwd + "/*.tfvars")

#     # filenames = [cwd + "/backend.tfvars", cwd + "/config.tfvars"]
#     with open(cwd + "/config/settings.tfvars", 'w') as outfile:
#         for fname in filenames:
#             with open(fname) as infile:
#                 for line in infile:
#                     outfile.write(line)
#                 #Add a newline so that variables are separated
#                 outfile.write("\n")
#                 # Remove newline at the end of the file
#                 infile.read().rstrip('\n')     

def terraform():

    TERRAFORM_ROOTS_PREFACE = "The following directories are terraform roots:\n"
    TERRAFORM_ROOTS_OPTIONS = "\nWhich terraform root would you like to invoke terraform commands on: "

    TERRAFORM_COMMAND_PREFACE = "The following terraform commands can be invoked:\n"
    LIST_TERRAFORM_COMMAND=[
        "terraform init",
        "terraform apply",
        "terraform destroy",
        "terraform destroy and apply -auto-approve",
        "terraform output",
        "terraform apply -refresh-only",
    ]

    TERRAFORM_COMMAND_OPTIONS_DEFAULT = "\nWhich command would you like to invoke? The default is currently [%s]: "

    BREAKER = False

    # Get list of terraform roots
    # list_terraform_root_dir = locate_terraform_root_directories(os.path.dirname(os.getcwd()))
    list_terraform_root_dir = locate_terraform_root_directories(os.getcwd())

    if len(list_terraform_root_dir) == 0:
        print_warning("There are no Terraform roots detected.")
        return

    while True:
        # Question 1
        DIR_NUMBER = input_options(TERRAFORM_ROOTS_PREFACE, [os.path.basename(directory) for directory in list_terraform_root_dir], TERRAFORM_ROOTS_OPTIONS,  allow_special_break=True, special_break="<")
        if DIR_NUMBER == "<":
            print()
            break

        print("\n\"%d. %s\" was selected." % (DIR_NUMBER+1, os.path.basename(list_terraform_root_dir[DIR_NUMBER])))

        COMMAND_NUMBER = None

        cwd = list_terraform_root_dir[DIR_NUMBER]

        # print("\ndoes_workflow_file_exist: %s"does_workflow_file_existist(cwd))
        
        workflow_file_exists = does_workflow_file_exist(cwd)
        if workflow_file_exists:
            terraform_workflow(cwd)

        while not workflow_file_exists:
            # Question 2
            COMMAND_NUMBER = input_options(TERRAFORM_COMMAND_PREFACE, LIST_TERRAFORM_COMMAND, TERRAFORM_COMMAND_OPTIONS_DEFAULT, use_prev_as_default=True, choice=COMMAND_NUMBER, allow_special_break=True, special_break="<")

            if COMMAND_NUMBER == "<":
                print()
                break

            print("\"%d. %s\" was selected.\n" % (COMMAND_NUMBER+1, LIST_TERRAFORM_COMMAND[COMMAND_NUMBER]))

            cwd = list_terraform_root_dir[DIR_NUMBER]

            tfvars_settings(cwd)  
            
            print(Terraform_constants.WAITING_MESSAGE)

            match COMMAND_NUMBER:
                case 0:
                    terraform_init(cwd)
                case 1:
                    terraform_apply(cwd)
                case 2:
                    terraform_destroy(cwd)
                case 3:
                    terraform_destroy(cwd)
                    terraform_apply(cwd, AUTO_APPROVE=True)
                case 4:
                    terraform_output(cwd)
                case 5:
                    terraform_apply_refresh(cwd)
            
            # To break out of while loop for Question 2
            match input("\nContinue invoking terraform commands for directory \"%s\"? N to stop, NN to return to main menu: " % os.path.basename(cwd)).upper():
                case "N":
                    break
                case "NN":
                    BREAKER = True
                    break

        # To break out of while loop for Question 1
        if BREAKER:
            BREAKER = False
            break

def terraform_workflow(cwd):
    # if does_workflow_contain_error_and_warnings(cwd):
    #     print("\nAborting workflow")
    #     return

    COMMAND_NUMBER = None
    
    while True:
        print_alert(WORKFLOW_CONFIG_DETECTED_MESSAGE)

        if does_workflow_contain_error_and_warnings(cwd):
            print("\nAborting workflow")
            break

        # Question 2
        COMMAND_NUMBER = input_options(TERRAFORM_COMMAND_PREFACE, LIST_TERRAFORM_COMMAND, TERRAFORM_COMMAND_OPTIONS_DEFAULT, use_prev_as_default=True, choice=COMMAND_NUMBER, allow_special_break=True, special_break="<")

        if COMMAND_NUMBER == "<":
            print()
            break

        match COMMAND_NUMBER:
            case 0:
                terraform_init(cwd)
            case 1:
                stage_workflow_terraform_apply(cwd)
            case 2:
                stage_workflow_terraform_destroy(cwd)
            case 3:
                # terraform_destroy(cwd)
                stage_workflow_terraform_destroy(cwd)
                stage_workflow_terraform_apply(cwd)
                # terraform_apply(cwd, AUTO_APPROVE=True)
            case 4:
                terraform_output(cwd)
            case 5:
                stage_workflow_terraform_apply_refresh(cwd)

def terraform_destroy_from_history():

    history_path = get_dir_of_terraform_manager() + History_constants.HISTORY_CSV_PATH

    histories = get_rows_as_list(history_path)

    list_history(histories)

    # if len(histories) == 0:
    #     print_warning("\nThere is no record of anything being provisioned based on your history. The program will now exit.")
    #     return

    histories = get_rows_as_list(history_path)

    list_history(histories)

    # if len(histories) == 0:
    #     print_warning("\nThere is no record of anything being provisioned based on your history. The program will now exit.")
    #     return

    # # ----- WARNING ----- #
    # print_high_alert("\n!!! THIS IS A DESTRUCTIVE ACTION !!!\
    # \nContinuing will invoke \"terraform destroy --auto-approve\" on the folders in the following order:\n"
    # )

    # for i in range(len(histories)):
    #     reverseIndex = len(histories) - i - 1

    #     cwd = histories[reverseIndex][0]
    #     stage_name = histories[reverseIndex][1]

    #     if len(stage_name) == 0:  
    #         print("%d. %s" % (i+1, os.path.basename(cwd)))
    #     else:
    #         print("%d. %s - Stage \"%s\"" % (i+1, os.path.basename(cwd), stage_name))

    # ----- WARNING ----- #

    if input("\nPlease ensure that the resources provisioned in these folders can be deleted. Enter \"Y destroy all\" to continue: ").upper() == "Y DESTROY ALL":
        for history in reversed(histories):
            cwd = history[0]
            stage_name = history[1]

            if len(stage_name) == 0: 
                print("no stage detected")
                tfvars_settings(cwd) 
                
                print("Performing \"terraform destroy --auto-approve\" on %s" % os.path.basename(cwd))
                terraform_destroy(cwd, AUTO_APPROVE=True)
            else:
                if does_stage_name_exist(cwd, stage_name):
                    stage = get_stage(cwd, stage_name)
                    stage_targets = stage["stage_targets"]
                    stage_name = stage["stage_name"]
                    workflow_terraform_destroy(cwd, stage_targets, stage_name, AUTO_APPROVE=True)
                else:
                    print_error("\n[ERROR] Did you delete/comment a workflow stage? Could not find %s - Stage \"%s\"!\n" % (os.path.basename(cwd), stage_name))

# def terraform_drift():
    
#     # Get list of terraform roots
#     list_terraform_root_dir = locate_terraform_root_directories(os.path.dirname(os.getcwd()))

#     while True:
#         # Question 1
#         DIR_NUMBER = input_options(TERRAFORM_ROOTS_PREFACE, [os.path.basename(directory) for directory in list_terraform_root_dir], TERRAFORM_ROOTS_CHECK_DRIFT_OPTIONS)
#         print("\"%d. %s\" was selected.\n" % (DIR_NUMBER+1, os.path.basename(list_terraform_root_dir[DIR_NUMBER])))

#         print(Terraform_constants.WAITING_MESSAGE)

#         cwd = list_terraform_root_dir[DIR_NUMBER]

#         # subprocess.Popen(APPLY_REFRESH_PROCESS, cwd=cwd, env=nt.environ).wait()

#         p = subprocess.Popen(PLAN_REFRESH_PROCESS, cwd=cwd, stdout=subprocess.PIPE, env=nt.environ)

#         out, err = p.communicate()

#         print("out")
#         # print(out.decode('UTF-8'))
#         if TERRAFORM_REFRESH_MESSAGE_OBJECTS_HAVE_CHANGED in out.decode('UTF-8'):
#             print(TERRAFORM_REFRESH_MESSAGE_OBJECTS_HAVE_CHANGED)
#         else:
#             print(NO_DRIFT_DETECTED)

#         print("err")
#         print(err)

#         # To break out of while loop for Question 1
#         if input("\nWould you like to return to main menu? Y to return to main menu: ").upper() == "Y":
#             break

def terraform_check_for_drift():

    TERRAFORM_REFRESH_MESSAGE_OBJECTS_HAVE_CHANGED = "Objects have changed outside of Terraform"
    NO_DRIFT_DETECTED = "No drift detected"

    while True:
        
        print("Checking for drift - In Progress...\n")
        
        # Get list of terraform roots
        list_terraform_root_dir = locate_terraform_root_directories(os.getcwd())

        drifted_terraform_roots = []

        for index in range(len(list_terraform_root_dir)):
            
            cwd = list_terraform_root_dir[index]

            if does_workflow_file_exist(cwd):
                stages, _ = get_stages(cwd)
                # for stage in stages_and_targets:
                for stage in stages:

                    stage_name = stage["stage_name"]
                    stage_targets = stage["stage_targets"]

                    # Prepare terraform command
                    p = workflow_terraform_plan_refresh(cwd, stage_targets)
    
                    out, _ = p.communicate()

                    # Check all terraform roots for configuration drift
                    if TERRAFORM_REFRESH_MESSAGE_OBJECTS_HAVE_CHANGED in out.decode('UTF-8'):
                        p.communicate("") # When there is drift, terraform waits for input. This sends "" to the input so that the output can end.
                        drifted_terraform_roots.append([cwd, stage_name])
                        print_error("%d. %s - Stage \"%s\" - %s" % (index+1, os.path.basename(cwd), stage_name, TERRAFORM_REFRESH_MESSAGE_OBJECTS_HAVE_CHANGED))
                    else:
                        print("%d. %s - Stage \"%s\" - %s" % (index+1, os.path.basename(cwd), stage_name, NO_DRIFT_DETECTED))
                    
                    # p.stdout.close()
                    
            else:
                p = terraform_plan_refresh(cwd)

                out, _ = p.communicate()

                # Check all terraform roots for configuration drift
                if TERRAFORM_REFRESH_MESSAGE_OBJECTS_HAVE_CHANGED in out.decode('UTF-8'):
                    p.communicate("") # When there is drift, terraform waits for input. This sends "" to the input so that the output can end.
                    drifted_terraform_roots.append([cwd, ""])
                    print_error("%d. %s - %s" % (index+1, os.path.basename(cwd), TERRAFORM_REFRESH_MESSAGE_OBJECTS_HAVE_CHANGED))
                else:
                    print("%d. %s - %s" % (index+1, os.path.basename(cwd), NO_DRIFT_DETECTED))
                # print(drifted_terraform_roots)

                # p.stdout.close()
            

        if len(drifted_terraform_roots) == 0:
            print("\nObjects in all Terraform Roots have not changed\n")
        else:
            print("\nObjects in the following Terraform Root have changed:\n")
            for index in range(len(drifted_terraform_roots)): 
                if len(drifted_terraform_roots[index][1]) > 0:
                    print("%d. %s - Stage \"%s\"" % (index+1, os.path.basename(drifted_terraform_roots[index][0]), drifted_terraform_roots[index][1]))
                else:
                    print("%d. %s" % (index+1, os.path.basename(drifted_terraform_roots[index][0])))
            
            # Attempt to sync the difted Terraform Roots' State file to amtch the current provisioned state 
            terraform_apply_refresh_or_apply_all(drifted_terraform_roots)

        if input("\nEnter Y to perform another configuration drift check and any key to return to main menu: ").upper() != "Y":
            break

def terraform_multi_build():
    TERRAFORM_ROOTS_PREFACE = "The following directories are terraform roots:\n"
    TERRAFORM_MULTI_BUILD_OPTIONS = "\nWhich terraform root would you like to multi-build: "

    TERRAFORM_MULTI_BUILD_STAGES_PREFACE = "The following stages are found in:\n"
    TERRAFORM_MULTI_BUILD_STAGES_OPTIONS = "\nWhich stage would you like to save to multi-build: "

    # TODO add function to build the config/settings.tfvars file

    # Get list of terraform roots
    list_terraform_root_dir = locate_terraform_root_directories(os.path.dirname(os.getcwd()))
    multiBuild = []

    terraform_roots = [os.path.basename(directory) for directory in list_terraform_root_dir]
    terraform_roots.append("REMOVE LAST DIRECTORY")
    terraform_roots.append("FINISH AND MULTI-BUILD")

    while True:

        # Question 1
        DIR_NUMBER = input_options(TERRAFORM_ROOTS_PREFACE, terraform_roots, TERRAFORM_MULTI_BUILD_OPTIONS, allow_special_break=True, special_break="<")
        if DIR_NUMBER == "<":
            break

        print("\"%d. %s\" was selected.\n" % (DIR_NUMBER+1, os.path.basename(terraform_roots[DIR_NUMBER])))

        removeLast = len(terraform_roots) - 2
        complete = len(terraform_roots) - 1

        stage_names = []
        
        if DIR_NUMBER < removeLast:
            cwd = list_terraform_root_dir[DIR_NUMBER]

            if does_workflow_file_exist(cwd):
                print_alert(WORKFLOW_CONFIG_DETECTED_MESSAGE)
                stages_and_targets = get_stages(cwd)

                for stage in stages_and_targets:
                    stage_names.append(stage["stage_name"])

                stage_names.append("< SELECT ALL >")
                STAGE_NUMBER = input_options(TERRAFORM_MULTI_BUILD_STAGES_PREFACE, stage_names, TERRAFORM_MULTI_BUILD_STAGES_OPTIONS)

                # print(STAGE_NUMBER)

                if STAGE_NUMBER == len(stage_names) - 1:
                    stage_names.pop()
                    # print(stage_names)
                    for stage_name in stage_names:
                        multiBuild.append([cwd, stage_name])
                else: 
                    multiBuild.append([cwd, stage_names[STAGE_NUMBER]])

            else:    
                multiBuild.append([cwd,""])

            # multiBuild.append(list_terraform_root_dir[DIR_NUMBER])

        if DIR_NUMBER == removeLast:
            if len(multiBuild) > 0:
                multiBuild.pop()

        elif DIR_NUMBER == complete:
            print("Starting Multi-Build...")
            break
        
        elif len(multiBuild) > 0:
            print("The current multi-build is:")
            for index in range(len(multiBuild)):
                cwd = multiBuild[index][0]
                stage_name = multiBuild[index][1]
                if len(stage_name) == 0:
                    print("%d. %s" % (index+1, os.path.basename(cwd)))
                else:
                    print("%d. %s - Stage \"%s\"" % (index+1, os.path.basename(cwd), stage_name))

        print()

    for dir_and_stage in multiBuild:
        cwd = dir_and_stage[0] 
        stage_name = dir_and_stage[1] 

        if len(stage_name) == 0:
            print("Building %s..." % os.path.basename(cwd))
            process = terraform_apply(cwd, AUTO_APPROVE=True)
        else:
            print("Building %s - Stage \"%s\"" % (os.path.basename(cwd), stage_name))

            stage = get_stage(cwd, stage_name)
            stage_targets = stage["stage_targets"]
            stage_name = stage["stage_name"]

            process = workflow_terraform_apply(cwd, stage_targets, stage_name, AUTO_APPROVE=True)
        
        if process == 1:
            # If the process experiences an error, break
            break

def terraform_blueprints():

    TERRAFORM_BLUEPRINTS_SELECTION_PREFACE = "What would you like to do with blueprints:\n" 
    LIST_SELECTION_COMMAND=[
        "Create a new blueprint",
        "Build existing blueprint",
    ]
    TERRAFORM_ROOTS_BLUEPRINTS_SELECTION_OPTIONS = "\nPlease key in your selection: "

    TERRAFORM_BLUEPRINTS_PREFACE = "The following blueprints are found:\n"
    TERRAFORM_ROOTS_BLUEPRINTS_OPTIONS = "\nWhich blueprint would you like to invoke \"terraform apply\" on: "

    while True:
        # Get csv files from blueprints directory
        path =  get_dir_of_terraform_manager() + "/data/blueprints/*.csv"
        blueprints = glob.glob(path)

        OPEN_BLUEPRINTS = True

        # If there are no blueprints, create one. 
        # If there are existing blueprints, allow user to choose if they would like to create a new blueprint or build an existing one.
        if len(blueprints) == 0:
            OPEN_BLUEPRINTS = False

            if input("No blueprints were found. Enter Y to create one? ").upper() == "Y":
                terraform_create_blueprint()
            else:
                break
    
        if OPEN_BLUEPRINTS:
            BLUEPRINT_SELECTION_NUMBER = input_options(TERRAFORM_BLUEPRINTS_SELECTION_PREFACE, LIST_SELECTION_COMMAND, TERRAFORM_ROOTS_BLUEPRINTS_SELECTION_OPTIONS, allow_special_break=True, special_break="<")
            if BLUEPRINT_SELECTION_NUMBER == "<":
                break

            match BLUEPRINT_SELECTION_NUMBER:
                case 0:
                    terraform_create_blueprint()
                case 1:
                    BLUEPRINT_NUMBER = input_options(TERRAFORM_BLUEPRINTS_PREFACE, [os.path.basename(directory) for directory in blueprints], TERRAFORM_ROOTS_BLUEPRINTS_OPTIONS, allow_special_break=True, special_break="<")
                    if BLUEPRINT_NUMBER == "<":
                        break

                    # print("correct")
                    # print(blueprints[BLUEPRINT_NUMBER])
                    BLUEPRINT_CSV_PATH = blueprints[BLUEPRINT_NUMBER]
                    blueprint = get_rows_as_list(BLUEPRINT_CSV_PATH)
                    
                    print("\nContinuing will invoke \"terraform apply --auto-approve\" on the folders in the following order:\n"
                    )
                    
                    for i in range(len(blueprint)):
                        cwd = blueprint[i][0]
                        stage_name = blueprint[i][1]
                        if len(stage_name) == 0:
                            print("%d. %s" % (i+1, os.path.basename(cwd)))
                        else:
                            print("%d. %s - Stage \"%s\"" % (i+1, os.path.basename(blueprint[i][0]), stage_name))
                    
                    if input("\nPlease enter \"Y\" to continue: ").upper() == "Y":
                        for dir_and_stage in blueprint:
                            # print("dir_and_stage")
                            # print(dir_and_stage)

                            cwd = dir_and_stage[0] 
                            stage_name = dir_and_stage[1] 

                            terraform_init(cwd)

                            if len(stage_name) == 0:
                                print("\nPerforming \"terraform apply --auto-approve\" on %s" % os.path.basename(cwd))
                                process = terraform_apply(cwd, AUTO_APPROVE=True)
                            else:
                                print("\nPerforming \"terraform apply --auto-approve\" on %s - Stage \"%s\"" % (os.path.basename(cwd), stage_name))

                                stage = get_stage(cwd, stage_name)
                                stage_targets = stage["stage_targets"]
                                stage_name = stage["stage_name"]

                                process = workflow_terraform_apply(cwd, stage_targets, stage_name, AUTO_APPROVE=True)
                            
                            if process == 1:
                                # If the process experiences an error, break
                                break