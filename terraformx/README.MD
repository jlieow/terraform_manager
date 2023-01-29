# Run following command to compile .py code into .exe

pyinstaller --onefile terraformx.py -p $(pwd)

update path at /etc/paths
vi ~/.zprofile

PATH="/Library/Frameworks/Python.framework/Versions/3.11/bin:/Users/jeromelieow/Documents/GitHub/terraform_manager/terraformx/dist/terraformx:${PATH}"

## Add terraformx commands via alias

vi ~/.zshrc

alias terraformx="python3 /Users/jeromelieow/Documents/GitHub/terraform_manager/terraformx/main.py"

export PATH=$PATH:/Users/jeromelieow/Documents/GitHub/terraform_manager/terraformx/dist/terraformx
alias terraformx="/Users/jeromelieow/Documents/GitHub/terraform_manager/terraformx/dist/terraformx"
