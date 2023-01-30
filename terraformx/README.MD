## To run terraformx commands via terraformx.py

In directory terraform_manager:

To set temporary path and alias:
export PYTHONPATH="${PYTHONPATH}:$PWD"
alias terraformx="python3 $PWD/terraformx/terraformx.py"

## To install Terraformx as a UNIX exe with pyinstaller --onefile perform the following commands

In directory terraformx run the following commands:
pyinstaller --onefile terraformx.py -p $(pwd)

To set temporary path and alias:

export PATH=$PATH:$(pwd)/dist/terraformx
alias terraformx=$(pwd)"/dist/terraformx"

To set permanent path and alias:

echo '\n# Setting PATH for terraformx
PATH="${PATH}:'$PWD'/dist/terraformx"
export PATH' >> ~/.zprofile

echo '\n# The next line updates alias for terraformx
alias terraformx="'$PWD'/dist/terraformx"' >> ~/.zshrc

Note: If you experience zsh permission denied error, execute this command in the terraformx directory
Give user exec permissions
chmod +x $(pwd)/dist/terraformx

## To install Terraformx as a UNIX exe with pyinstaller --onedir perform the following commands

In directory terraformx run the pyinstaller command:
pyinstaller --onedir terraformx.py -p $(pwd)

To set temporary path and alias:

export PATH=$PATH:$(pwd)/dist/terraformx/terraformx
alias terraformx=$(pwd)"/dist/terraformx/terraformx"

To set permanent path and alias:

echo '\n# Setting PATH for terraformx
PATH="${PATH}:'$PWD'/dist/terraformx/terraformx"
export PATH' >> ~/.zprofile

echo '\n# The next line updates alias for terraformx
alias terraformx="'$PWD'/dist/terraformx/terraformx"' >> ~/.zshrc

Note: If you experience zsh permission denied error, execute this command in the terraformx directory
Give user exec permissions
chmod +x $(pwd)/dist/terraformx
