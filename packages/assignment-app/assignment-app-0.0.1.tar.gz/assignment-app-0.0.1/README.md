[![CLI_Lab](https://github.com/nogibjj/oo46_Mini_Proj_W6/actions/workflows/cicd.yml/badge.svg)][def]

# SQL Lab - Week 6 mini project

## The current implementation of the Mini-project can be executed as follows:

1. All dependencies needed for execution can be found in the [requirement.txt](https://github.com/nogibjj/oo46_Mini_Proj_W6/blob/main/requirements.txt) file.

2. The main purpose of this application is to [connect](https://github.com/nogibjj/oo46_Mini_Proj_W6/blob/main/mylib/mydbconn.py) remotely to an Azure Sql Server database and perform some [complex sql query](https://github.com/nogibjj/oo46_Mini_Proj_W6/blob/main/mylib/query.py).

   - The complex SQL query uses the Northwind sample database and retrieves the top N = 10 customers with the highest total purchase amounts. You can adjust the value of N as needed.
   - In this query:

     1. The RankedCustomers common table expression (CTE) calculates the total purchase amount for each customer by joining the Customers, Orders, and Order Details tables.

     2. It then assigns a rank to each customer based on their total purchase amount using the ROW_NUMBER() window function.

     3. The main query then selects the top N customers with the highest total purchase amounts from the RankedCustomers CTE, where N is a parameter you can adjust.

     This query will give you a list of the top N customers with the highest total purchase amounts in the Northwind database, and it is applicable to databases with similar schema structure.

## Mini-project deliverables:

1. [Remote Connection Module](https://github.com/nogibjj/oo46_Mini_Proj_W6/blob/main/mylib/mydbconn.py) => This module securely connects to an Azure SQL Server database in the cloud and returns a connection object along with a "success" message string. It relies on environment variables (Server Name, Database, User Name, Password) for this connection.

2. [SQL Query Module](https://github.com/nogibjj/oo46_Mini_Proj_W6/blob/main/mylib/query.py) => The query module does the following:

   1. It relies on the mydbconn module to connect to the Northwind
      database.

   2. It then performs a complex SQL query that retrieves
      the top 10 customers with the highest total purchase amounts.

   3. Finally, it returns the results as a Pandas DataFrame.

3. [Main App Module](https://github.com/nogibjj/oo46_Mini_Proj_W6/blob/main/main.py) => This module can be thought of as the main entry point to the application.

   1. It calls the query function from the query module to get the data from the database.

   2. Then, it plots the data and saves the plot as a png file.

   3. Finally, it returns a string "Success" to indicate that the program has run successfully.

4. [Testing Module](https://github.com/nogibjj/oo46_Mini_Proj_W6/blob/main/test_main.py) => This module is used to test the functionality of the above modules. Its output is displayed [here](https://github.com/nogibjj/oo46_Mini_Proj_W6/blob/main/test.png)

### Entity Relationship Diagram of Northwind Database:

![ERD](erd.png)

### Application output:

![Output](top.png)

### Testing outcome:

![Test](test.png)

[def]: https://github.com/nogibjj/oo46_Mini_Proj_W6/actions/workflows/cicd.yml
