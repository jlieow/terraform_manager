import os

from terraformx.terraformx_common import *
from utils import *

def blueprints(args):

    chdir = args.chdir
    create = args.create

    cwd = get_cwd(chdir)
    if len(cwd) == 0:
        if not os.path.exists(cwd):
            print_error("[ERROR] Unable to locate directory.")
            return 

    if create:
        print("TODO Create Blueprints via cli")
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