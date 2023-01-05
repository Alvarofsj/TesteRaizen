# TesteRaizen

Raizen test for Data Engineers

## Intro

This application was made as test for Data Engineers from Raizen. It aims to read a XLS file, and perfome an ETL process to gather data and store on a database.

The application is made in Python3, and the dependencies can be seen on requirements.txt. For installing, use `pip install -r requirements.txt` from the root directory.

There's also a Dockerfile in case you want to enclose it on a Docker container. Just remember to switch your Docker daemon to `Windows Containers`. 
This is necessary because the application uses the library `PyWin32`, which is only available on Windows OS.

## Pipeline

The pipeline of the application is:

**- Download the XLS file from source:** The source is described on `config.py`, variable `link_download`. You can change it if the source changes. Also, the name of the
file is as the variable `namefiles['dwn_file']` in the same file, and can be changed too if the source file changes its name.

**- Open and read the XLS file with PyWin32:** With PyWin32, the application reads the XLS file and gather the data. The tables with data are identified by the string
text described on the dictionary `str_busca` inside `config.py`. It's the text in red on the table that describes the title of the table with data.
You can add as much as strings you want on this dictionary, as long as the text really exists on the XLS file. Also, the order of this dictionary and the dictionary 
`filtros` (which contains the filter names of the tables the application will gather the data) has to be the same, as in the first item of the dictionary `str_bus` 
matches the first item with the filters of the table identified by that string. If filters are not available on the identified table, the application will end.

**- Check Consistency of Data:** The application then checks for the consistency of the data gathered before, by comparing the sum of each filtered data with the total 
that was already on the XLS file. Also, the check is made by comparing the total per year too. If both of these checks are True, the applicaton will move to the
insertion on the database.

**- Insert Data on the Database:** The data then will be inserted on the database. Since there's always a different creation time on the data, the application just
inserts it without checking for duplicates on the database. That's actually better, since we'll have to append data on the DB every time the source updates its data.

**- Ending iterations:** After doing all the above for all the desired data, the application will end. Every step is logged on the `logs.txt` file, that can be found
on the root of the application. Also, the data gathered is exported to CSV files, that can found on the `tmp` folder, on the root of the application.

## Final Thoughts

The application stored data on a SQLite database, but can alse work on any other relational database like MySQL or PostGresSQL, by changing the variable `string_engine`
on the `config.py` file to fit the desired schema. Also, if more data would be gathered in the future, new schemas of tables needs to be declared on the `Banco.py` file
(inside the `database` folder), and some changes have to be made on the insertion function.
