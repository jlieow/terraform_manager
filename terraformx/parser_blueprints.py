import os

from terraformx.terraformx_common import *
from utils import *

def create_blueprint(cwd, file_name):

    TERRAFORM_BLUEPRINT_STAGES_PREFACE = "The following stages are found:\n"
    TERRAFORM_BLUEPRINT_STAGES_OPTIONS = "\nWhich stage would you like to save to blueprint: "

    blueprint = []

    if os.path.exists(cwd + "/" + file_name + ".csv"):
        if input("\n %s.csv currently exists. Please enter \"Y\" to confirm you would like to continue and overwrite this file." % file_name).upper() != "Y":
            return

    while True:

        terraform_root = input("\nPlease provide the path to the Terraform root: ")
        terraform_root_dir = get_full_path_else_return_empty_str(terraform_root)
        stage_name = ""

        if not os.path.exists(terraform_root_dir):
            print_error("\n[ERROR] Unable to locate Terraform root.")
        
        if does_workflow_file_exist(terraform_root_dir):
            stages, _ = get_stages(terraform_root_dir)

            stage_names = []
            for stage in stages:
                stage_names.append(stage["stage_name"])

            stage_names.append("< SELECT ALL >")
            STAGE_NUMBER = input_options(TERRAFORM_BLUEPRINT_STAGES_PREFACE, stage_names, TERRAFORM_BLUEPRINT_STAGES_OPTIONS)

            # print(STAGE_NUMBER)

            if STAGE_NUMBER == len(stage_names) - 1:
                stage_names.pop()
                # print(stage_names)
                for stage_name in stage_names:
                    blueprint.append([terraform_root_dir, stage_name])
            else: 
                blueprint.append([terraform_root_dir, stage_names[STAGE_NUMBER]])
        else:
            blueprint.append([terraform_root_dir, stage_name])

        if input("\nPlease enter \"Y\" to continue or any key to save the blueprint: ").upper() != "Y":
            os.remove(os.getcwd() + "/" + file_name + ".csv")
            
            if len(blueprint) > 0:
                for dir_and_stage in blueprint:
                    cwd = dir_and_stage[0] 
                    stage_name = dir_and_stage[1] 
                    
                    addBlueprint(os.getcwd() + "/" + file_name + ".csv", cwd, stage_name)

            print("Blueprint \"%s.csv\" has been saved!" % file_name)
            return



def blueprints(args):

    chdir = args.chdir
    create = args.create
    file_name = args.file_name

    cwd = get_cwd(chdir)
    if len(cwd) == 0:
        if not os.path.exists(cwd):
            print_error("[ERROR] Unable to locate directory.")
            return 

    if create:
        create_blueprint(cwd, file_name)
    else:
        blueprint = get_rows_as_list(cwd)
                        
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