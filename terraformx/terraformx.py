# importing required modules
import argparse

from init import *
from apply import *
from destroy import *
from output import *

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

    terraformx_init = subparsers.add_parser("init")
    terraformx_init.set_defaults(function=init)

    terraformx_apply = subparsers.add_parser("apply")
    terraformx_apply.set_defaults(function=apply)

    terraformx_destroy = subparsers.add_parser("destroy")
    terraformx_destroy.set_defaults(function=destroy)

    terraformx_output = subparsers.add_parser("output")
    terraformx_output.set_defaults(function=output)
    
    all_parsers = [
        terraformx_init, 
        terraformx_apply, 
        terraformx_destroy, 
        terraformx_output, 
        ]

    for parser in all_parsers:
        # arguments
        parser.add_argument("-dir", type = str, default="", help = "Location of terraform root.")
        parser.add_argument("-var-file", type = str, default="", help = "Location of variable definitions file.")
        parser.add_argument("-auto-approve", action="store_true", help = "Auto approve command.")
        parser.add_argument("-refresh-only", action="store_true", help = "Review how terraform would update your state file.")
    
    # parse the arguments and call the right function
    args = top_level_parser.parse_args()
    args.function(args)

if __name__ == "__main__":
    main()
