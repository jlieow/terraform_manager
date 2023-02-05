import os
import sys
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from terraformx.parser_apply import *
from terraformx.terraformx import *

def main(blueprint_path):

    # top-level parser
    top_level_parser = argparse.ArgumentParser(description = "terraformx")
    top_level_parser.add_argument(Args_constants.BLUEPRINT, type = str, default=Default_constants.EMPTY_STRING, help = Help_constants.LOCATION_OF_BLUEPRINT_FILE)

    args = top_level_parser.parse_args()
    
    blueprint_path = args.blueprint
    
    if not os.path.exists(blueprint_path) or ".csv" not in blueprint_path:
        print_error("\n[ERROR] Unable to locate blueprint file in the specified directory: \n%s" % blueprint_path)
        return
    
    blueprint_path = os.path.abspath(blueprint_path)

    apply_blueprint(blueprint_path, github_action=True)

if __name__ == "__main__":
    main(sys.argv[1])