## Run following command to compile .py code into .exe for Terraform Manager features

### Recommended Install

terraformx:
1. For MacOS use HomeBrew:
- `brew tap jlieow/terraform-manager`
- `brew install terraformx-mac`

2. For MacOS download the latest version [here](https://github.com/jlieow/terraform_manager/releases). Place the executable in the folder and perform the following commands to add it to path.      
-     echo '\n# Setting PATH for terraformx
      PATH="${PATH}:'$PWD'"
      export PATH' >> ~/.zprofile
      
      
      echo '\n# The next line updates alias for terraformx
      alias terraformx="'$PWD'/dist/terraformx"' >> ~/.zshrc
      

3. For Windows, download the latest version [here](https://github.com/jlieow/terraform_manager/releases). Place the executable in the folder and set up path:

      Recommend to place the executable in `Program Files/Terraform Manager/cli`

      Add directory to PATH via System Properties > Advanced > Environmental Variables

### To install manually

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
  
  2. Run regedit and go to HKEY_LOCAL_MACHINE\Software\Microsoft\Command Processor

  3. Add String Value entry with the name AutoRun and the full path of your .bat/.cmd file.