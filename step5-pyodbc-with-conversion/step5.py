import pyodbc
import decimal, datetime
from tableauhyperapi import *

server = 'localhost'
database = 'tcph'
username = 'datadev'
password = 'tableau'

conn_str = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str)

file_path = 'D:\\TEMP\\'

with HyperProcess(Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
    print("Hyper Started")

    with Connection(hyper.endpoint, file_path + 'TCPH.hyper', CreateMode.CREATE_AND_REPLACE) as connection:
        print("Connection Created")

        cursor = conn.cursor()
        sql_query = 'SELECT * FROM sample_orders'
        cursor.execute(sql_query)

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
