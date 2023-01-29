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

if __name__ == '__main__':
    unittest.main()