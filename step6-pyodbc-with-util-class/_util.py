import datetime, decimal
from tableauhyperapi import *

def get_table_def(cursor):
    list_def = []
    cursor_desc = cursor.description
    for d in cursor_desc:
        colname, dtype = d[0], d[1]

        if dtype == str:
            s = SqlType.varchar(d[4])
        elif dtype == int:
            s = SqlType.int()
        elif dtype == datetime.date:
            s = SqlType.date()
        elif dtype == decimal.Decimal:
            s = SqlType.numeric(d[4], d[5])
        else:
            s = SqlType.varchar(1024)
        list_def.append(TableDefinition.Column(colname, s))

    return list_def