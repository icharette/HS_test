"""
Technical test backend python: unit testing for main.py

Setup:
    Please see README.md

Usage:
    python unittesting.py
"""

import unittest
import os
from main import *
from camelot.core import TableList


class TestPDFExtract(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        """
        Initializes the TestPDFExtract instance.

        Args:
            *args: Positional arguments for the superclass constructor.
            **kwargs: Keyword arguments for the superclass constructor.
        
        This init function calls the get_data() function from main.py, since several test methods in this class use this result.
        """
        #calling the super here to make sure when the test framework instantiates this class, everything runs smoothly, since we are overriding the __init__ method
        super().__init__(*args, **kwargs)
        self.table_extraction = get_data("Closing_Disclosure.pdf")
        self.table_dict  = {"Closing Information":{}, "Transaction Information": {}, "Loan Information":{}}

    def test_table_extraction_exists(self):
        """
        Test whether get_data returns a list of tables bigger than 0.

        Methodology:
        - Verify that the get_data() function returns a list of tables bigger than 0.

        Expected Outcome:
        - The function should return a list of tables bigger than 0.
        """
        #testing that tables exist and were extracted from the PDF
        self.assertTrue(len(self.table_extraction)>0)
        print("Test table extraction exists: PASSED")

    def test_table_extraction_data_type(self):
        """
        Test whether get_data returns a list of type TableList.

        Methodology:
        - Verify that the get_data() function returns a list of type TableList.

        Expected Outcome:
        - The function should return a list of type TableList.
        """
        #testing that tables were extracted with correct data type from the PDF
        self.assertIsInstance(self.table_extraction,TableList)
        print("Test table extraction data type: PASSED")

    def test_data_parsing(self):
        """
        Test whether get_data returns a dictionary of dictionaries.

        Methodology:
        - Verify that the parse_table_data() function returns a dictionary of dictionaries.

        Expected Outcome:
        - The function should return a dictionary of dictionaries.
        """
        #parsing the data extracted from the pdf and populating the self.table_dict
        test_data = parse_table_data(self.table_extraction, self.table_dict)
        #is test_data a dictionary?
        self.assertIsInstance(test_data, dict, "Variable is not of type Dictionary.")
         #is each value in the variable a dictionary?
        for key, value in test_data.items():
            self.assertIsInstance(value, dict, f"Value for key '{key}' is not a Dictionary")
        print("Test data parsing: PASSED")


class TestJSON(unittest.TestCase):
    def test_json_file_exists(self):
        """
        Test whether format_json() creates a json file.

        Methodology:
        - Verify that a json file exists with the correct file name.

        Expected Outcome:
        - The function should create a json file in the current directory.
        """
        test_file_name = "test_json.json"
        table_dict  = {"Closing Information":{"test":"test"}, "Transaction Information": {"test":"test"}, "Loan Information":{"test":"test"}}
        json_data = format_json(table_dict, test_file_name)
        #Does the file exist?
        self.assertTrue(os.path.exists(test_file_name), "JSON file was not created.")
        #test cleanup
        os.remove(test_file_name)
        print("Test JSON file exists: PASSED")

if __name__ == '__main__':
    unittest.main()