DROP TABLE sample_orders;

CREATE TABLE sample_orders
(
    o_orderkey      INT            NOT NULL,
    o_custkey       BIGINT         NOT NULL,
    o_orderstatus   VARCHAR(50)    NOT NULL,
    o_totalprice    DECIMAL(15, 2) NOT NULL,
    o_orderdate     DATE           NOT NULL,
    o_orderpriority VARCHAR(50)    NOT NULL,
    o_clerk         VARCHAR(50)    NOT NULL,
    o_shippriority  INT            NOT NULL,
    o_comment       VARCHAR(400)   NOT NULL
);

TRUNCATE TABLE sample_orders;

BULK INSERT sample_orders
FROM 'C:\path\to\sample_orders.txt'
WITH (
    FIELDTERMINATOR = '|',
    ROWTERMINATOR = '\n',
	FIRSTROW = 2
);
