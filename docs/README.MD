# Terraform Manager

Terraform Manager extends the Terraform CLI with additional functonalities and aids to standardize Terraform code structure thorughout the entire development lifecycle to enable more consistent Ops deployment of Terraform for use cases such as GitOps.

Terraform Manager consists of 3 parts:
1. Utils: Core Features of Terraform Manager
2. Terraformx: Extends Terraform Manager core features into a CLI
3. Actions: Turns basic terraformx commands into executables for use in custom CI actions.

Please refer to **/utils/README.MD**, **/terraformx/README.MD** and **/actions/README.MD** for more details about the functions contained in their respective directories. 

The following sections will explain the features of Terraform Manager. 

---
## Utils: Core Features of Terraform Manager

Features include:

1. Import AWS profiles from CSVs stored in /aws_credentials
    
    - Import .csv profiles found in /aws_credentials using aws configure import --csv command.

2. Perform Terraform Commands

    - Detects if a workflow file exists in the terraform root and perform regular or more complex terraform commands

3. Check Terraform Roots for Configuration Drift

    - Detects configuration drift based on workflow configuration

4. Perform Terraform Multi-Build

    - Allows sequential building of multiple terrform roots

5. Apply Terraform Blueprints

    - Allows you to save sequential build steps into a csv file and reference them later on when a build is required.

6. Terraform Destroy based on History

    - Each time a terraform root is built, it is saved to a history .csv file. When required, the file can be later referenced to destroy each root sequentially.

7. Use Workflows

    - Workflows is a method to perform terraform apply on targeted modules/resources by storing them as steps in a yaml file.

...By simply creating a directory called workflow on the root dir of a Terraform root and placing a config.yaml file in your terraform root, Terraform Manager and Terraformx CLI will detect the yaml file and invoke terraform commands on targets modules and resources.

#### A typical terraform root directory layout with workflow

    .
    ├── config                # Terraform Manager and Terraformx CLI locates all your tfvars files in the root directory and combines them into a settings.tfvars file here.
    │   └── .env              # Environmental variables declared in a .env file will be loaded
    │   └── settings.tfvars   # Values in backend.tfvars and config.tfvars will be stored here
    ├── modules               # Location of Terraform modules.
    ├── workflow
    │   └── config.yaml       # Terraform Manager and Terraformx CLI will detect the yaml file and invoke terraform commands on targeted modules and resources.
    ├── backend.tf            # Tells Terraform where to store the Terraform state file.
    ├── main.tf               # Terraform main.tf.
    ├── output.tf             # Outputs values after provisioning resources.
    ├── variables.tf
    ├── backend.tfvars        # Variables to be used by backend.tf. This will be picked up by Terraform Manager and Terraformx CLI and placed into /config
    ├── config.tfvars         # Variables to be used by Terraform when provisioning your resources. This will be picked up by Terraform Manager and Terraformx CLI and placed into /config
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

---
## Terraformx: Extends Terraform Manager core features into a CLI

Commands:

1. terraformx init<br/><br/>

    The terraformx init command initializes a terraform root.<br/><br/>

    Optional Parameters:
    
    1. -ch-dir
        - Location of terraform root.
    2. -var-file        
        - Location of variable definitions file.
    <br/>

2. terraformx apply<br/><br/>

    The terraformx apply command executes the actions proposed in a Terraform plan.<br/><br/>

    Optional Parameters:
    
    1. -ch-dir
        - Location of terraform root.
    2. -var-file
        - Location of variable definitions file.
    3. -auto-approve
        - Auto approve command without requiring user input.
    4. -override-workflow
        - Overrides workflow stages auto_approve keys and auto approves every stage.
    5. -refresh-only
        - Review how terraform would update your state file.
    6. -rebuild
        - Rebuild terraform by destroying and applying the script.
    7. -blueprint
        - Location of blueprint file. Full and relative paths are allowed. If used without the parameter -create, the blueprint file is applied. If used with the parameter -create, a blueprint file is created.
    8. -create
        - Creates a blueprint. Must be used with the parameter -blueprint.
    <br/>

3. terraformx destroy<br/><br/>

    The terraformx destroy command destroys the resources managed by the terraform root.<br/><br/>

    Optional Parameters:
    
    1. -ch-dir
        - Location of terraform root.
    2. -var-file
        - Location of variable definitions file.
    3. -auto-approve
        - Auto approve command without requiring user input.
    4. -override-workflow
        - Overrides workflow stages auto_approve keys and auto approves every stage.
    5. -refresh-only
        - Review how terraform would update your state file.
    6. -destroy-history
        - Destroys all terraform roots' managed resources in terraform_history.csv.
    <br/>

4. terraformx output<br/><br/>

    The terraformx output command is used to extract the value of output variables from the terraform root.<br/><br/>

    Optional Parameters:
    
    1. -ch-dir
        - Location of terraform root.
    <br/>

5. terraformx blueprints<br/><br/>

    The terraformx blueprints command is used to extract the value of output variables from the terraform root.<br/><br/>
    
    Optional Parameters:
    
    1. -file
        - Location of blueprint file. Full and relative paths are allowed. If used without the parameter -create, the blueprint file is applied. If used with the parameter -create, a blueprint file is created.
    2. -list
        - List terraform roots in a Blueprint.
    3. -create
        - Creates a blueprint. Must be used with -blueprint.
    <br/>

6. terraformx history<br/><br/>

    The terraformx blueprints command is used to extract the value of output variables from the terraform root.<br/><br/>

      Optional Parameters:
      
      1. -ch-dir
          - Location of terraform root.
      2. -destroy
          - Destroys all terraform roots' managed resources in terraform_history.csv.
      3. -list
          - List terraform roots in History.
      <br/>

7. terraformx list<br/><br/>

    The terraformx blueprints command is used to extract the value of output variables from the terraform root.<br/><br/>

      Optional Parameters:
      
      1. -blueprint
          - Location of blueprint file. Full and relative paths are allowed.
      2. -history
          - Destroys all terraform roots' managed resources in terraform_history.csv.
      <br/>

---
## Actions: Turns basic terraformx commands into executables for use in custom CI actions.

The code transforms the following features into exes for custom GitHub Actions:

1. Terraformx Apply
2. Terraformx Destroy
3. Terraformx Rebuild

Please refer to the earlier sections for their behaviours.