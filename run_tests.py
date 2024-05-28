import unittest

def run_all_unittests(test_directory):
    # Create a test loader
    loader = unittest.TestLoader()

    # Discover all tests in the specified directory
    suite = loader.discover(test_directory)

    # Create a test runner
    runner = unittest.TextTestRunner()

    # Run the tests
    runner.run(suite)

if __name__ == "__main__":
    # Specify the directory containing the tests
    test_directory = 'test'

    # Run all unittests in the specified directory
    run_all_unittests(test_directory)
