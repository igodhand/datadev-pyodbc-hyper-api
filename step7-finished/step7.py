import _util as util

file_path = 'D:\\TEMP\\'

util.create_hyper(util.conn, 'select * from nation', file_path + "nation.hyper", "nation")
util.create_hyper(util.conn, 'select * from region', file_path + "region.hyper", "region")
util.create_hyper(util.conn, 'select * from supplier', file_path + "supplier.hyper", "supplier")
util.create_hyper(util.conn, 'select top 100000 * from orders', file_path + "orders.hyper", "orders")
util.create_hyper(util.conn, 'select top 100000 * from customer', file_path + "customer.hyper", "customer")
util.create_hyper(util.conn, 'select top 100000 * from part', file_path + "part.hyper", "part")
util.create_hyper(util.conn, 'select top 100000 * from partsupp', file_path + "partsupp.hyper", "partsupp")
util.create_hyper(util.conn, 'select top 100000 * from lineitem', file_path + "lineitem.hyper", "lineitem")
