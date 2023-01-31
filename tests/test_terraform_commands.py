import os
import unittest

from utils import terraform_commands

class TerraformCommandsTestSuite(unittest.TestCase):
    """Common test cases."""

    def test_get_terraform_root_directories(self):
        
        # example_terraform_root_directories contains 3 directories
        # 2 are terraform root directories as they contain backend.tf files

        root_directory = "./test_data/terraform_commands/example_terraform_root_directories"

        EXPECTED_TERRAFORM_ROOT_DIR = [
            "./test_data/terraform_commands/example_terraform_root_directories/example_terraform_root_directory",
            "./test_data/terraform_commands/example_terraform_root_directories/example_second_terraform_root_directory"
            ]

        list_terraform_root_dir = terraform_commands.locate_terraform_root_directories(root_directory)

        list_terraform_root_dir.sort()
        EXPECTED_TERRAFORM_ROOT_DIR.sort()

        if list_terraform_root_dir == EXPECTED_TERRAFORM_ROOT_DIR:
            assert True
        else:
            assert False

    # test case to check tfvars_settings()
    def test_tfvars_settings(self):
        
        #Test if tfvars_settings work with both config dir and settings.tfvars file present
        cwd_tfvars_settings_config_dir_exist_settings_tfvars_exist = "./test_data/terraform_commands/tfvars_settings_config_dir_exist_settings_tfvars_exist"
        try:
            terraform_commands.tfvars_settings(cwd_tfvars_settings_config_dir_exist_settings_tfvars_exist)
        except:
            assert False


        #Test if tfvars_settings work with only config dir present
        cwd_tfvars_settings_config_dir_exist_settings_tfvars_exist = "./test_data/terraform_commands/tfvars_settings_only_config_dir_exist"

        ext_config_settings_tfvars = "/config/settings.tfvars"
        
        # Check for and remove settings.tfvars if present before beginning test
        if os.path.exists(cwd_tfvars_settings_config_dir_exist_settings_tfvars_exist + ext_config_settings_tfvars):
            print("settings.tfvars is present")
            os.remove(cwd_tfvars_settings_config_dir_exist_settings_tfvars_exist + ext_config_settings_tfvars)
        
        try:
            terraform_commands.tfvars_settings(cwd_tfvars_settings_config_dir_exist_settings_tfvars_exist)
        except:
            assert False

        if os.path.exists(cwd_tfvars_settings_config_dir_exist_settings_tfvars_exist + ext_config_settings_tfvars):
            print("settings.tfvars is present")
            os.remove(cwd_tfvars_settings_config_dir_exist_settings_tfvars_exist + ext_config_settings_tfvars)
        
        #Test if tfvars_settings work when both config dir and settings.tfvars are not presents
        cwd_tfvars_settings_config_dir_and_settings_tfvars_do_not_exist = "./test_data/terraform_commands/tfvars_settings_config_dir_and_settings_tfvars_do_not_exist"

        ext_config_settings_tfvars = "/config/settings.tfvars"
        ext_config_dir = "/config"

        # Check for and remove settings.tfvars and config dir if present before beginning test
        if os.path.exists(cwd_tfvars_settings_config_dir_and_settings_tfvars_do_not_exist + ext_config_settings_tfvars):
            print("settings.tfvars is present")
            os.remove(cwd_tfvars_settings_config_dir_and_settings_tfvars_do_not_exist + ext_config_settings_tfvars)
        
        if os.path.exists(cwd_tfvars_settings_config_dir_and_settings_tfvars_do_not_exist + ext_config_dir):
            print("settings.tfvars is present")
            os.rmdir(cwd_tfvars_settings_config_dir_and_settings_tfvars_do_not_exist + ext_config_dir)

        try:
            terraform_commands.tfvars_settings(cwd_tfvars_settings_config_dir_and_settings_tfvars_do_not_exist)
        except:
            assert False

        if os.path.exists(cwd_tfvars_settings_config_dir_and_settings_tfvars_do_not_exist + ext_config_settings_tfvars):
            print("settings.tfvars is present")
            os.remove(cwd_tfvars_settings_config_dir_and_settings_tfvars_do_not_exist + ext_config_settings_tfvars)
        
        if os.path.exists(cwd_tfvars_settings_config_dir_and_settings_tfvars_do_not_exist + ext_config_dir):
            print("settings.tfvars is present")
            os.rmdir(cwd_tfvars_settings_config_dir_and_settings_tfvars_do_not_exist + ext_config_dir)

if __name__ == '__main__':
    unittest.main()