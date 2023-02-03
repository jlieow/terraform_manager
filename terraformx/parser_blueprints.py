import os

from terraformx.terraformx_common import *
from utils import *

def create_blueprint(blueprint_path):

    TERRAFORM_BLUEPRINT_STAGES_PREFACE = "The following stages are found:\n"
    TERRAFORM_BLUEPRINT_STAGES_OPTIONS = "\nWhich stage would you like to save to blueprint: "

    blueprint = []
    file_name = os.path.basename(blueprint_path)

    if os.path.exists(blueprint_path):
        if input("\n %s.csv currently exists. Please enter \"Y\" to confirm you would like to continue and overwrite this file." % file_name).upper() != "Y":
            return

    while True:

        terraform_root = input("\nPlease provide the path to the Terraform root: ")
        terraform_root_dir = get_full_path_else_return_empty_str(terraform_root)

        if not os.path.exists(terraform_root_dir):
            print_error("\n[ERROR] Unable to locate Terraform root.")
        
        blueprint += add_blueprint_row(terraform_root_dir)

        if input("\nPlease enter \"Y\" to continue or any key to save the blueprint: ").upper() != "Y":
            if os.path.exists(blueprint_path):
                os.remove(blueprint_path)

            if len(blueprint) > 0:
                add_blueprint_rows(blueprint_path, blueprint)

                # for dir_and_stage in blueprint:
                #     cwd = dir_and_stage[0] 
                #     stage_name = dir_and_stage[1] 
                    
                #     add_blueprint(blueprint_path, cwd, stage_name)
     
            print("Blueprint \"%s.csv\" has been saved!" % file_name)
            return

def apply_blueprint(blueprint_path):
    print("\nVerifying blueprint...")
    if not is_this_a_verified_blueprint(blueprint_path):
        return
    print("Blueprint verified!")

    blueprint = get_rows_as_list(blueprint_path)
                    
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

def blueprints(args):

    create = args.create
    file = args.file.replace("/", "" )
    list = args.list

    blueprint_path = get_full_path_else_return_empty_str(file, ".csv")
    if not os.path.exists(blueprint_path):
        print_error("\n[ERROR] Unable to locate blueprint file.")
        return 
    
    if list:
        rows = get_rows_as_list(blueprint_path)
        list_blueprint(rows)
        return

    if create:
        create_blueprint(blueprint_path)
        return
    else:
        apply_blueprint(blueprint_path)
        return