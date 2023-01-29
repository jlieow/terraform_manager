import unittest

from utils import common

class CommonTestSuite(unittest.TestCase):
    """Common test cases."""

    def test_get_rows_as_list(self):

        path = "./test_data/common/rows_as_list.csv"
        CHECK_ROWS_AS_LIST = [['1'], ['2'], ['3'], ['4']]
        
        rows_as_list = common.get_rows_as_list(path)

        if rows_as_list == CHECK_ROWS_AS_LIST:
            assert True
        else:
            assert False


if __name__ == '__main__':
    unittest.main()