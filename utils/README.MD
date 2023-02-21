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
2. [common](####common)
    - check_if_terraform_manager_root_is_valid
    - get_dir_of_terraform_manager
    - input_options
    - get_rows_as_list
3. [credentials](####credentials)
    - import_aws_profiles
4. [drift](####drift)
    - function
5. [history](####history)
    - list_history
    - add_history
    - delete_latest_row_from_history
6. [print_options](####print_options)
    - print_normal
    - print_error
    - print_warning
    - print_success
    - print_alert
    - print_high_alert
    - print_info
7. [terraform_commands](####terraform_commands)
    - tfvars_settings
    - terraform_init
    - terraform_apply
    - terraform_destroy
    - terraform_output
    - terraform_apply_refresh
    - terraform_plan_refresh
    - terraform_apply_auto_approve_refresh
    - locate_terraform_root_directories
8. [terraform](####terraform)
    - terraform
    - terraform_workflow
    - terraform_destroy_from_history
    - terraform_check_for_drift
    - terraform_multi_build
    - terraform_blueprints
9. [workflow](####workflow)
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
- add_blueprint_rows
- is_this_a_verified_blueprint
- add_blueprint_row
- list_blueprint
- terraform_create_blueprint

---
#### Common

---
#### Credentials

---
#### Drift

---
#### History

---
#### Print_options

---
#### Terraform_commands

---
#### Terraform

---
#### Workflow