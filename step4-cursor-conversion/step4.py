import datetime
import decimal
import pyodbc
from tableauhyperapi import *

server = 'dbserver'
database = 'tcph'
username = 'datadev'
password = 'tableau'
conn_str = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

sql_query = 'SELECT * FROM sample_orders'
cursor.execute(sql_query)
desc = cursor.description

for d in cursor.description:
    print(d)

print("=======================================")

list_def = []

for d in cursor.description:
    colname, dtype = d[0], d[1]
    if dtype == str:
        s = SqlType.varchar(d[4])
    elif dtype == int and d[4] > 10:
        s = SqlType.big_int()
    elif dtype == int:
        s = SqlType.int()
    elif dtype == datetime.date:
        s = SqlType.date()
    elif dtype == decimal.Decimal:
        s = SqlType.numeric(d[4], d[5])
    else:
        s = SqlType.varchar(1024)
    list_def.append(TableDefinition.Column(colname, s))

for t in list_def:
    print(t)




