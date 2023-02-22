# API Documentation for actions.

Actions turn terraformx commands into executables for use in custom CI actions.

---
### File Summary

Core features are broken down into the various files

1. [github_action_terraformx_apply_blueprint](#github_action_terraformx_apply_blueprint)
    - main
2. [github_action_terraformx_apply](#github_action_terraformx_apply)
    - github_action_apply_only
    - main
3. [github_action_terraformx_destroy](#github_action_terraformx_destroy)
    - github_action_destroy_only
    - main
4. [github_action_terraformx_rebuild_with_destroy_apply](#github_action_terraformx_rebuild_with_destroy_apply)
    - main

---
#### github_action_terraformx_apply_blueprint
- main 
    - Description
        - Entry point for Custom GitHub Action terraformx apply blueprint
    - Args
    - Return

---
#### github_action_terraformx_apply
- github_action_apply_only
    - Description
        - Perform terraformx apply when users use it through a custom GitHub action.
    - Args
        - cwd: string
        - var_file: string
        - auto_approve: boolean
        - override_workflow: boolean
        - github_action_active_stages: string
    - Return

- main
    - Description
        - Entry point for Custom GitHub Action terraformx apply
    - Args
    - Return

---
#### github_action_terraformx_destroy
- main
    - Description
        - Entry point for Custom GitHub Action terraformx destroy
    - Args
    - Return

---
#### github_action_terraformx_rebuild_with_destroy_apply
- main
    - Description
        - Entry point for Custom GitHub Action terraformx rebuild
    - Args
    - Return
