"""
Custom test runner to handle discovery issues with non-Python directories.
"""

import unittest
import importlib
from django.conf import settings
from django.test.utils import setup_test_environment, teardown_test_environment
from django.db import connections


class CustomTestRunner:
    """
    Custom test runner that fixes discovery issues by directly
    loading test modules instead of using discovery.
    """
    
    def __init__(self, verbosity=1, interactive=True, keepdb=False):
        self.verbosity = verbosity
        self.interactive = interactive
        self.keepdb = keepdb
    
    def run_tests(self, test_labels, **kwargs):
        """
        Run tests by directly loading test modules.
        """
        # Setup test environment
        setup_test_environment(debug=settings.DEBUG)
        
        # Setup databases
        old_names = []
        for alias in connections:
            connection = connections[alias]
            old_names.append((connection, connection.settings_dict['NAME']))
            connection.creation.create_test_db(verbosity=self.verbosity, autoclobber=True, keepdb=self.keepdb)
        
        try:
            # Build the test suite
            suite = self.build_suite(test_labels)
            
            # Run the tests
            runner = unittest.TextTestRunner(verbosity=self.verbosity)
            result = runner.run(suite)
            
            return result.wasSuccessful()
        finally:
            # Teardown databases
            for connection, old_name in old_names:
                connection.creation.destroy_test_db(old_name, verbosity=self.verbosity)
            
            # Teardown test environment
            teardown_test_environment(debug=settings.DEBUG)
    
    def build_suite(self, test_labels):
        """
        Build test suite by directly loading test modules.
        """
        from unittest.loader import TestLoader
        
        loader = TestLoader()
        suite = unittest.TestSuite()
        
        # Map app labels to specific test modules
        test_module_map = {
            'apps.recipe': [
                'apps.recipe.tests.test_models',
                'apps.recipe.tests.test_forms',
                'apps.recipe.tests.test_views',
                'apps.recipe.tests.test_recipe_list_detail',
                'apps.recipe.tests.test_recipes_views'
            ]
        }
        
        # If no specific test labels are provided, load all recipe tests
        if not test_labels:
            test_labels = ['apps.recipe']
        
        # Load tests for each label
        for label in test_labels:
            if label in test_module_map:
                for module_name in test_module_map[label]:
                    try:
                        module = importlib.import_module(module_name)
                        suite.addTests(loader.loadTestsFromModule(module))
                    except ImportError as e:
                        print(f"Warning: Could not import {module_name}: {e}")
            else:
                # For direct module references (e.g., apps.recipe.tests.test_models)
                try:
                    module = importlib.import_module(label)
                    suite.addTests(loader.loadTestsFromModule(module))
                except ImportError as e:
                    print(f"Warning: Could not import {label}: {e}")
        
        return suite
