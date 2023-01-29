import unittest

from utils import chaos_test

class UnitTestTestSuite(unittest.TestCase):
    """Common test cases."""

    def test_is_chaos_test_file_ignored(self):

        chaos_test_is_ignored_path = "./test_data/chaos_test/config_unit_test_is_ignored/chaos_test/config.yaml"
        
        if chaos_test.is_chaos_test_file_ignored(chaos_test_is_ignored_path):
            assert True
        else:
            assert False

    def test_is_chaos_test_file_not_ignored(self):

        chaos_test_is_not_ignored_path = "./test_data/chaos_test/config_unit_test_is_not_ignored/chaos_test/config.yaml"
        
        if chaos_test.is_chaos_test_file_ignored(chaos_test_is_not_ignored_path):
            assert False
        else:
            assert True
    
    def test_get_chaos_test_directories(self):
        
        # example_chaos_test_directories contains 3 directories
        # 2 contain directories with chaos_test config.yaml

        root_directory = "./test_data/chaos_test/example_chaos_test_directories"

        EXPECTED_CHAOS_TEST_DIR = [
            "./test_data/chaos_test/example_chaos_test_directories/example_terraform_directory_with_chaos_test",
            "./test_data/chaos_test/example_chaos_test_directories/example_second_terraform_directory_with_chaos_test"
            ]

        list_chaos_test_dir = chaos_test.locate_chaos_test_directories(root_directory)

        list_chaos_test_dir.sort()
        EXPECTED_CHAOS_TEST_DIR.sort()

        if list_chaos_test_dir == EXPECTED_CHAOS_TEST_DIR:
            assert True
        else:
            assert False

    def test_get_chaos_test_stages(self):

        chaos_test_path = "./test_data/chaos_test/config.yaml"
        
        chaos_test_stages, _ = chaos_test.get_chaos_test_stages(chaos_test_path)
        if len(chaos_test_stages) == 2:
            assert True
        else:
            assert False

    def test_stage_destroy_is_disabled(self):
        
        # Stage 1, destroy_disabled: True
        # Stage 2, destroy_disabled: False
        # Stage 3

        chaos_test_stage_destroy_is_disabled_path = "./test_data/chaos_test/config_test_keys/chaos_test/config.yaml"

        chaos_test_stages, _ = chaos_test.get_chaos_test_stages(chaos_test_stage_destroy_is_disabled_path)
        
        print("chaos_test_stages")
        print(chaos_test_stages)
        if chaos_test_stages[0]["destroy_disabled"] != True:
            assert False
        elif chaos_test_stages[1]["destroy_disabled"] != False:
            assert False
        elif chaos_test_stages[2]["destroy_disabled"] != False:
            assert False
        else:
            assert True

    def test_stage_delay_before_execution(self):
        
        # Stage 1, delay_before_execution: 15
        # Stage 2, delay_before_execution: 0
        # Stage 3

        chaos_test_stage_delay_before_execution_path = "./test_data/chaos_test/config_test_keys/chaos_test/config.yaml"

        chaos_test_stages, _ = chaos_test.get_chaos_test_stages(chaos_test_stage_delay_before_execution_path)

        if chaos_test_stages[0]["delay_before_execution"] != 15:
            assert False
        elif chaos_test_stages[1]["delay_before_execution"] != 0:
            assert False
        elif chaos_test_stages[2]["delay_before_execution"] != 0:
            assert False
        else:
            assert True

    def test_stage_delay_after_execution(self):
        
        # Stage 1, delay_before_execution: 23
        # Stage 2, delay_before_execution: 0
        # Stage 3

        chaos_test_stage_delay_after_execution_path = "./test_data/chaos_test/config_test_keys/chaos_test/config.yaml"

        chaos_test_stages, _ = chaos_test.get_chaos_test_stages(chaos_test_stage_delay_after_execution_path)

        if chaos_test_stages[0]["delay_after_execution"] != 23:
            assert False
        elif chaos_test_stages[1]["delay_after_execution"] != 0:
            assert False
        elif chaos_test_stages[2]["delay_after_execution"] != 0:
            assert False
        else:
            assert True
    
    def test_stage_repeat(self):
        
        # Stage 1, delay_before_execution: 100
        # Stage 2, delay_before_execution: 0
        # Stage 3

        chaos_test_stage_delay_after_execution_path = "./test_data/chaos_test/config_test_keys/chaos_test/config.yaml"

        chaos_test_stages, _ = chaos_test.get_chaos_test_stages(chaos_test_stage_delay_after_execution_path)

        if chaos_test_stages[0]["repeat"] != 100:
            assert False
        elif chaos_test_stages[1]["repeat"] != 0:
            assert False
        elif chaos_test_stages[2]["repeat"] != 1:
            assert False
        else:
            assert True

    def test_stage_wrong_value_type(self):
        
        # Stage 1, delay_before_execution: 100
        # Stage 2, delay_before_execution: 0
        # Stage 3

        chaos_test_stage_wrong_value_type_path = "./test_data/chaos_test/config_test_keys_wrong_value_type/chaos_test/config.yaml"

        chaos_test_stages, chaos_test_stages_errors = chaos_test.get_chaos_test_stages(chaos_test_stage_wrong_value_type_path)

        for index in range(len(chaos_test_stages)):

            chaos_test_stage_errors = chaos_test_stages_errors[index]

            if chaos_test_stage_errors["error"] != True:
                assert False
            elif len(chaos_test_stage_errors["delay_before_execution_error_message"]) == 0:
                assert False
            elif len(chaos_test_stage_errors["delay_after_execution_error_message"]) == 0:
                assert False
            elif len(chaos_test_stage_errors["repeat_error_message"]) == 0:
                assert False
            else:
                assert True


if __name__ == '__main__':
    unittest.main()