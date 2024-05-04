#Context: Technical test backend python: extract specific information from a PDF file and present the data in a structured format (JSON, SQLITE3)
#Methods: main, get_data, parse_data, write_json, write_db, unit_tests

#library imports
import camelot
import json
import sqlite3


def get_data(file_name):
    table_names = {"Closing Information","Transaction Information","Loan Information"}
    try:
    #get list of tables returned from camelot read pdf method, for all pages
        tables = camelot.read_pdf(pdf_path, flavor='stream', pages="1")
    except FileNotFoundError:
        print("No file named : ", file_name)
    except Exception as e:
        print("Error : ", e)

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

def parse_table_data(tables, table_dict):
    #the table where the information for {"Closing Information","Transaction Information","Loan Information"} is in the first table, according to the camelot extract
    table = tables[0]
    #converting to data frame to iterating through the information
    df = table.df
    #using the value of i to index through the table title index (seen as a column in the data frame output from the camelot table extraction)
    i = 0

    #iterate through the dictionary of {"Closing Information":{}, "Transaction Information": {}, "Loan Information":{}}
    for tableKey, tableValue in table_dict.items():
        #find location of tables: "Closing Information","Transaction Information","Loan Information"
        row, column = get_coordinates(tableKey, tables)
        if(row == None and column == None):
            print("Table ", tableKey, " does not exist.")
        else:
            row_start = row + 1
            #print("row: ", row)
            #print("column: ", column)

            #get data for each table:
            #iterate through the table data of the rows starting beneath the table titles, in each column (i) accordingly (which corresponds to each table of: {"Closing Information":{}, "Transaction Information": {}, "Loan Information":{}})
            for index, value in df.iloc[row_start:, i].items():
                # print("index: ", index)
                #print("value: ", value)

                #checking if value to avoid keeping track of empty spaces
                if value:
                    if "Property" in value:
                            #add extra line
                        value += df.iloc[index + 1,i]
                    elif "Borrower" in value:
                        #add 2 extra lines
                        value += " " + df.iloc[index + 1,i] + df.iloc[index + 2,i]            
                    if '\n' in value:
                        key, value = value.split('\n')
                        if "Loan Type" in key:
                            #stripping the 'X' selection
                            value = value[2:]
                        if "Loan ID #" in key:
                            #stripping the '#', this causes a problem with the SQL queries
                            key = key[:-2]
                        #populating the dictionary for each table
                        table_dict[tableKey][key] = value
            i = i + 1
    return table_dict

def format_json(data_dict):
    #convert to json
    json_obj = json.dumps(data_dict, indent=4)
    json_file = "Closing_Disclosure.json"
    with open(json_file, "w") as json_file:
        json.dump(data_dict, json_file, indent=4)

    print(json_obj)

def format_sql(data):
    try:
        #connect to db, which creates the db
        conn = sqlite3.connect('Closing_Disclosure.db')
        cursor = conn.cursor()

        #iterate through dictionary of extracted tables and create tables
        for key, item in data.items():
            if data[key]:
                #set columns names accordings to the keys in each nested dictionary
                column_names = list(item.keys())
                #replace spaces with underscores, otherwise this causes complication in the queries
                column_names = list(map(lambda x: x.replace(" ", "_"), column_names))
                #set values accordings to the values mapped to the keys in each nested dictionary
                values = tuple(item.values())

                #table names
                #replace spaces with underscores, otherwise this causes complication in the queries
                key = key.replace(" ", "_")
                print("key: ", key)
                #create table, if it does not already exist
                #key: table name
                create_table_sql = f'CREATE TABLE IF NOT EXISTS {key} ({", ".join(f"{name} TEXT" for name in column_names)})'
                print(create_table_sql)
                cursor.execute(create_table_sql)

                #populate tables with camelot table PDF extract
                insert_sql = f'INSERT INTO {key} ({", ".join(column_names)}) VALUES ({", ".join("?" for _ in column_names)})'
                cursor.execute(insert_sql, values)
            


        #Make sure to commit changes
        conn.commit()

    except sqlite3.Error as e:
        print("Error with SQLite: ", e)
    except Exception as e:
        print("Error: ", e)
    finally:
        #and close connection
        conn.close()

if __name__ == "__main__":
   pdf_path = "Closing_Disclosure.pdf"
   #extract data
   tables = get_data(pdf_path)

   #base for dictionary where to place extracted information
   table_dict  = {"Closing Infomation":{}, "Transaction Information": {}, "Loan Information":{}}

   #if camelot extracted tables
   if tables:
    #parse data
    table_dict = parse_table_data(tables, table_dict)
    #format data
    format_json(table_dict)
    format_sql(table_dict)
   else:
       print("No tables found")
       #need unit test here
   

    