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
            TableDefinition.Column('o_orderkey', SqlType.int()),
            TableDefinition.Column('o_custkey', SqlType.big_int()),
            TableDefinition.Column('o_orderstatus', SqlType.varchar(50)),
            TableDefinition.Column('o_totalprice', SqlType.numeric(15, 2)),
            TableDefinition.Column('o_orderdate', SqlType.date()),
            TableDefinition.Column('o_orderpriority', SqlType.varchar(50)),
            TableDefinition.Column('o_clerk', SqlType.varchar(50)),
            TableDefinition.Column('o_shippriority', SqlType.int()),
            TableDefinition.Column('o_comment', SqlType.varchar(400)),
        ])

        connection.catalog.create_table(table)

        cursor = conn.cursor()
        sql_query = 'SELECT * FROM sample_orders'
        cursor.execute(sql_query)

        i = 0
        fetch_size = 10000
        rows = cursor.fetchmany(fetch_size)

        with Inserter(connection, table) as inserter:
            while rows:
                i += len(rows)
                print(f"Reading {str((i))} "rows.")
                if not rows:
                    break
                else:
                    inserter.add_rows(rows=rows)
                rows = cursor.fetchmany(fetch_size)
            inserter.execute()


        print("Connection Closed")
    print("Hyper Stopped")
print("Done")
