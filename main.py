#Context: Technical test backend python: extract specific information from a PDF file and present the data in a structured format (JSON, SQLITE3)
#Methods: main, get_data, parse_data, write_json, write_db, unit_tests

#library imports
import camelot

def get_data(file_name):
    table_names = {"Closing Information","Transaction Information","Loan Information"}

    #get list of tables returned from camelot read pdf method, for all pages
    tables = camelot.read_pdf(pdf_path, flavor='stream', pages="1")

    #output tables
    #for table in tables:
        #print("---------------------------------------------------")
        #the table obj needs to be converted to a data frame for wanted output
        #print(table.df)
    return tables

def get_coordinates(table_name, tables):
    if tables:
        #the table name we are looking for is in the first table
        table = tables [0]
        df = table.df
        #flag to keep track if we found the location or not
        value_found = False

        # Iterate over the DataFrame to find the table name and its position
        for i, row in enumerate(df.values):
            for j, cell in enumerate(row):
                if cell == table_name:
                    #print(f"Value '{table_name}' found at row {i} and column {j}.")
                    value_found = True
                    return i,j
                    break
            if value_found:
                break
        
        #IF we haven't found the table name
        if not value_found:
            print(f"Value '{table_name}' not found in the table.")
            return None, None

def parse_table_data(tableKey, tableValue, table_names, row_start, df,i):
   #iterate through the table data of the rows starting beneath the table titles, in each column (i) accordingly (which corresponds to each table of: {"Closing Information":{}, "Transaction Information": {}, "Loan Information":{}})
    for index, value in df.iloc[row_start:, i].items():
        # print("index: ", index)
        #print("value: ", value)

        #checking if value to avoid keeping track of empty spaces
        if value:
            #add to the table_names dictionnary with the table values assigned to each table element in table_names
            #check if line return in value and if so, split the strings to seperate key(column) and value in each table
            if '\n' in value:
                key, value = value.split('\n')
                table_names[tableKey][key] = value
    
    
    #print(table_names)

if __name__ == "__main__":
   pdf_path = "Closing_Disclosure.pdf"
   tables = get_data(pdf_path)
   #table_names = {"Closing Information","Transaction Information","Loan Information"}
   table_dict  = {"Closing Information":{}, "Transaction Information": {}, "Loan Information":{}}

   #find location of tables: "Closing Information","Transaction Information","Loan Information"
   if tables:
        #using the value of i to index through the table title index (seen as a column in the data frame output from the camelot table extraction)
        i = 0
        for tableKey, tableValue in table_dict.items():
           row, column = get_coordinates(tableKey, tables)
           #print("row: ", row)
           #print("column: ", column)

           #get data for each table:
           #iterate through the dictionary of {"Closing Information":{}, "Transaction Information": {}, "Loan Information":{}}
           parse_table_data(tableKey, tableValue, table_dict, row + 1, tables[0].df,i)
           i = i + 1
        print(table_dict)
   else:
       print("no tables found")
       #need to add unit test for this

    