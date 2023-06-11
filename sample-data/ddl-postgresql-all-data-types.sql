DROP TABLE all_data_types;

CREATE TABLE all_data_types
(
    col_bigint   bigint NULL,
    col_int      INT NULL,
    col_smallint SMALLINT NULL,
    col_bit      BIT NULL,
    col_decimal  DECIMAL(10, 2) NULL,
    col_numeric  NUMERIC(10, 2) NULL,
    col_money    money NULL,
    col_float    REAL NULL,
    col_real     REAL NULL,
    col_date     DATE NULL,
    col_time     TIME(0) NULL,
    col_datetime TIMESTAMP NULL,
    col_char     CHAR(10) NULL,
    col_varchar  VARCHAR(50) NULL,
    col_text     text NULL,
    col_nchar    NCHAR(10) NULL
);
