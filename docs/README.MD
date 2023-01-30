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
