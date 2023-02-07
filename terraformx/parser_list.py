import os

from terraformx.terraformx_common import *
from utils.terraform import *
from utils import *

def list(args):

    blueprint = args.blueprint
    history = args.history

    if len(blueprint) > 0:
        blueprint_path = get_full_path_else_return_empty_str(blueprint, ".csv")
        if not os.path.exists(blueprint_path):
            print_error("\n[ERROR] Unable to locate blueprint file.")
            return 
        
        if list:
            rows = get_rows_as_list(blueprint_path)
            list_blueprint(rows)
            return

    if history:
        history_path = get_dir_of_terraform_manager() + History_constants.HISTORY_CSV_PATH

        histories = get_rows_as_list(history_path)

        list_history(histories)
        return