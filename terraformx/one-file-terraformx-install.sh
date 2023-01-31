set_path_alias() {
    echo '\n# Setting PATH for terraformx
    PATH="${PATH}:'$PWD'/dist/terraformx"
    export PATH' >> ~/.zprofile

    echo '\n# The next line updates alias for terraformx
    alias terraformx="'$PWD'/dist/terraformx"' >> ~/.zshrc
}

(
    pyinstaller --onefile terraformx.py -p $(pwd) -y 2> /dev/null &&
    set_path_alias
) || (
    set_path_alias
)