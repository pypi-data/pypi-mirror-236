import unittest


class TestCaseBase(unittest.TestCase):
    @classmethod
    def run_tests(cls) -> unittest.TestResult:
        """run all tests in class and return the result"""
        test = unittest.defaultTestLoader.loadTestsFromTestCase(cls)
        test_result = unittest.TextTestRunner().run(test)
        return test_result

    def setUp(self):
        """Initialize objects for testing"""
        raise NotImplementedError

    def tearDown(self):
        """Clean up the objects after running the test"""
        raise NotImplementedError
