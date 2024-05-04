import camelot
import unittest

class TestPDFExtract(unittest.TestCase):

    def test_table_extraction(self):
        pdf_file = "Closing_Disclosure.pdf"
        #getting tables from pdf using camelot
        tables = camelot.read_pdf(pdf_file)
        #testing that tables were extracted from the PDF
        self.assertTrue(tables, "Failure to extract tables from PDF")

