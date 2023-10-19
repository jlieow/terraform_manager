# importing required modules
import sys
import argparse
import os
from dotenv import load_dotenv

from terraformx.parser_init import *
from terraformx.parser_apply import *
from terraformx.parser_destroy import *
from terraformx.parser_output import *
from terraformx.parser_blueprints import *
from terraformx.parser_history import *
from terraformx.parser_list import *
from terraformx.parser_import import *
from terraformx.parser_state import *

class Parser_constants:
    INIT = "init"
    APPLY = "apply"
    DESTROY = "destroy"
    OUTPUT = "output"
    BLUEPRINTS = "blueprints"
    HISTORY = "history"
    LIST = "list"
    IMPORT = "import"
    STATE = "state"

class Args_constants:
    CHDIR = "-chdir"
    VAR_FILE = "-var-file"
    MIGRATE_STATE = "-migrate-state"
    AUTO_APPROVE = "-auto-approve"
    OVERRIDE_WORKFLOW = "-override-workflow"
    REFRESH_ONLY = "-refresh-only"
    DESTROY_HISTORY = "-destroy-history"
    REBUILD = "-rebuild"
    CREATE = "-create"
    FILE = "-file"
    BLUEPRINT = "-blueprint"
    LIST = "-list"
    DESTROY = "-destroy"
    HISTORY = "-history"
    ACTIVE_STAGES = "-active-stages"
    STRINGVARS = "stringvars"
    ADDRESS = "address"
    ID = "id"

class Action_constants:
    STORE_TRUE = "store_true"

class Default_constants:
    EMPTY_STRING = ""

class Help_constants:
    LOCATION_OF_TERRAFORM_ROOT = "Location of terraform root."
    LOCATION_OF_TFVARS_FILE = "Location of variable definitions file."
    LOCATION_OF_BLUEPRINT_FILE = "Location of blueprint file. Full and relative paths are allowed."
    LOCATION_OF_BLUEPRINT_FILE_CREATE = "Location of blueprint file. Full and relative paths are allowed. If used without the parameter -create, the blueprint file is applied. If used with the parameter -create, a blueprint file is created."
    MIGRATE_STATE_COMMAND = "Reconfigure a backend, and attempt to migrate any existing state."
    AUTO_APPROVE_COMMAND = "Auto approve command without requiring user input."
    OVERRIDE_WORKFLOW = "Overrides workflow stages auto_approve keys and auto approves every stage."
    TERRAFORM_STATE_FILE_REVIEW = "Review how terraform would update your state file."
    REBUILD = "Rebuild terraform by destroying and applying the script."
    DESTORY_ALL_IN_HISTORY = "Destroys all terraform roots' managed resources in terraform_history.csv."
    CREATE_BLUEPRINT = "Creates a blueprint. Must be used with -blueprint."
    LIST_BLUEPRINT = "List terraform roots in a Blueprint."
    LIST_HISTORY = "List terraform roots in History."
    ACTIVE_STAGES = "Specify the active stages overriding the active stages in the workflow."
    STRING_ARGUMENTS = "Specify the string arguments."
    ADDRESS = "Valid resource address, can import resources into modules as well as directly into the root of the state."
    ID = "ID of the resource to import."

top_level_help_message = "Usage: terraformx [global options] <subcommand> [args]\n\
\n\
The available commands for execution are listed below.\n\
The primary workflow commands are given first, followed by\n\
less common or more advanced commands.\n\
\n\
Main commands:\n\
  init          Prepare your working directory for other commands\n\
  apply         Create or update infrastructure\n\
  destroy       Destroy previously-created infrastructure\n\
  output        Output information about your infrastructure\n\
  import        Import existing infrastructure resources\n\
  rm            Remove a binding to an existing remote object without first destroying it"

