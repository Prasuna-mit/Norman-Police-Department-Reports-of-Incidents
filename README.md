# Norman Police Department Reports of Incidents

Norman police department frequently updates the summary of incidents, arrests and daily case reports. The goal of this project is to extract a pdf document from the [website](http://normanpd.normanok.gov/content/daily-activity), perform analytics on the text data to retrieve the nature and the frequency of incidents from the resultant database. The implementation is done using python on google cloud platform.

## Getting Started

The information below walks you through the project.

### Prerequisites

Clone your git reposity to your local machine using ```git clone <url>``` . This project has been done in python 3.8.1 version. So, please make sure to install it using ```pyenv```. Also, create the local environment using ```pipenv``` which will auto generate pipfile and pipfile.lock. Import libraries and packages like SQLite3, pandas, pypdf2, etc.

## Project Descriptions

For this project I have created five below methods to perform particular task.

### fetchincidents(url)
This method takes an URL as an input, opens the url using using urllib.request to read it into a file in the form of bytes. This method returns the extracted data. 

### extractincidents(data)
This method is used to extract the actual data using PyPDF2.To do so, initially, a temporary file needs to be created to store the input data. This data again passed to PdfFileReader builtin function in the PyPDF2 library. This library is capable of splitting, merging together, cropping, and transforming the pages of PDF files. 

The data now is in string format seperated by newline. Replace the delimiter "\n" with comma using split function. Continue doing this process for all of the available pages using for loop. Perform some text mining on the data as it is having some issues with header inclusion which makes the text unstructured. I have removed the heading that usually is appended at the ending of the first page. The finaly structured dataframe will be returned to the function call.

### createdb()
Create a database using SQLite with the number of columns to store the dataframe. But before that, we need to create a database connection. 

**Database Schema:**

    CREATE TABLE incidents (
        incident_time TEXT,
        incident_number TEXT,
        incident_location TEXT,
        nature TEXT,
        incident_ori TEXT
    );

### populatedb(sqlite3_conn, incidents)
This method takes two parameters such as database connection link and the table and populate the database. "to_sql" used to write the dataframe into the database. This method is will not return any output. 

### status()
This method is the final method that takes database connction as an input parameter, executes the query that retrieves only nature and the count of incidents. After that, I have concatenated the columns using pipeline "|" delimiter.

**Output:**

0     Abdominal Pains/Problems|2
1               Aircraft Crash|2
2                       Alarm|10
3           Alarm Holdup/Panic|2
4               Animal Vicious|2
                 ...            
63        Unconscious/Fainting|8
64    Unknown Problem/Man Down|2

I have called all these methods in the main function with the respective input parameters.

## Test

To check the correctness of the implementation, I have generatied testcases for each methods.

### Testcase-1 for Fetching
I have written a condition to check whether the type of fetched file is "bytes" or not.

### Testcase-2 for extracting
This testcase checks the number of columns and the value at the specific field of the created dtaframe.

### Testcase-3 for connection
It checks if the database is connected at all or not.

### Testcase-4 for populating
Since this method populates the database with the values in dataframe, I have created the testcase to check if the number of rows have been stored properly or not.

### Testcase-5 for checking the status
This checks if output of the executed query is having the specific values or not.


### Execute the files in terminal

To run main.py file

```pipenv run python project0/main.py --incidents <url>```

To run test cases:

```pipenv run python setup.py test```

## Authors

* **Prasuna Mitikiri** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


