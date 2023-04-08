## Run following command to compile .py code into .exe for Terraform Manager features

For Mac:
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

For Windows:

  First install the following tools with PyInstaller:
  1. For terraformx:<br/><br/>

        In the root directory of terraformx, run:
        - `pyinstaller --onefile terraformx.py -p %cd% -y`
      <br/>

  After PyInstaller has completed follow the following instructions to set the alias:
  1. Create a .bat or .cmd file with your DOSKEY commands.
  - ```
    @echo off

    DOSKEY terraformx=D:\Documents\Projects\GitHub\terraform_manager\terraformx\dist\terraformx.exe```
  
  2. Run regedit and go to HKEY_CURRENT_USER\Software\Microsoft\Command Processor

  3. Add String Value entry with the name AutoRun and the full path of your .bat/.cmd file.