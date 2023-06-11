import pyodbc

server = 'localhost'
database = 'tcph'
username = 'datadev'
password = 'tableau'

conn_str = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

sql_query = 'SELECT * FROM sample_orders'
cursor.execute(sql_query)
desc = cursor.description
for d in desc:
    print(d)

