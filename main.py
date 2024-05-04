#Context: Technical test backend python: extract specific information from a PDF file and present the data in a structured format (JSON, SQLITE3)
#Methods: main, get_data, parse_data, write_json, write_db, unit_tests

#library imports
import camelot

def get_data(file_name):
    table_names = {"Closing Information","Transaction Information","Loan Information"}

    #get list of tables returned from camelot read pdf method, for all pages
    tables = camelot.read_pdf(pdf_path, flavor='stream', pages="1-5")

    #output tables
    for table in tables:
        print("---------------------------------------------------")
        #the table obj needs to be converted to a data frame for wanted output
        print(table.df)
    return tables


if __name__ == "__main__":
   pdf_path = "Closing_Disclosure.pdf"
   data = get_data(pdf_path)