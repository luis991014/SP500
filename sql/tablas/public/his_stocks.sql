CREATE TABLE stocks.public.his_stocks
(
    id_date INT
    ,open NUMERIC
    ,high NUMERIC
    ,low NUMERIC
    ,close NUMERIC
    ,volume INT
    ,id_stock INT
    ,id_index INT
    ,FOREIGN KEY (id_date) REFERENCES stocks.public.cat_dates(id)
    ,FOREIGN KEY (id_stock) REFERENCES stocks.public.cat_stock_names(id)
    ,FOREIGN KEY (id_index) REFERENCES stocks.public.cat_indexes(id)
);