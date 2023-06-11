import pyodbc
from tableauhyperapi import *

server = 'dbserver'
database = 'tcph'
username = 'datadev'
password = 'tableau'

conn_str = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str)

file_path = 'D:\\HYPER\\'

with HyperProcess(Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
    print("Hyper Started")

    with Connection(hyper.endpoint, file_path + 'TCPH.hyper', CreateMode.CREATE_AND_REPLACE) as connection:
        print("Connection Created")

        connection.catalog.create_schema('Extract')

        table = TableDefinition(TableName('Extract', 'orders'), [

        ])

        connection.catalog.create_table(table)

        cursor = conn.cursor()
        sql_query = 'SELECT * FROM sample_orders'
        cursor.execute(sql_query)

        rows = cursor.fetchall()

        with Inserter(connection, table) as inserter:
            inserter.add_rows(rows=rows)
            inserter.execute()

        print("Connection Closed")
    print("Hyper Stopped")
print("Done")
