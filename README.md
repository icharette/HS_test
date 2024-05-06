# HS_test

## Libraries 
camelot version 0.11.0<br>
opencv-python-headless version 4.9.0.80<br>
json<br>
os<br>
unittest<br>
sqlite3 version 3.45.3<br>

## Programming Language
python version 3.11.8<br>

## Installation
To install this project, follow these steps:
1. Clone the repository<br>
2. Complete these installations steps:<br>
pip install camelot-py<br>
https://pypi.org/project/camelot-py/<br>
<br>
pip install opencv-python-headless<br>
https://pypi.org/project/opencv-python-headless/<br>
<br>
squlite3: <br>
https://www.sqlite.org/download.html<br>
Precompiled Binaries for Windows: sqlite-tools-win-x64-3450300.zip<br>
Add sqlite3 extracted folder name to environment variables PATH<br>
<br>
3. Make sure you have python 3.11.8 version, or any compatible version

## Configuration
resources: place the file "Closing_Disclosure.pdf" in the respository folder, at the level of main.py<br>

## Usage
1. Complete the Installation and Configuration sections<br>
2. To execute the unit tests in command line: python unittesting.py<br>
3. To execute the script in command line: python main.py<br>


## Future implementations:
    To parse the full PDF document with all the tables, here are the following updates I would add to this project: 
    1. Create parent class Table with defined methods format_sql(data, db_file_name) and format_json(data, json_file_name) and abstract method parse_table_data(tables, table_dict)
    2. Create a child class for each table to be extracted and override the method parse_table_data(tables, table_dict)
        The method parse_table_data(tables, table_dict) will be unique to each child class since each table has different formatting.
        Each method will still return a dictionnary of dictionnaries. Similar to the following, which will be used for the methods format_sql(data, db_file_name) and format_json(data, json_file_name)
        
    {
	"Loan Terms": {
		"Loan Amount": {
			"value": "******",
			"Loan Terms Can this amount increase after closing?": "NO/YES"
		},
		"Interest Rate": {
			"value": "***",
			"Loan Terms Can this amount increase after closing?": "NO/YES"
		},
		"Monthly Principal & Interest": {
			"value": "***",
			"Loan Terms Can this amount increase after closing?": "NO/YES"
		},
		"Estimated Total Monthly Payment": {
			"value": "***",
			"Does the loan have these features?": "NO/YES"
		},
		"Prepayment Penalty": {
			"value": "***",
			"Does the loan have these features?": "NO/YES"
		},
		"Balloon Payment": {
			"value": "***",
			"Does the loan have these features?": "NO/YES"
		}
	}
}

*The OOP approach is ideal at this step since it will help in keeping the program modular and reuse the methods for format_sql(data, db_file_name) and format_json(data, json_file_name) 