pyinstaller --onefile github_action_terraformx_apply.py -p $(pwd) -y
pyinstaller --onefile github_action_terraformx_destroy.py -p $(pwd) -y
pyinstaller --onefile github_action_terraformx_rebuild_using_destroy_apply.py -p $(pwd) -y
