# API Documentation for terraformx.

Terraformx provides Terraform Manager core features in a CLI.

---
### File Summary

Core features are broken down into the various files

1. [parser_apply](#parser_apply)
    - apply_rebuild_true
    - apply_only
    - blueprints
    - apply
2. [parser_blueprints](#parser_blueprints)
    - create_blueprint
    - apply_blueprint_via_github_action
    - apply_blueprint_via_terraformx
    - apply_blueprint
    - blueprints
3. [parser_destroy](#parser_destroy)
    - destroy_only
    - destroy
4. [parser_history](#parser_history)
    - history
5. [parser_init](#parser_init)
    - init
6. [parser_list](#parser_list)
    - list
7. [parser_output](#parser_output)
    - output
8. [terraformx_common](#terraformx_common)
    - get_cwd
    - get_full_path_else_return_empty_str
9. [terraformx](#terraformx)
    - default
    - main

---
#### parser_apply
- apply_rebuild_true
    - Description
        - Rebuild resources when users use CLI command terraformx apply.
    - Args
        - cwd: string
        - var_file: string
    - Return

- apply_only
    - Description
        - Provision resources when users use CLI command terraformx apply.
    - Args
        - cwd: string
        - var_file: string
        - auto_approve: boolean
        - override_workflow: boolean
    - Return

- blueprints
    - Description
        - Apply or create blueprint when users use CLI command terraformx apply blueprint.
    - Args
        - blueprint_file: string
        - create: boolean
    - Return
    
- apply
    - Description
        - Terraform Manager CLI: terraformx apply
    - Args
        - args: args()
    - Return

---
#### parser_blueprints
- create_blueprint
    - Description
        - Create blueprint when users use CLI command terraformx blueprints.
    - Args
        - blueprint_path: string
    - Return

- apply_blueprint_via_github_action
    - Description
        - Apply blueprint when users use it through a custom GitHub action and a workflow config.yaml exists.
    - Args
        - blueprint: string
    - Return

- apply_blueprint_via_terraformx
    - Description
        - Apply blueprint when users use CLI command terraformx blueprints and a workflow config.yaml exists.
    - Args
        - blueprint: string
    - Return

- apply_blueprint
    - Description
        - Apply blueprint when users use CLI command terraformx blueprints.
    - Args
        - blueprint_path: string
        - github_action: boolean
    - Return

- blueprints
    - Description
        - Terraform Manager CLI: terraformx blueprints
    - Args
        - args: args()
    - Return

---
#### parser_destroy
- destroy_only
    - Description
        - Destroy resources when users use CLI command terraformx destroy.
    - Args
        - cwd: string
        - var_file: string
        - auto_approve: boolean
        - override_workflow: boolean
    - Return

- destroy
    - Description
        - Terraform Manager CLI: terraformx destroy
    - Args
        - args: args()
    - Return

---
#### parser_history
- history
    - Description
        - Terraform Manager CLI: terraformx list
    - Args
        - args: args()
    - Return

---
#### parser_init
- init
    - Description
        - Terraform Manager CLI: terraformx init
    - Args
        - args: args()
    - Return

---
#### parser_list
- list
    - Description
        - Terraform Manager CLI: terraformx list
    - Args
        - args: args()
    - Return

---
#### parser_output
- output
    - Description
        - Terraform Manager CLI: terraformx output
    - Args
        - args: args()
    - Return

---
#### terraformx_common
- get_cwd
    - Description
        - Determines which directory to use
    - Args
        - dir: string
    - Return
        - cwd: string

- get_full_path_else_return_empty_str
    - Description
        - Returns full path
    - Args
        - path: string
        - optional_ext: string
    - Return
        - full_path: string

---
#### terraformx
- default
    - Description
        - Prints help message
    - Args
    - Return

- main
    - Description
        - Entry point for cmd line
    - Args
    - Return
