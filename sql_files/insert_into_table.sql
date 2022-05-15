-- LOAD DATA INFILE '/store_files_mysql/clean_store_transactions.csv' INTO TABLE clean_store_transactions FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
COPY Weather(City, State, Description, Temperature,Feels_Like_Temperature, Min_Temperature, Max_Temperature, Humidity, Clouds)
FROM '/store_files_postgres/result_many_city.csv'
DELIMITER ','
CSV HEADER;