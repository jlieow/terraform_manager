# importing required modules
import sys
import argparse

from terraformx.parser_init import *
from terraformx.parser_apply import *
from terraformx.parser_destroy import *
from terraformx.parser_output import *
from terraformx.parser_blueprints import *
from terraformx.parser_history import *
from terraformx.parser_list import *

class Parser_constants:
    INIT = "init"
    APPLY = "apply"
    DESTROY = "destroy"
    OUTPUT = "output"
    BLUEPRINTS = "blueprints"
    HISTORY = "history"
    LIST = "list"
class Args_constants:
    CHDIR = "-chdir"
    VAR_FILE = "-var-file"
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

class Action_constants:
    STORE_TRUE = "store_true"

class Default_constants:
    EMPTY_STRING = ""

class Help_constants:
    LOCATION_OF_TERRAFORM_ROOT = "Location of terraform root."
    LOCATION_OF_TFVARS_FILE = "Location of variable definitions file."
    LOCATION_OF_BLUEPRINT_FILE = "Location of blueprint file. Full and relative paths are allowed."
    LOCATION_OF_BLUEPRINT_FILE_CREATE = "Location of blueprint file. Full and relative paths are allowed. If used without the parameter -create, the blueprint file is applied. If used with the parameter -create, a blueprint file is created."
    AUTO_APPROVE_COMMAND = "Auto approve command without requiring user input."
    OVERRIDE_WORKFLOW = "Overrides workflow stages auto_approve keys and auto approves every stage."
    TERRAFORM_STATE_FILE_REVIEW = "Review how terraform would update your state file."
    REBUILD = "Rebuild terraform by destroying and applying the script."
    DESTORY_ALL_IN_HISTORY = "Destroys all terraform roots' managed resources in terraform_history.csv."
    CREATE_BLUEPRINT = "Creates a blueprint. Must be used with -blueprint."
    LIST_BLUEPRINT = "List terraform roots in a Blueprint."
    LIST_HISTORY = "List terraform roots in History."
    ACTIVE_STAGES = "Specify the active stages overriding the active stages in the workflow."


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
  output        Output information about your infrastructure"

def default(args):
    print(top_level_help_message)

def main():
    # top-level parser
    top_level_parser = argparse.ArgumentParser(description = "terraformx")
    top_level_parser.set_defaults(function=default)

    subparsers = top_level_parser.add_subparsers(dest="command", help=top_level_help_message)

    terraformx_init = subparsers.add_parser(Parser_constants.INIT)
    terraformx_init.set_defaults(function=init)
    terraformx_init.add_argument(Args_constants.CHDIR, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_TERRAFORM_ROOT)
    terraformx_init.add_argument(Args_constants.VAR_FILE, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_TFVARS_FILE)

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

    terraformx_blueprints = subparsers.add_parser(Parser_constants.BLUEPRINTS)
    terraformx_blueprints.set_defaults(function=blueprints)
    terraformx_blueprints.add_argument(Args_constants.FILE, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_BLUEPRINT_FILE_CREATE, required=True)
    terraformx_blueprints.add_argument(Args_constants.LIST, action=Action_constants.STORE_TRUE, help = Help_constants.LIST_BLUEPRINT)
    terraformx_blueprints.add_argument(Args_constants.CREATE, action=Action_constants.STORE_TRUE, help = Help_constants.CREATE_BLUEPRINT)

    terraformx_history = subparsers.add_parser(Parser_constants.HISTORY)
    terraformx_history.set_defaults(function=history)
    terraformx_history.add_argument(Args_constants.CHDIR, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_TERRAFORM_ROOT)
    terraformx_history.add_argument(Args_constants.DESTROY, action=Action_constants.STORE_TRUE, help = Help_constants.DESTORY_ALL_IN_HISTORY)
    terraformx_history.add_argument(Args_constants.LIST, action=Action_constants.STORE_TRUE, help = Help_constants.LIST_HISTORY)

    terraformx_list = subparsers.add_parser(Parser_constants.LIST)
    terraformx_list.set_defaults(function=list)
    terraformx_list.add_argument(Args_constants.BLUEPRINT, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_BLUEPRINT_FILE)
    terraformx_list.add_argument(Args_constants.HISTORY, action=Action_constants.STORE_TRUE, help = Help_constants.LIST_HISTORY)
    
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
