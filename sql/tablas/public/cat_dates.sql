CREATE TABLE stocks.public.cat_dates
(
    id INT
    ,"date" DATE
    ,"day" INT
    ,id_week_day INT
    ,"month" INT
    ,id_month INT
    ,"year" INT
    ,id_quarter INT
    ,FOREIGN KEY (id_week_day) REFERENCES stocks.public.cat_days_of_week(id)
    ,FOREIGN KEY (id_month) REFERENCES stocks.public.cat_months(id)
    ,FOREIGN KEY (id_quarter) REFERENCES stocks.public.cat_quarters(id)
);