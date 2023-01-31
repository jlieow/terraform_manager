set_path_alias() {
    echo '\n# Setting PATH for Terraform Manager
    PATH="${PATH}:'$PWD'/dist/main/main"
    export PATH' >> ~/.zprofile &&

    echo '\n# The next line updates alias for Terraform Manager
    alias terraform_manager="'$PWD'/dist/main/main"' >> ~/.zshrc
}

set_path_alias_terraform_manager1() {
    export PATH=$PATH:$(pwd)/dist/main/main
    alias terraform_manager1=$(pwd)"/dist/main/main" 
    # echo $(terraform_manager1)
}

set_path_alias_terraform_manager1() {
    export PATH=$PATH:$(pwd)/dist/main/main
    alias terraform_manager2=$(pwd)"/dist/main/main" 
    # echo $(terraform_manager2)
}

(
    pyinstaller --onedir main.py -p $(pwd) -y 2> /dev/null &&
    set_path_alias
) || (

    set_path_alias
)  
echo "Install complete"