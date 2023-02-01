# importing required modules
import sys
import argparse

from init import *
from apply import *
from destroy import *
from output import *

class Parser_constants:
    INIT = "init"
    APPLY = "apply"
    DESTROY = "destroy"
    OUTPUT = "output"
    BLUEPRINTS = "blueprints"
    HISTORY = "history"
class Args_constants:
    DIR = "-dir"
    VAR_FILE = "-var-file"
    AUTO_APPROVE = "-auto-approve"
    OVERRIDE_WORKFLOW = "-override-workflow"
    REFRESH_ONLY = "-refresh-only"
    DESTROY_HISTORY = "-destroy-history"

class Action_constants:
    STORE_TRUE = "store_true"

class Default_constants:
    EMPTY_STRING = ""

class Help_constants:
    LOCATION_OF_TERRAFORM_ROOT = "Location of terraform root."
    LOCATION_OF_TFVARS_FILE = "Location of variable definitions file."
    AUTO_APPROVE_COMMAND = "Auto approve command without requiring user input."
    OVERRIDE_WORKFLOW = "Overrides workflow stages auto_approve keys and auto approves every stage."
    TERRAOFORM_STATE_FILE_REVIEW = "Review how terraform would update your state file."
    DESTORY_ALL_IN_HISTORY = "Destroys all in terraform_history.csv."


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
    terraformx_init.add_argument(Args_constants.DIR, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_TERRAFORM_ROOT)
    terraformx_init.add_argument(Args_constants.VAR_FILE, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_TFVARS_FILE)

    terraformx_apply = subparsers.add_parser(Parser_constants.APPLY)
    terraformx_apply.set_defaults(function=apply)
    terraformx_apply.add_argument(Args_constants.DIR, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_TERRAFORM_ROOT)
    terraformx_apply.add_argument(Args_constants.VAR_FILE, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_TFVARS_FILE)
    terraformx_apply.add_argument(Args_constants.AUTO_APPROVE, action=Action_constants.STORE_TRUE, help = Help_constants.AUTO_APPROVE_COMMAND)
    terraformx_apply.add_argument(Args_constants.OVERRIDE_WORKFLOW, action=Action_constants.STORE_TRUE, help = Help_constants.OVERRIDE_WORKFLOW)
    terraformx_apply.add_argument(Args_constants.REFRESH_ONLY, action=Action_constants.STORE_TRUE, help = Help_constants.TERRAOFORM_STATE_FILE_REVIEW)

    terraformx_destroy = subparsers.add_parser(Parser_constants.DESTROY)
    terraformx_destroy.set_defaults(function=destroy)
    terraformx_destroy.add_argument(Args_constants.DIR, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_TERRAFORM_ROOT)
    terraformx_destroy.add_argument(Args_constants.VAR_FILE, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_TFVARS_FILE)
    terraformx_destroy.add_argument(Args_constants.AUTO_APPROVE, action=Action_constants.STORE_TRUE, help = Help_constants.AUTO_APPROVE_COMMAND)
    terraformx_destroy.add_argument(Args_constants.OVERRIDE_WORKFLOW, action=Action_constants.STORE_TRUE, help = Help_constants.OVERRIDE_WORKFLOW)
    terraformx_destroy.add_argument(Args_constants.REFRESH_ONLY, action=Action_constants.STORE_TRUE, help = Help_constants.TERRAOFORM_STATE_FILE_REVIEW)
    terraformx_destroy.add_argument(Args_constants.DESTROY_HISTORY, action=Action_constants.STORE_TRUE, help = Help_constants.DESTORY_ALL_IN_HISTORY)

    terraformx_output = subparsers.add_parser(Parser_constants.OUTPUT)
    terraformx_output.set_defaults(function=output)
    terraformx_output.add_argument(Args_constants.DIR, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_TERRAFORM_ROOT)
    
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
