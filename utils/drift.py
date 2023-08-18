import os

from utils.common import *
from utils.workflow import *

def terraform_refresh_or_apply_all(drifted_terraform_roots):

    print("Please select the desired method to resolve following drifted Terraform Root(s):")

    Choices = []
    # print(drifted_terraform_roots)
    for index in range(len(drifted_terraform_roots)):

        cwd = drifted_terraform_roots[index][0]
        stage_name = drifted_terraform_roots[index][1]

        PREFACE = "\n%d. %s - Stage \"%s\".\
            \nPerforming \"terraform apply\" would resolve missing/overprovisioned resources.\
            \nPerforming \"terraform apply -refresh-only\" would save the current state.\n" % (index+1, os.path.basename(cwd), stage_name)
        OPTIONS = [
            "terraform apply", 
            "terraform apply -refresh-only", 
            "< SKIP >"
            ]
        QUESTION = "\nWhich command would you like to invoke: "
        
        choice = input_options(preface=PREFACE, options=OPTIONS, input_question=QUESTION)
        
        Choices.append({
            "cwd": cwd,
            "stage_name": stage_name,
            "selection": choice
        })

    for choice in Choices:

        cwd = choice["cwd"]
        stage_name = choice["stage_name"]
        selection = choice["selection"]

        match selection:
            case 0:

                if len(stage_name) == 0:
                    terraform_apply(cwd, AUTO_APPROVE=True)
                else:
                    stage_and_targets = get_stage(cwd, stage_name)
                    stage_targets = stage_and_targets["stage_targets"]
                    workflow_terraform_apply(cwd, stage_targets, stage_name, AUTO_APPROVE=True)

            case 1:

                if len(stage_name) == 0:
                    terraform_refresh(cwd, AUTO_APPROVE=True)
                else:
                    stage_and_targets = get_stage(cwd, stage_name)
                    stage_targets = stage_and_targets["stage_targets"]
                    workflow_terraform_refresh(cwd, stage_targets, stage_name, AUTO_APPROVE=True)