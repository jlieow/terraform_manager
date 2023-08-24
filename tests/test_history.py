import unittest
import csv
import os

from utils import history

class HistoryTestSuite(unittest.TestCase):
    """History test cases."""

    cwd = "unit_testing"
    stage_name = "unit_testing_stage"
    unit_testing = True 
    unit_testing_path = os.path.join(".", "test_data", "history", "terraform_history.csv")

    def erase_history(self):
        unit_testing_path = HistoryTestSuite.unit_testing_path

        with open(unit_testing_path, 'w', newline='') as f:  
            # using csv.writer method from CSV package
            write = csv.writer(f)
            
            write.writerows("")
            f.close()

    def test_add_history(self):
        HistoryTestSuite.erase_history(self)

        # Adds new csv to ./test_data/history location
        cwd = HistoryTestSuite.cwd
        stage_name = HistoryTestSuite.stage_name
        unit_testing = HistoryTestSuite.unit_testing 
        unit_testing_path = HistoryTestSuite.unit_testing_path

        EXPECTED_RESULT = [[cwd, stage_name]]

        history.add_history(cwd, stage_name, unit_testing, unit_testing_path)

        read_current_history = []

        # Read the CSV contents to a list     
        with open(unit_testing_path, 'rt') as f:  
            for row in csv.reader(f):
                read_current_history.append(row)

        # history.delete_latest_row_from_history(cwd, stage_name, unit_testing, unit_testing_path)

        # print("%s equals %s ? Result: %s" %(read_current_history, EXPECTED_RESULT, read_current_history == EXPECTED_RESULT))

        if read_current_history == EXPECTED_RESULT:
            assert True
        else:
            assert False
        
    
    def test_delete_latest_row_from_history(self):
        HistoryTestSuite.erase_history(self)

        cwd = HistoryTestSuite.cwd
        stage_name = HistoryTestSuite.stage_name
        unit_testing = HistoryTestSuite.unit_testing 
        unit_testing_path = HistoryTestSuite.unit_testing_path

        # Add history
        history.add_history(cwd, stage_name, unit_testing, unit_testing_path)
    
        read_current_history = []

        # Read the CSV contents to a list     
        with open(unit_testing_path, 'rt') as f:  
            for row in csv.reader(f):
                read_current_history.append(row)
        
        # Check that history is added
        if len(read_current_history) != 1:
            assert False

        # Delete previously added history
        history.delete_latest_row_from_history(cwd, stage_name, unit_testing, unit_testing_path)

        read_current_history = []

        # Read the CSV contents to a list     
        with open(unit_testing_path, 'rt') as f:  
            for row in csv.reader(f):
                read_current_history.append(row)
        
        # print("The current read history length is %d" % len(read_current_history))

        # Check that history was removed
        if len(read_current_history) == 0:
            assert True
        else:
            assert False

if __name__ == '__main__':
    unittest.main()