import csv

from .print_options import *
from .terraform_commands import *
from .workflow import *

# ----- CONSTANTS ----- #

BLUEPRINTS_CSV_PATH = "./data/blueprints/"

# ----- CONSTANTS ----- #

def addBlueprint(blueprint_name, cwd, stage_name=""):
    path = BLUEPRINTS_CSV_PATH + blueprint_name + ".csv"
    #Save results to CSV    
    with open(path, 'a', newline='') as f:  
        # using csv.writer method from CSV package
        write = csv.writer(f)
        
        write.writerow([cwd, stage_name])
        f.close()

def terraformCreateBlueprint():

    TERRAFORM_ROOTS_PREFACE = "The following directories are terraform roots:\n"
    TERRAFORM_ROOTS_ADD_BLUEPRINT_OPTIONS = "\nWhich directory would you like to add to the blueprint: "

    TERRAFORM_BLUEPRINT_STAGES_PREFACE = "The following stages are found in:\n"
    TERRAFORM_BLUEPRINT_STAGES_OPTIONS = "\nWhich stage would you like to save to blueprint: "

    blueprint_name = input("\nPlease provide the name of the blueprint: ")

    # Get list of terraform roots
    list_terraform_root_dir = locate_terraform_root_directories(get_parent_dir(os.getcwd()))
    blueprint = []

    terraform_roots = [os.path.basename(directory) for directory in list_terraform_root_dir]
    terraform_roots.append("< REMOVE LAST DIRECTORY >")
    terraform_roots.append("< FINISH ADDING TO BLUEPRINT >")

    while True:
        
        # Question 1
        DIR_NUMBER = input_options(TERRAFORM_ROOTS_PREFACE, terraform_roots, TERRAFORM_ROOTS_ADD_BLUEPRINT_OPTIONS)
        print("\"%d. %s\" was selected.\n" % (DIR_NUMBER+1, os.path.basename(terraform_roots[DIR_NUMBER])))

        removeLast = len(terraform_roots) - 2
        complete = len(terraform_roots) - 1

        stage_names = []

        if DIR_NUMBER < removeLast:
            
            ## TODO refactor 
            cwd = list_terraform_root_dir[DIR_NUMBER]
            if does_workflow_file_exist(cwd):
                print_alert(WORKFLOW_CONFIG_DETECTED_MESSAGE)
                stages, _ = get_stages(cwd)

                for stage in stages:
                    stage_names.append(stage["stage_name"])

                stage_names.append("< SELECT ALL >")
                STAGE_NUMBER = input_options(TERRAFORM_BLUEPRINT_STAGES_PREFACE, stage_names, TERRAFORM_BLUEPRINT_STAGES_OPTIONS)

                # print(STAGE_NUMBER)

                if STAGE_NUMBER == len(stage_names) - 1:
                    stage_names.pop()
                    # print(stage_names)
                    for stage_name in stage_names:
                        blueprint.append([cwd, stage_name])
                else: 
                    blueprint.append([cwd, stage_names[STAGE_NUMBER]])

            else:    
                blueprint.append([cwd,""])

        elif DIR_NUMBER == removeLast:
            if len(blueprint) > 0:
                blueprint.pop()

        elif DIR_NUMBER == complete:
            print("Saving Blueprint...")
            break
        
        if len(blueprint) > 0:
            print("The current blueprint is:")
            for index in range(len(blueprint)):
                cwd = blueprint[index][0]
                stage_name = blueprint[index][1]
                if len(stage_name) == 0:
                    print("%d. %s" % (index+1, os.path.basename(cwd)))
                else:
                    print("%d. %s - Stage \"%s\"" % (index+1, os.path.basename(cwd), stage_name))
        
        print()

    for dir_and_stage in blueprint:
        cwd = dir_and_stage[0] 
        stage_name = dir_and_stage[1] 
        
        addBlueprint(blueprint_name, cwd, stage_name)
    
    print("Blueprint \"%s.csv\" has been saved!" % blueprint_name)



    TERRAFORM_BLUEPRINTS_SELECTION_PREFACE = "What would you like to do with blueprints:\n" 
    LIST_SELECTION_COMMAND=[
        "Create a new blueprint",
        "Build existing blueprint",
    ]
    TERRAFORM_ROOTS_BLUEPRINTS_SELECTION_OPTIONS = "\nPlease key in your selection: "

    TERRAFORM_BLUEPRINTS_PREFACE = "The following blueprints are found:\n"
    TERRAFORM_ROOTS_BLUEPRINTS_OPTIONS = "\nWhich blueprint would you like to invoke \"terraform apply\": "

    while True:
        # Get csv files from blueprints directory
        path =  os.getcwd() + "/blueprints/*.csv"
        blueprints = glob.glob(path)

        OPEN_BLUEPRINTS = True

        # If there are no blueprints, create one. 
        # If there are existing blueprints, allow user to choose if they would like to create a new blueprint or build an existing one.
        if len(blueprints) == 0:
            OPEN_BLUEPRINTS = False

            if input("No blueprints were found. Enter Y to create one? ").upper() == "Y":
                terraformCreateBlueprint()
            else:
                break
    
        if OPEN_BLUEPRINTS:
            BLUEPRINT_SELECTION_NUMBER = input_options(TERRAFORM_BLUEPRINTS_SELECTION_PREFACE, LIST_SELECTION_COMMAND, TERRAFORM_ROOTS_BLUEPRINTS_SELECTION_OPTIONS, allow_special_break=True, special_break="<")
            if BLUEPRINT_SELECTION_NUMBER == "<":
                break

            match BLUEPRINT_SELECTION_NUMBER:
                case 0:
                    terraformCreateBlueprint()
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
                        if len(blueprint[i][1]) == 0:
                            print("%d. %s" % (i+1, os.path.basename(blueprint[i][0])))
                        else:
                            print("%d. %s - Stage \"%s\"" % (i+1, os.path.basename(blueprint[i][0]), blueprint[i][1]))
                    
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

                                process = workflow_terraform_apply(cwd, stage["stage_targets"], stage["stage_name"], AUTO_APPROVE=True)
                            
                            if process == 1:
                                # If the process experiences an error, break
                                break