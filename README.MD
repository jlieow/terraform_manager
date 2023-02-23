# Terraform Manager

Terraform Manager extends the Terraform CLI with additional functonalities and aids to standardize Terraform code structure throughout the entire development lifecycle to enable more consistent Ops deployment of Terraform for use cases such as GitOps.

Terraform Manager consists of 3 parts:
1. Utils: Core Features of Terraform Manager
2. Terraformx: Extends Terraform Manager core features into a CLI
3. Actions: Turns basic terraformx commands into executables for use in custom CI actions.

Please refer to **/docs/README.MD** for an explanation of the purpose and features regarding each of the 3 parts. 
Please refer to **/utils/README.MD**, **/terraformx/README.MD** and **/actions/README.MD** for more details about the functions contained in their respective directories. 

The following sections will detail how to install Terraform Manager.

---
## To install python dependencies

`pip install -r requirements.txt`

---
## To generate new requirements.txt

`pip install pipreqs`
`python -m pipreqs.pipreqs .`

---
## Run following command to compile .py code into .exe for Terraform Manager features

1. For terraform_manager:<br/><br/>
      
      In the root directory of terraform_manager, use the following shell scripts to install the exe and update the PATH and alias:

      - `one-dir-terraform-manager-install.sh`
      - `one-file-terraform-manager-install.sh`
      <br/>

2. For terraformx:<br/><br/>

      In the root directory of terraformx, use the following shell scripts to install the exe and update the PATH and alias:
      - `one-dir-terraformx-install.sh`
      - `one-file-terraformx-install.sh`
      <br/>

3. To compile exe for custom GitHub actions:<br/><br/>  

      In the root directory of actions, use the following shell scripts to install the exe and update the PATH and alias:
      - `one-file-github-action-terraformx-apply-install.sh`
      - `one-file-github-action-terraformx-destroy-install.sh`
      - `one-file-github-action-terraformx-rebuild-with-destroy-apply-install.sh`
      <br/>

Troubleshooting install/execution errors:
1. Permission denied error during exe execution
    - use the following command to give user exec permissions to the executable. 
      For example:
      chmod +x $(pwd)/dist/terraformx

2. Cannot find module error during exe execution.
    - PyInstaller might not pick up local import and dependencies. If so, one solution is to include the root folder into the Python path.

---
# Run tests with the following methods

1. To run a single test module, in this case test_antigravity.py:

    - To run a single test module, in this case test_antigravity.py:
      `python -m unittest test.test_antigravity`
      <br/>

2. Running a single test case or test method:

    - Also you can run a single TestCase or a single test method:
      `python -m unittest test.test_antigravity.GravityTestCase`
      <br/>

3. Running all tests:

    - This command will discover and run all the tests for you, they must be modules or packages named test\*.py (can be changed with the -p, --pattern flag):
      `python -m unittest`