set_path_alias() {
    echo '\n# Setting PATH for terraformx
    PATH="${PATH}:'$PWD'/dist/terraformx/terraformx"
    export PATH' >> ~/.zprofile &&

    echo '\n# The next line updates alias for terraformx
    alias terraformx="'$PWD'/dist/terraformx/terraformx"' >> ~/.zshrc
}

set_path_alias_terraformx_sample1() {
    export PATH=$PATH:$(pwd)/dist/terraformx/terraformx
    alias terraformx_sample1=$(pwd)"/dist/terraformx/terraformx" 
    # echo $(terraformx_sample1)
}

set_path_alias_terraformx_sample2() {
    export PATH=$PATH:$(pwd)/dist/terraformx/terraformx
    alias terraformx_sample2=$(pwd)"/dist/terraformx/terraformx" 
    # echo $(terraformx_sample2)
}

(
    pyinstaller --onedir terraformx.py -p $(pwd) -y 2> /dev/null &&
    set_path_alias
) || (

    set_path_alias
)  
echo "Install complete"