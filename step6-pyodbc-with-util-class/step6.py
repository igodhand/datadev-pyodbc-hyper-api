import pyodbc
import decimal, datetime
import _util as util

server = 'localhost'
database = 'tcph'
username = 'datadev'
password = 'tableau'

conn_str = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str)

file_path = 'D:\\TEMP\\'

util.create_hyper(conn, 'select * from sample_orders', file_path + "TCPH.hyper", "orders")
