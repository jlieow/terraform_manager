pyinstaller --onedir terraformx.py -p $(pwd) -y

echo '\n# Setting PATH for terraformx
PATH="${PATH}:'$PWD'/dist/terraformx/terraformx"
export PATH' >> ~/.zprofile

echo '\n# The next line updates alias for terraformx
alias terraformx="'$PWD'/dist/terraformx/terraformx"' >> ~/.zshrc