#!/usr/bin/env python
"""
Test runner script for the school management system.

This script runs all tests and provides a comprehensive report.

Usage:
    # Run all tests
    python run_tests.py

    # Run specific app tests
    python run_tests.py colleges
    python run_tests.py departments
    python run_tests.py courses
    python run_tests.py students
    python run_tests.py professors
    python run_tests.py subjects

    # Run with coverage
    python run_tests.py --coverage

    # Run specific test classes
    python run_tests.py colleges.tests.CollegeModelTest
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner


def setup_django():
    """Setup Django for testing"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
    django.setup()


def run_tests(test_labels=None, verbosity=1, interactive=True, coverage=False):
    """Run tests with optional coverage"""
    
    setup_django()
    
    if coverage:
        try:
            import coverage
            cov = coverage.Coverage()
            cov.start()
        except ImportError:
            print("Coverage.py not installed. Install with: pip install coverage")
            coverage = False
    
    # Get the Django test runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=verbosity, interactive=interactive)
    
    # If no test labels provided, run all tests
    if not test_labels:
        test_labels = [
            'colleges.tests',
            'departments.tests', 
            'courses.tests',
            'students.tests',
            'professors.tests',
            'subjects.tests',
            'tests.test_integration',
        ]
    
    # Run the tests
    failures = test_runner.run_tests(test_labels)
    
    if coverage:
        cov.stop()
        cov.save()
        
        # Print coverage report
        print("\n" + "="*50)
        print("COVERAGE REPORT")
        print("="*50)
        cov.report()
        
        # Generate HTML coverage report
        cov.html_report(directory='htmlcov')
        print(f"\nHTML coverage report generated in htmlcov/")
    
    return failures


def main():
    """Main function to handle command line arguments"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run tests for school management system')
    parser.add_argument('tests', nargs='*', help='Specific tests to run')
    parser.add_argument('-v', '--verbosity', type=int, default=2, 
                       help='Verbosity level (0-3)')
    parser.add_argument('--coverage', action='store_true', 
                       help='Run tests with coverage report')
    parser.add_argument('--no-interactive', action='store_true',
                       help='Run tests non-interactively')
    
    args = parser.parse_args()
    
    # Run tests
    failures = run_tests(
        test_labels=args.tests or None,
        verbosity=args.verbosity,
        interactive=not args.no_interactive,
        coverage=args.coverage
    )
    
    # Exit with appropriate code
    if failures:
        print(f"\n{failures} test(s) failed.")
        sys.exit(1)
    else:
        print(f"\nAll tests passed!")
        sys.exit(0)


if __name__ == '__main__':
    main()
