import subprocess
import os
import glob

from utils import *

# from import_aws_profiles import *
# from terraform import *
# from common import *
# from drift import *
# from blueprints import *

# ----- CONSTANTS ----- #

TOOLS_PREFACE = "Welcome to Terraform Manager. The following tools are available:\n"
LIST_TOOLS=[
    "Import AWS profiles from CSVs stored in /aws_credentials",
    "Perform Terraform Commands",
    "Check Terraform Roots for Configuration Drift",
    "Perform Terraform Multi-Build",
    "Apply Terraform Blueprints",
    "Terraform Destroy based on History",
    "Perform Unit Test",
]
TOOLS_OPTIONS = "\nWhich tool would you like to use: "

# ----- CONSTANTS ----- #

print(os.getcwd())

while True:

    term = input_options(TOOLS_PREFACE, LIST_TOOLS, TOOLS_OPTIONS, True) 

    print()

    match term:
        case 1: # Import AWS profiles
            print("Importing AWS Profiles...")
            import_aws_profiles()
        case 2:
            terraform()
        case 3:
            terraform_check_for_drift()
        case 4:
            terraform_multi_build()
        case 5:
            terraform_blueprints()
        case 6:
            terraform_destroy_from_history()
        case _:
            print("default")
    
    print()


