#!/usr/bin/env python
"""
Simple test runner script for SpeedRead application.
Run this script to execute all unit tests.
"""

import sys
import unittest

def run_tests():
    """Discover and run all tests in the tests directory."""
    # Discover all tests
    loader = unittest.TestLoader()
    start_dir = '../tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code based on results
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests())
