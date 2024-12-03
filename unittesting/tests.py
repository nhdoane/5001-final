"""
One convenient place to run all your tests from
"""
import unittest
import test_search, test_db, test_conversions

def main():
    # create the list of test modules
    # add any new test modules to this list following the same format
    test_list = [
        unittest.TestLoader().loadTestsFromModule(test_search),
        unittest.TestLoader().loadTestsFromModule(test_db),
        unittest.TestLoader().loadTestsFromModule(test_conversions)
    ]
    # instantiate a test suite
    test_suite = unittest.TestSuite()
    # add all the tests from the various modules into the test suite
    test_suite.addTests(test_list)
    # run the test suite with decent verbosity
    unittest.TextTestRunner(verbosity=2).run(test_suite)

if __name__ == '__main__':
    main()