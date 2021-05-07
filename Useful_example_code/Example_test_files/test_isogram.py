import unittest  # the test file has to have the unittest module imported
import isogram  # import the file with the functions/classes you want to test


class TestIsogram(unittest.TestCase):

    '''
        @classmethod
        def setUpClass(cls):
            #this class runs once before the tests begin 
            #useful to have to build something needed in the tests methods

        @classmethod
        def tearDownClass(cls):
            #this class is run last after all the test are completed
            # is useful when taking down something built at the start of tests
            pass 
    '''
    # _______________________________________________________________________
    '''
    This code below runs a starndard test
    '''
    # def test_Isogram(self):
    #     result = isogram.is_Isogram('cliford')
    #     self.assertTrue(result)

    #     with self.assertRaises(ValueError):
    #         isogram.is_Isogram('cli345ff')
    # ________________________________________________________
    '''
        This code below runs the test  starting with a setUp function 
        that creates variables to be reused in functions below!
    '''

    def setUp(self):
        self.result = isogram.is_Isogram('cliford')
        # this set allows the code in here to run everytime
        # before each test is run!

    def tearDown(self):  # can have code that runs after every test
        # usually used to clean, or clear any entries or data made from running the test.
        pass

    def test_Isogram(self):

        self.assertTrue(self.result)
        with self.assertRaises(ValueError):
            isogram.is_Isogram('cli345ff')

    # ______________________________________________________


# this code below allows you to run this script with the run button and bypasses having to type the run command in the terminal
if __name__ == '__main__':
    unittest.main()