def load_nt_env(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env = get_env_object()
                env[key] = value

def default(args):
    print(top_level_help_message)

def main():
    # export environmental variables from /config/.env if it exists
    if os.path.isfile(os.path.join("config", ".env")):
        if sys.platform == "win32":
            load_nt_env(os.path.join("config", ".env"))
        else:
            load_dotenv(os.path.join("config", ".env")) 
    

    # top-level parser
    top_level_parser = argparse.ArgumentParser(description = "terraformx")
    top_level_parser.set_defaults(function=default)

    subparsers = top_level_parser.add_subparsers(dest="command", help=top_level_help_message)

    terraformx_init = subparsers.add_parser(Parser_constants.INIT)
    terraformx_init.set_defaults(function=init)
    terraformx_init.add_argument(Args_constants.CHDIR, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_TERRAFORM_ROOT)
    terraformx_init.add_argument(Args_constants.VAR_FILE, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_TFVARS_FILE)
    terraformx_init.add_argument(Args_constants.MIGRATE_STATE, action=Action_constants.STORE_TRUE, help = Help_constants.MIGRATE_STATE_COMMAND)

    terraformx_apply = subparsers.add_parser(Parser_constants.APPLY)
    terraformx_apply.set_defaults(function=apply)
    terraformx_apply.add_argument(Args_constants.CHDIR, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_TERRAFORM_ROOT)
    terraformx_apply.add_argument(Args_constants.VAR_FILE, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_TFVARS_FILE)
    terraformx_apply.add_argument(Args_constants.AUTO_APPROVE, action=Action_constants.STORE_TRUE, help = Help_constants.AUTO_APPROVE_COMMAND)
    terraformx_apply.add_argument(Args_constants.OVERRIDE_WORKFLOW, action=Action_constants.STORE_TRUE, help = Help_constants.OVERRIDE_WORKFLOW)
    terraformx_apply.add_argument(Args_constants.REFRESH_ONLY, action=Action_constants.STORE_TRUE, help = Help_constants.TERRAFORM_STATE_FILE_REVIEW)
    terraformx_apply.add_argument(Args_constants.REBUILD, action=Action_constants.STORE_TRUE, help = Help_constants.REBUILD)
    terraformx_apply.add_argument(Args_constants.BLUEPRINT, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_BLUEPRINT_FILE_CREATE)
    terraformx_apply.add_argument(Args_constants.CREATE, action=Action_constants.STORE_TRUE, help = Help_constants.CREATE_BLUEPRINT)

    terraformx_destroy = subparsers.add_parser(Parser_constants.DESTROY)
    terraformx_destroy.set_defaults(function=destroy)
    terraformx_destroy.add_argument(Args_constants.CHDIR, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_TERRAFORM_ROOT)
    terraformx_destroy.add_argument(Args_constants.VAR_FILE, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_TFVARS_FILE)
    terraformx_destroy.add_argument(Args_constants.AUTO_APPROVE, action=Action_constants.STORE_TRUE, help = Help_constants.AUTO_APPROVE_COMMAND)
    terraformx_destroy.add_argument(Args_constants.OVERRIDE_WORKFLOW, action=Action_constants.STORE_TRUE, help = Help_constants.OVERRIDE_WORKFLOW)
    terraformx_destroy.add_argument(Args_constants.REFRESH_ONLY, action=Action_constants.STORE_TRUE, help = Help_constants.TERRAFORM_STATE_FILE_REVIEW)
    terraformx_destroy.add_argument(Args_constants.DESTROY_HISTORY, action=Action_constants.STORE_TRUE, help = Help_constants.DESTORY_ALL_IN_HISTORY)

    terraformx_output = subparsers.add_parser(Parser_constants.OUTPUT)
    terraformx_output.set_defaults(function=output)
    terraformx_output.add_argument(Args_constants.CHDIR, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_TERRAFORM_ROOT)

    # terraformx_blueprints = subparsers.add_parser(Parser_constants.BLUEPRINTS)
    # terraformx_blueprints.set_defaults(function=blueprints)
    # terraformx_blueprints.add_argument(Args_constants.FILE, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_BLUEPRINT_FILE_CREATE, required=True)
    # terraformx_blueprints.add_argument(Args_constants.LIST, action=Action_constants.STORE_TRUE, help = Help_constants.LIST_BLUEPRINT)
    # terraformx_blueprints.add_argument(Args_constants.CREATE, action=Action_constants.STORE_TRUE, help = Help_constants.CREATE_BLUEPRINT)

    # terraformx_history = subparsers.add_parser(Parser_constants.HISTORY)
    # terraformx_history.set_defaults(function=history)
    # terraformx_history.add_argument(Args_constants.CHDIR, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_TERRAFORM_ROOT)
    # terraformx_history.add_argument(Args_constants.DESTROY, action=Action_constants.STORE_TRUE, help = Help_constants.DESTORY_ALL_IN_HISTORY)
    # terraformx_history.add_argument(Args_constants.LIST, action=Action_constants.STORE_TRUE, help = Help_constants.LIST_HISTORY)

    # terraformx_list = subparsers.add_parser(Parser_constants.LIST)
    # terraformx_list.set_defaults(function=list)
    # terraformx_list.add_argument(Args_constants.BLUEPRINT, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_BLUEPRINT_FILE)
    # terraformx_list.add_argument(Args_constants.HISTORY, action=Action_constants.STORE_TRUE, help = Help_constants.LIST_HISTORY)
    
    terraformx_import = subparsers.add_parser(Parser_constants.IMPORT)
    terraformx_import.set_defaults(function=t_import)
    terraformx_import.add_argument(Args_constants.CHDIR, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_TERRAFORM_ROOT)
    terraformx_import.add_argument(Args_constants.VAR_FILE, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_TFVARS_FILE)
    terraformx_import.add_argument(Args_constants.ADDRESS, metavar="ADDRESS", type = str, help = Help_constants.ADDRESS)
    terraformx_import.add_argument(Args_constants.ID, metavar="ID", type = str, help = Help_constants.ID)

    terraformx_state_rm = subparsers.add_parser(Parser_constants.STATE)
    terraformx_state_rm.set_defaults(function=state_rm)
    terraformx_state_rm.add_argument(Args_constants.CHDIR, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_TERRAFORM_ROOT)
    terraformx_state_rm.add_argument(Args_constants.STRINGVARS, metavar = "N", type = str, nargs = "+", default=Default_constants.EMPTY_STRING, help = Help_constants.STRING_ARGUMENTS)

    # parse the arguments and call the right function
    args = top_level_parser.parse_args()
    args.function(args)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
