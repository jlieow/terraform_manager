set_path_alias() {
    echo '\n# Setting PATH for Terraform Manager
    PATH="${PATH}:'$PWD'/dist/main"
    export PATH' >> ~/.zprofile

    echo '\n# The next line updates alias for Terraform Manager
    alias terraform_manager="'$PWD'/dist/main"' >> ~/.zshrc
}

(
    pyinstaller --onefile main.py -y 2> /dev/null &&
    set_path_alias
) || (
    set_path_alias
)

echo "
Install complete...
Please use command terraform_manager to instantiate the program.
"