import pyodbc
from tableauhyperapi import *
import _util as util

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

        cursor = conn.cursor()
        sql_query = 'SELECT * FROM sample_orders'
        cursor.execute(sql_query)

        list_def = util.get_table_def(cursor)

        connection.catalog.create_schema('Extract')
        table = TableDefinition(TableName('Extract', 'orders'), list_def)
        connection.catalog.create_table(table)

        i = 0
        fetch_size = 10000
        rows = cursor.fetchmany(fetch_size)

        with Inserter(connection, table) as inserter:
            while rows:
                i += len(rows)
                print(str((i)))
                if not rows:
                    break
                else:
                    inserter.add_rows(rows=rows)
                rows = cursor.fetchmany(fetch_size)
            inserter.execute()

        print("Connection Closed")
    print("Hyper Stopped")
print("Done")
