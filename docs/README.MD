## To install python dependencies

pip install -r requirements.txt

## To generate new requirements.txt

pip install pipreqs
python -m pipreqs.pipreqs .

# Run following command to compile .py code into .exe

pyinstaller --onefile main.py

# Run tests with the following methods

1. To run a single test module, in this case test_antigravity.py:

   - To run a single test module, in this case test_antigravity.py:<br /><br />
     python -m unittest test.test_antigravity

2. Running a single test case or test method:

   - Also you can run a single TestCase or a single test method:<br /><br />
     python -m unittest test.test_antigravity.GravityTestCase

3. Running all tests:

   - This command will discover and run all the tests for you, they must be modules or packages named test\*.py (can be changed with the -p, --pattern flag):<br /><br />
     python -m unittest

## Runnings Terraform Manager

vi ~/.zshrc

alias terraform_manager="python3 /Users/jeromelieow/Documents/GitHub/terraform_manager/main.py"

export PATH=$PATH:/Users/jeromelieow/Documents/GitHub/terraform_manager/dist/main
alias terraform_manager2="/Users/jeromelieow/Documents/GitHub/terraform_manager/dist/main"

## Features of Terraform Manager

### Import AWS profiles from CSVs stored in /aws_credentials

Import .csv profiles found in /aws_credentials using aws configure import --csv command.

### Perform Terraform Commands

Detects if a workflow file exists in the terraform root and perform regular or more complex terraform commands

### Check Terraform Roots for Configuration Drift

Detects configuration drift based on workflow configuration

### Perform Terraform Multi-Build

Allows sequential building of multiple terrform roots

### Apply Terraform Blueprints

Allows you to save sequential build steps into a csv file and reference them later on when a build is required.

### Terraform Destroy based on History

Each time a terraform root is built, it is saved to a history .csv file. When required, the file can be later referenced to destroy each root sequentially.

### Use Workflows

Workflows is a method to perform terraform apply on targeted modules/resources by storing them as steps in a yaml file.

By simply creating a directory called workflow on the root dir of a Terraform root and placing a config.yaml file in your terraform root, Terraform Manager and Terraformx CLI will detect the yaml file and invoke terraform commands on targets modules and resources.

#### A typical terraform root directory layout with workflow

    .
    ├── config            # Terraform Manager and Terraformx CLI locates all your tfvars files in the root directory and combines them here.
    ├── modules           # Location of Terraform modules.
    ├── workflow          # Location of config.yaml.
    ├── backend.tf        # Tells Terraform where to store the Terraform state file.
    ├── main.tf           # Terraform main.tf.
    ├── output.tf         # Outputs values after provisioning resources.
    ├── variables.tf
    ├── backend.tfvars    # Variables to be used by backend.tf. This will be picked up by Terraform Manager and Terraformx CLI and placed into /config
    ├── config.tfvars     # Variables to be used by Terraform when provisioning your resources. This will be picked up by Terraform Manager and Terraformx CLI and placed into /config
    └── README.md

#### Sample workflow config.yaml

```
ignore: True
active_stages: 2-3, 5
active_stage_names: stage 1, stage 2
stages:
  - name: stage 1
    auto_approve: True
    targets:
      - module:
          - mi-1
          - mi-2
      - resource:
          - ri-1.extra
          - ri-2.extra
          - ri-1.try
  - name: stage 2
    auto_approve: True
    targets:
      - module:
          - mi-24
```

config.yaml legend:
| key | description | type | Example allowed values | Default value when omitted | Behaviour if omitted |
| --- | --- | --- | --- | --- | --- |
| ignore | True tells the Terraform Manager or Terraformx CLI to ignore the entire workflow file | bool | True, False | False | config.yaml is not ignored |
| active_stages | Specifies which stage should be applied or destroyed and ignores the rest using an int | int | 1, 3-4 | None | No stage is ignored |
| active_stage_names | Specifies which stage should be applied or destroyed and ignores the rest using the name of the stage | int | stage 1, stage 2 | None | No stage is ignored |
| stages | Specifies the stages | arr | [] | None | Operation would fail |
| stages.name | Name of the stage | str | "stage 1" | None | Stage would not have a name but will continue to run |
| stages.auto_approve | Evaluated to see if the stage would should be auto approved without user input | bool | True, False | False | Stage will not be auto approved and require user input |
| stages.targets | Specifies which modules or resources should be built in this stage | dict | module, resource | None | Operation would fail |
| stages.targets.module | Specifies the name of the modules which should be built in this stage | arr | "name_of_module" | None | No modules will be targeted |
| stages.targets.resources | Specifies the name of the resources which should be built in this stage | arr | "type_of_resource.name_of_resource" | None | No resources will be targeted |
