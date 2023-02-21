# API Documentation for utils

Utils contain Terraform Manager's core feature which build on top of Terraform CLI to provide a few additional features

---
### File Summary

Core features are broken down into the various files

1. [blueprints](#blueprints)
    - add_blueprint
    - add_blueprint_rows
    - is_this_a_verified_blueprint
    - add_blueprint_row
    - list_blueprint
    - terraform_create_blueprint
2. [common](#common)
    - check_if_terraform_manager_root_is_valid
    - get_dir_of_terraform_manager
    - input_options
    - get_rows_as_list
3. [credentials](#credentials)
    - import_aws_profiles
4. [drift](#drift)
    - terraform_apply_refresh_or_apply_all
5. [history](#history)
    - list_history
    - add_history
    - delete_latest_row_from_history
6. [print_options](#print_options)
    - print_normal
    - print_error
    - print_warning
    - print_success
    - print_alert
    - print_high_alert
    - print_info
7. [terraform_commands](#terraform_commands)
    - tfvars_settings
    - terraform_init
    - terraform_apply
    - terraform_destroy
    - terraform_output
    - terraform_apply_refresh
    - terraform_plan_refresh
    - terraform_apply_auto_approve_refresh
    - locate_terraform_root_directories
8. [terraform](#terraform)
    - terraform
    - terraform_workflow
    - terraform_destroy_from_history
    - terraform_check_for_drift
    - terraform_multi_build
    - terraform_blueprints
9. [workflow](#workflow)
    - is_workflow_file_ignored
    - is_stage_auto_approve
    - does_stage_name_exist
    - github_action_get_active_stages_from_workflow
    - get_active_stages_from_workflow
    - get_active_stage_names_from_workflow
    - get_active_stages_and_stage_names_from_workflow
    - get_stages_to_apply_from_active_stages
    - does_workflow_file_exist
    - get_number_of_resources_from_workflow
    - get_number_of_resources_from_maintf
    - get_list_of_resources_from_workflow
    - get_list_of_resources_from_maintf
    - does_workflow_file_contain_duplicates
    - does_workflow_objects_exist_in_maintf
    - does_workflow_contain_error_and_warnings
    - get_targets
    - get_stage
    - get_stages
    - workflow_terraform_apply
    - workflow_terraform_destroy
    - workflow_terraform_apply_refresh
    - workflow_terraform_plan_refresh
    - check_stages_errors
    - workflow_terraform_apply_active_stages
    - github_action_stage_workflow_terraform_apply
    - stage_workflow_terraform_apply
    - workflow_terraform_destroy_active_stages
    - github_action_stage_workflow_terraform_destroy
    - stage_workflow_terraform_destroy
    - stage_workflow_terraform_apply_refresh

---
#### Blueprints

- add_blueprint
    - Description
        - Create blueprint with single row
    - Args
        - blueprint_path: string
        - rows: string
        - mkdir: boolean
    - Return

- add_blueprint_rows
    - Description
        - Create blueprint with multiple rows
    - Args
        - blueprint_path: string
        - rows: string
        - mkdir: boolean
    - Return

- is_this_a_verified_blueprint
    - Description
        - Checks if blueprint is valid
    - Args
        - blueprint_path: string
    - Return
        - is_blueprint_valid: boolean

- add_blueprint_row
    - Description
        - Request for user input on which terraform root to add to blueprint
    - Args
        - terraform_root_dir: string
    - Return
        - blueprint: string[]

- list_blueprint
    - Description
        - List resources in the current blueprint
    - Args
        - blueprint: string[]
    - Return

- terraform_create_blueprint
    - Description
        - Requests for user input to choose the terraform root to create a blueprint
    - Args
    - Return

---
#### Common
- check_if_terraform_manager_root_is_valid
    - Description
        - Checks if the directory provided is a valid terraform root and returns a boolean
    - Args
        - directory: string
    - Return
        - valid_terraform_root: boolean

- get_dir_of_terraform_manager
    - Description
        - Returns the absolute path of terraform manager
    - Args
    - Return
        - terraform_manager_path: string

- input_options
    - Description
        - Returns a question with a set of options that requires user input
    - Args
        - preface: string
        - options: string
        - input_question: string
        - return_input: boolean
        - use_prev_as_default: boolean
        - choice: int
        - allow_special_break: boolean
        - special_break: string
    - Return
        - choice: int

- get_rows_as_list
    - Description
        - Return rows in a csv as a string array
    - Args
        - path: string
    - Return
        - rows: string[]

---
#### Credentials
- import_aws_profiles
    - Description
        - Import aws profiles using aws configure 
    - Args
    - Return

---
#### Drift
- terraform_apply_refresh_or_apply_all
    - Description
        - Request for user input on how to resolve drift 
    - Args
        - drifted_terraform_roots: string[]
    - Return

---
#### History
- list_history
    - Description
        - Evaluates rows in history.csv as a string array and prints warnings
    - Args
        - histories: string[]
        - turn_high_alert_on: boolean
    - Return

- add_history
    - Description
        - Adds a new row in history.csv based on the cwd
    - Args
        - cwd: string
        - stage_name: string
        - unit_testing: boolean
        - unit_testing_path: string
    - Return

- delete_latest_row_from_history
    - Description
        - Removes the latest row in history.csv based on the cwd
    - Args
        - cwd: string
        - stage_name: string
        - unit_testing: boolean
        - unit_testing_path: string
    - Return

---
#### Print_options
- print_normal
    - Description
        - Print normal messages
    - Args
        - message: string
        - disable_print: boolean
    - Return

- print_error
    - Description
        - Print error messages
    - Args
        - message: string
        - disable_print: boolean
    - Return

- print_warning
    - Description
        - Print warning messages
    - Args
        - message: string
        - disable_print: boolean
    - Return

- print_success
    - Description
        - Print success messages
    - Args
        - message: string
        - disable_print: boolean
    - Return

- print_alert
    - Description
        - Print alert messages
    - Args
        - message: string
        - disable_print: boolean
    - Return

- print_high_alert
    - Description
        - Print high alert messages
    - Args
        - message: string
        - disable_print: boolean
    - Return

- print_info
    - Description
        - Print informational messages
    - Args
        - message: string
        - disable_print: boolean
    - Return

---
#### Terraform_commands
- tfvars_settings
    - Description
        - Find all tfvars files in the terraform root, concat them and place the results in /config/settings.tfvars
    - Args
        - cwd: string
    - Return

- terraform_init
    - Description
        - Performs terraformx init
    - Args
        - cwd: string
        - CUSTOM_VAR_FILE: string
        - set_stdin: subprocess()
        - set_stdout: subprocess()
        - set_stderr: subprocess()
    - Return

- terraform_apply
    - Description
        - Performs terraformx apply
    - Args
        - cwd: string
        - CUSTOM_VAR_FILE: string
        - AUTO_APPROVE: boolean
        - github_action: boolean
        - set_stdin: subprocess()
        - set_stdout: subprocess()
        - set_stderr: subprocess()
    - Return

- terraform_destroy
    - Description
        - Performs terraformx destroy
    - Args
        - cwd: string
        - CUSTOM_VAR_FILE: string
        - AUTO_APPROVE: boolean
        - github_action: boolean
        - set_stdin: subprocess()
        - set_stdout: subprocess()
        - set_stderr: subprocess()
    - Return

- terraform_output
    - Description
        - Performs terraformx output
    - Args
        - cwd: string
        - set_stdin: subprocess()
        - set_stdout: subprocess()
        - set_stderr: subprocess()
    - Return

- terraform_apply_refresh
    - Description
        - Performs terraformx apply refresh
    - Args
        - cwd: string
        - AUTO_APPROVE: boolean
    - Return

- terraform_plan_refresh
    - Description
        - Performs terraformx plan refresh
    - Args
        - cwd: string
    - Return

- terraform_apply_auto_approve_refresh
    - Description
        - Performs terraformx apply auto refresh
    - Args
        - cwd: string
    - Return

- locate_terraform_root_directories
    - Description
        - Returns list of terraform roots as a string array
    - Args
        - root_directory: string
    - Return
        - list_terraform_root_dir: string[]

---
#### Terraform
- terraform
    - Description
        - Requests for user input on which terraformx action to apply
    - Args
    - Return

- terraform_workflow
    - Description
        - Requests for user input on which terraformx action to apply for a workflow
    - Args
    - Return

- terraform_destroy_from_history
    - Description
        - Destroys resources based on history
    - Args
    - Return

- terraform_check_for_drift
    - Description
        - Performs configuration drift check on terraform roots found in the folder
    - Args
    - Return

- terraform_multi_build
    - Description
        - Requests for user input regarding the terraform roots they would like to add to a blueprint
    - Args
    - Return

- terraform_blueprints
    - Description
        - Requests for user input regarding the action they would like to take with blueprints
    - Args
    - Return

---
#### Workflow
- is_workflow_file_ignored
    - Description
        - Check if workflow config.yaml can be ignored and returns a boolean
    - Args
        - path: string
    - Return
        - ignore: boolean

- is_stage_auto_approve
    - Description
        - Check if stage can be auto approved and returns a boolean
    - Args
        - path: string
    - Return
        - auto_approve: boolean

- does_stage_name_exist
    - Description
        - Check if stage name exists and returns a boolean
    - Args
        - cwd: string
        - stage_name: string
    - Return
        - exist: boolean

- github_action_get_active_stages_from_workflow
    - Description
        - Github Action to get the active stages from workflow and return them with any errors
    - Args
        - cwd: string
    - Return
        - active_stages: string[]
        - err: boolean
        - err_message: string

- get_active_stages_from_workflow
    - Description
        - Get the active stages from workflow and return them with any errors
    - Args
        - cwd: string
    - Return
        - active_stages: string[]
        - err: boolean
        - err_message: string

- get_active_stage_names_from_workflow
    - Description
        - Get the active stage names from workflow and return them with any errors
    - Args
        - cwd: string
    - Return
        - active_stages: string[]
        - err: boolean
        - err_message: string

- get_active_stages_and_stage_names_from_workflow
    - Description
        - Get the actives stages and stage names from workflow and return them with any errors
    - Args
        - cwd: string
    - Return
        - active: string[]
        - err: boolean
        - err_message: string

- get_stages_to_apply_from_active_stages
    - Description
        - Compare the active stages against existing stages and return only the active stages
    - Args
        - active_stages: string[]
        - stages: string
    - Return
        - new_stages: string[]

- does_workflow_file_exist
    - Description
        - Return a boolean indicating if workflow file exists
    - Args
        - cwd: string
    - Return
        - does_workflow_file_exist: boolean

- get_number_of_resources_from_workflow
    - Description
        - Return an integer reflecting the number of resources in workflow config.yaml
    - Args
        - workflow_config_path: string
    - Return
        - number_of_resources: int

- get_number_of_resources_from_maintf
    - Description
        - Return an integer reflecting the number of resources in main.tf
    - Args
        - main_tf_path: string
    - Return
        - number_of_resources: int

- get_list_of_resources_from_workflow
    - Description
        - Return a list of resources from workflow config.yaml
    - Args
        - workflow_config_path: string
    - Return
        - list_of_resources: string[]

- get_list_of_resources_from_maintf
    - Description
        - Return a list of resources from main.tf
    - Args
        - maintf_path: string
    - Return
        - list_of_resources: string[]

- does_workflow_file_contain_duplicates
    - Description
        - Return a boolean to indicate if workflow config.yaml contains duplicate objects
    - Args
        - workflow_resources: string[]
    - Return
        - does_objects_exist_in_maintf: boolean

- does_workflow_objects_exist_in_maintf
    - Description
        - Return a boolean to indicate if workflow config.yaml objects exist in main.tf
    - Args
        - workflow_resources: string[]
        - maintf_resources: string[]
        - disable_print: boolean
    - Return
        - does_objects_exist_in_maintf: boolean

- does_workflow_contain_error_and_warnings
    - Description
        - Return a boolean to indicate if the workflow has errors
    - Args
        - cwd: string
    - Return
        - contains_error_and_warnings: boolean

- get_targets
    - Description
        - Return targets as a string array
    - Args
        - test: {
                target: [
                    key: value
                ]
            }
    - Return
        - targets: string[]

- get_stage
    - Description
        - Return one stage
    - Args
        - cwd: string
        - stage_name: string
    - Return
        - stages: {
                    stage_name: string,
                    stage_auto_approve: boolean,
                    stage_targets: string[],
                }
            

- get_stages
    - Description
        - Return list of stages and stage errors.
    - Args
        - cwd: string
    - Return
        - stages: [
                {
                    stage_name: string,
                    stage_auto_approve: boolean,
                    stage_targets: string[],
                }
            ]
        - stages_errors: [
                {
                    error: boolean,
                    stage_name: string,
                    stage_auto_approve_error_message: string,
                    stage_targets: string,
                }
            ]

- workflow_terraform_apply
    - Description
        - Perform terraformx apply on each stage.
    - Args
        - cwd: string
        - stage_targets: string[]
        - stage_name: boolean
        - AUTO_APPROVE: boolean
        - github_action: boolean
    - Return

- workflow_terraform_destroy
    - Description
        - Perform terraformx destroy on each stage.
    - Args
        - cwd: string
        - stage_targets: string[]
        - stage_name: boolean
        - AUTO_APPROVE: boolean
        - github_action: boolean
    - Return

- workflow_terraform_apply_refresh
    - Description
        - Perform terraformx apply refresh on each stage.
    - Args
        - cwd: string
        - stage_targets: string[]
        - AUTO_APPROVE: boolean
    - Return

- workflow_terraform_plan_refresh
    - Description
        - Perform terraformx plan refresh on each stage.
    - Args
        - cwd: string
        - stage_targets: string[]
    - Return

- check_stages_errors
    - Description
        - Print errors in the stages
    - Args
        - stages_errors: stages_errors()
    - Return

- workflow_terraform_apply_active_stages
    - Description
        - Perform terraformx apply on each stage.
    - Args
        - cwd: string
        - stage: stage()
        - override_workflow: boolean
        - github_action: boolean
    - Return

- github_action_stage_workflow_terraform_apply
    - Description
        - Github Action to perform terraformx apply on each stage.
    - Args
        - cwd: string
        - override_workflow: boolean
        - active_stages_statements: string
    - Return

- stage_workflow_terraform_apply
    - Description
        - Perform terraformx apply on all stages.
    - Args
        - cwd: string
        - override_workflow: boolean
        - active_stages_statements: string
    - Return

- workflow_terraform_destroy_active_stages
    - Description
        - Perform terraformx destroy on each stage.
    - Args
        - cwd: string
        - stage: stage()
        - override_workflow: boolean
        - github_action: boolean
    - Return

- github_action_stage_workflow_terraform_destroy
    - Description
        - Github Action to perform terraformx destroy on each stage.
    - Args
        - cwd: string
        - override_workflow: boolean
        - active_stages_statements: string
    - Return

- stage_workflow_terraform_destroy
    - Description
        - Perform terraformx destroy on all stages.
    - Args
        - cwd: string
        - override_workflow: boolean
        - active_stages_statements: string
    - Return

- stage_workflow_terraform_apply_refresh
    - Description
        - Perform terraformx apply refresh on all stages.
    - Args
        - cwd: string
    - Return