import unittest

from utils import workflow

class WorkflowTestSuite(unittest.TestCase):
    """Workflow test cases."""

    def test_workflow_is_ignored(self):

        workflow_is_ignored_path = "./test_data/workflow/config_is_ignored/workflow/config.yaml"
    
        if workflow.is_workflow_file_ignored(workflow_is_ignored_path):
            assert True
        else:
            assert False

    def test_workflow_is_not_ignored(self):

        workflow_is_not_ignored_path = "./test_data/workflow/config_is_not_ignored/workflow/config.yaml"

        if workflow.is_workflow_file_ignored(workflow_is_not_ignored_path):
            assert False
        else:
            assert True

    # def test_stage_is_auto_approve(self):
    #     stage_is_auto_approve = "./test_data/workflow/workflow/config_stage_is_auto_approve.yaml"

    #     if workflow.is_stage_auto_approve(stage_is_auto_approve):
    #         assert True
    #     else:
    #         assert False

    # def test_stage_is_not_auto_approve(self):
    #     stage_is_not_auto_approve = "./test_data/workflow//config_stage_is_not_auto_approve/config.yaml"

    #     if workflow.is_stage_auto_approve(stage_is_not_auto_approve):
    #         assert False
    #     else:
    #         assert True

    def test_stage_name_exists(self):
        stage_name_exists = "./test_data/workflow/config_stage_name_exists"

        if workflow.does_stage_name_exist(stage_name_exists, "stage"):
            assert True
        else:
            assert False

    # TODO
    def test_stage_name_does_not_exist(self):
        stage_name_does_not_exist = "./test_data/workflow/config_stage_name_does_not_exist"

        if workflow.does_stage_name_exist(stage_name_does_not_exist, "stage_does_not_exist"):
            assert False
        else:
            assert True

    def test_all_active_stages_from_workflow(self):
        cwd = "./test_data/workflow/active_stage_1/"
        ACTIVE_STAGES = [0]
        active_stages, err, err_message = workflow.get_active_stages_from_workflow(cwd)

        if ACTIVE_STAGES == active_stages:
            assert True
        else:
            assert False

    def test_get_active_stages_0_from_workflow_and_detect_error(self):
        cwd = "./test_data/workflow/active_stage_0/"

        active_stages, err, err_message = workflow.get_active_stages_and_stage_names_from_workflow(cwd)

        if err:
            assert True
        else:
            assert False

    def test_get_active_stages_1_from_workflow(self):
        cwd = "./test_data/workflow/active_stage_1/"
        ACTIVE_STAGES = [0]
        active_stages, err, err_message = workflow.get_active_stages_and_stage_names_from_workflow(cwd)
        
        if ACTIVE_STAGES == active_stages:
            assert True
        else:
            assert False

    def test_get_active_stages_2_from_workflow(self):
        cwd = "./test_data/workflow/active_stage_2/"
        ACTIVE_STAGES = [1]
        active_stages, err, err_message = workflow.get_active_stages_and_stage_names_from_workflow(cwd)

        if ACTIVE_STAGES == active_stages:
            assert True
        else:
            assert False

    # TODO
    def test_get_active_stages_names_from_workflow(self):
        cwd = "./test_data/workflow/active_stage_named_stage/"
        ACTIVE = [1]
        
        active, err, err_message = workflow.get_active_stages_and_stage_names_from_workflow(cwd)

        if ACTIVE == active:
            assert True
        else:
            assert False

    def test_get_active_stages_range_2to3_and_5_from_workflow(self):
        cwd = "./test_data/workflow/active_stages_range_2to3_and_5/"
        ACTIVE = [1,2,4]
        
        active, err, err_message = workflow.get_active_stages_and_stage_names_from_workflow(cwd)

        if ACTIVE == active:
            assert True
        else:
            assert False

    def test_get_active_stages_mix_range_2to3_and_5_and_named_stage_from_workflow(self):
        cwd = "./test_data/workflow/active_stages_range_2to3_and_5_and_named_stage/"
        ACTIVE = [1,2,4,7,9]
        
        active, err, err_message = workflow.get_active_stages_and_stage_names_from_workflow(cwd)

        if ACTIVE == active:
            assert True
        else:
            assert False


    # def test_get_stages_to_apply_from_active_stages(self):
    
    def test_does_workflow_file_exists(self):

        # Test if workflow is ignored when ignore: False
        # If does_workflow_file_exist() returns False, that means workflow does not exist
        # Expected workflow to exist as workflow is not ignored
        cwd_config_is_not_ignored = "./test_data/workflow/config_is_not_ignored"
        cwd_config_is_ignored = "./test_data/workflow/config_is_ignored"
        cwd_config_ignore_key_is_missing = "./test_data/workflow/config_ignore_key_is_missing"

        if workflow.does_workflow_file_exist(cwd_config_is_not_ignored) == False:
            assert False

        # Test if workflow is ignored when ignore: True
        # If does_workflow_file_exist() returns True, that means workflow exists
        # Expected workflow to not exist as workflow should be ignored

        elif workflow.does_workflow_file_exist(cwd_config_is_ignored) == True:
            assert False
        
        # Test if workflow is ignored when ignore key is not included
        # If does_workflow_file_exist() returns True, that means workflow exists
        # Expected workflow to exist as ignore key is False by default

        elif workflow.does_workflow_file_exist(cwd_config_ignore_key_is_missing) == False:
            assert False

        else:
            assert True

    def test_get_number_of_resources_from_workflow(self):
        path = "./test_data/workflow/workflow/config.yaml"

        number_of_workflow_resources = workflow.get_number_of_resources_from_workflow(path)

        if number_of_workflow_resources == 6:
            assert True
        else:
            assert False

    def test_get_number_of_resources_from_maintf(self):
        path = "./test_data/workflow/main.tf"

        number_of_maintf_resources = workflow.get_number_of_resources_from_maintf(path)

        if number_of_maintf_resources == 6:
            assert True
        else:
            assert False

    def test_get_list_of_resources_from_workflow(self):
        path = "./test_data/workflow/workflow/config.yaml"

        EXPECTED_LIST_OF_WORKFLOW_RESOURCES = [
            "module.mi-1",
            "module.mi-2",
            "resource.ri-1.extra",
            "resource.ri-2.extra",
            "resource.ri-1.try",
            "module.mi-24",
            ]

        list_of_workflow_resources = workflow.get_list_of_resources_from_workflow(path)

        list_of_workflow_resources.sort()
        EXPECTED_LIST_OF_WORKFLOW_RESOURCES.sort()

        if list_of_workflow_resources == EXPECTED_LIST_OF_WORKFLOW_RESOURCES:
            assert True
        else:
            assert False

    def test_get_list_of_resources_from_maintf(self):
        path = "./test_data/workflow/main.tf"

        EXPECTED_LIST_OF_MAINTF_RESOURCES = [
            "module.mi-1",
            "module.mi-2",
            "resource.ri-1.extra",
            "resource.ri-2.extra",
            "resource.ri-1.try",
            "module.mi-24",
            ]

        list_of_maintf_resources = workflow.get_list_of_resources_from_maintf(path)

        list_of_maintf_resources.sort()
        EXPECTED_LIST_OF_MAINTF_RESOURCES.sort()

        if list_of_maintf_resources == EXPECTED_LIST_OF_MAINTF_RESOURCES:
            assert True
        else:
            assert False

    def test_does_workflow_file_contain_duplicates(self):
        path = "./test_data/workflow/workflow/config.yaml"

        list_of_workflow_resources = workflow.get_list_of_resources_from_workflow(path)

        does_workflow_file_contain_duplicates = workflow.does_workflow_file_contain_duplicates(list_of_workflow_resources)

        if does_workflow_file_contain_duplicates == False:
            assert True
        else:
            assert False

    def test_does_workflow_objects_exist_in_maintf(self):

        number_of_checks = 0

        workflow_less_than_maintf_path = "./test_data/workflow/config_less_than_maintf/workflow/config.yaml"
        workflow_more_than_maintf_path = "./test_data/workflow/config_more_than_maintf/workflow/config.yaml"
        workflow_same_as_maintf_path = "./test_data/workflow/config_same_as_maintf/workflow/config.yaml"
        workflow_same_as_maintf_path_but_wrong_resource = "./test_data/workflow/config_same_as_maintf_but_wrong_resource/workflow/config.yaml"
        
        maintf_path = "./test_data/workflow/main.tf"
        list_of_maintf_resources = workflow.get_list_of_resources_from_maintf(maintf_path)

        # List of workflow resources is less than maintf, so does_workflow_objects_exist_in_maintf should be True
        list_of_workflow_resources_less_than_maintf = workflow.get_list_of_resources_from_workflow(workflow_less_than_maintf_path)
        does_workflow_objects_exist_in_maintf = workflow.does_workflow_objects_exist_in_maintf(list_of_workflow_resources_less_than_maintf, list_of_maintf_resources)

        if does_workflow_objects_exist_in_maintf == True:
            number_of_checks += 1

        # List of workflow resources is more than maintf, so does_workflow_objects_exist_in_maintf should be False
        list_of_workflow_resources_more_than_maintf = workflow.get_list_of_resources_from_workflow(workflow_more_than_maintf_path)
        does_workflow_objects_exist_in_maintf = workflow.does_workflow_objects_exist_in_maintf(list_of_workflow_resources_more_than_maintf, list_of_maintf_resources, disable_print=True)

        if does_workflow_objects_exist_in_maintf == False:
            number_of_checks += 1

        # List of workflow resources is same as maintf, so does_workflow_objects_exist_in_maintf should be True
        list_of_workflow_resources_same_as_maintf = workflow.get_list_of_resources_from_workflow(workflow_same_as_maintf_path)
        does_workflow_objects_exist_in_maintf = workflow.does_workflow_objects_exist_in_maintf(list_of_workflow_resources_same_as_maintf, list_of_maintf_resources)

        if does_workflow_objects_exist_in_maintf == True:
            number_of_checks += 1

        # List of workflow resources is same as maintf but with wrong resource names, so does_workflow_objects_exist_in_maintf should be False
        list_of_workflow_resources_same_as_maintf_but_wrong_resource = workflow.get_list_of_resources_from_workflow(workflow_same_as_maintf_path_but_wrong_resource)
        does_workflow_objects_exist_in_maintf = workflow.does_workflow_objects_exist_in_maintf(list_of_workflow_resources_same_as_maintf_but_wrong_resource, list_of_maintf_resources, disable_print=True)

        if does_workflow_objects_exist_in_maintf == False:
            number_of_checks += 1

        if number_of_checks == 4:
            assert True
        else:
            assert False
    
    def test_check_stages_errors_with_no_workflow_errors(self):

        cwd = "./test_data/workflow/stages_with_no_workflow_errors"

        stages, stages_errors = workflow.get_stages(cwd)

        if workflow.check_stages_errors(stages_errors):
            assert False
        else:
            assert True

    def test_get_targets_module(self):
        targets_module =  [{'module': ['mi-24']}]

        targets = workflow.get_targets(targets_module)

        if targets == ['module.mi-24']:
            assert True
        else: 
            assert False

    def test_get_targets_module(self):
        targets_module =  [{'resource': ['mi-1.name']}]
        
        targets = workflow.get_targets(targets_module)
        
        print("targets: %s" % targets)

        if targets == ['resource.mi-1["name"]']:
            assert True
        else: 
            assert False

    def test_check_stages_return_module(self):

        cwd = "./test_data/workflow/stages_with_no_workflow_errors"

        stages, stages_errors = workflow.get_stages(cwd)

        print("stages: %s" % stages)

        if workflow.check_stages_errors(stages_errors):
            assert False
        else:
            assert True
    
    def test_check_stages_return_resources(self):

        cwd = "./test_data/workflow/stages_with_no_workflow_errors_target_resource"

        stages, stages_errors = workflow.get_stages(cwd)

        print("stages: %s" % stages)

        if workflow.check_stages_errors(stages_errors):
            assert False
        else:
            assert True

    def test_check_stages_errors_with_workflow_errors(self):

        workflow_less_than_maintf_cwd = "./test_data/workflow/config_less_than_maintf"
        workflow_more_than_maintf_cwd = "./test_data/workflow/config_more_than_maintf"
        workflow_same_as_maintf_path = "./test_data/workflow/config_same_as_maintf"
        workflow_same_as_maintf_path_but_wrong_resource = "./test_data/workflow/config_same_as_maintf_but_wrong_resource/workflow/config.yaml"

        # List of workflow resources is less than maintf, so does_workflow_contain_error_and_warnings should be False
        if workflow.does_workflow_contain_error_and_warnings(workflow_less_than_maintf_cwd) != False:
            assert False

        # List of workflow resources is more than maintf, so does_workflow_contain_error_and_warnings should be True
        if workflow.does_workflow_contain_error_and_warnings(workflow_more_than_maintf_cwd) != True:
            assert False

        # List of workflow resources is same as maintf, so does_workflow_contain_error_and_warnings should be False
        if workflow.does_workflow_contain_error_and_warnings(workflow_same_as_maintf_path) != False:
            assert False

    #     cwd = "./test_data/workflow/stages_with_workflow_errors"

    #     stages, stages_errors = workflow.get_stages(cwd)

    #     if workflow.check_stages_errors(stages_errors):
    #         assert True
    #     else:
    #         assert False

    # def test_does_workflow_contain_error_and_warnings(self):

    # def test_get_targets(self):

    # def test_get_stage_and_targets(self):

    # def test_get_stages(self):
    # {
    #         "stage_name":stage_name,
    #         "stage_auto_approve":stage_auto_approve,
    #         "stage_targets":stage_targets,
    #         }


if __name__ == '__main__':
    unittest.main()