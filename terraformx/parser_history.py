# import os

# from terraformx.terraformx_common import *
# from utils.terraform import *
# from utils import *

# def history(args):

#     destroy = args.destroy
#     list = args.list

#     if list:
#         history_path = os.path.join(get_dir_of_terraform_manager(), History_constants.HISTORY_CSV_PATH)

#         histories = get_rows_as_list(history_path)

#         list_history(histories, turn_high_alert_on=False)

#         if destroy:
#             print_warning("\nIf -list flag is active, -destroy flag will be ignored.")
#         return

#     if destroy:
#         terraform_destroy_from_history()
#         return