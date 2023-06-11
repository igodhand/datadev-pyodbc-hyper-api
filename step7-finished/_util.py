import pyodbc
import datetime, decimal
from tableauhyperapi import *

server = 'dbserver'
database = 'tcph'
username = 'datadev'
password = 'tableau'

conn_str = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str)

def get_table_def(cursor):
    list_def = []
    cursor_desc = cursor.description

    for d in cursor_desc:
        colname, dtype = d[0], d[1]
        if dtype == str:
            if d[4] <= 4096:
                s = SqlType.varchar(d[4])
            else:
                s = SqlType.text()
        elif dtype == int:
            if d[4] >= 16:
                s = SqlType.big_int()
            elif d[4] < 6:
                s = SqlType.small_int()
            else:
                s = SqlType.int()
        elif dtype == bool:
            s = SqlType.bool()
        elif dtype == float:
            s = SqlType.double()
        elif dtype == datetime.date:
            s = SqlType.date()
        elif dtype == datetime.time:
            s = SqlType.time()
        elif dtype == datetime.datetime:
            s = SqlType.timestamp()
        elif dtype == decimal.Decimal:
            s = SqlType.numeric(d[4], d[5])
        else:
            s = SqlType.varchar(1024)
        list_def.append(TableDefinition.Column(colname, s))

    return list_def


def create_hyper(conn, sql_query, file_name, table_name):
    print(f"Creating {file_name} using {sql_query}")

    with HyperProcess(Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        print("Hyper Started")

        with Connection(hyper.endpoint, file_name, CreateMode.CREATE_AND_REPLACE) as connection:
            print("Connection Created")

            cursor = conn.cursor()
            cursor.execute(sql_query)

            list_def = get_table_def(cursor)

            connection.catalog.create_schema('Extract')
            table = TableDefinition(TableName('Extract', table_name), list_def)
            connection.catalog.create_table(table)

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
