#!/bin/bash

# setting global variable for writing inside a database from file
mysql -h db -u root -p${MYSQL_ROOT_PASSWORD} <<EOF
SET GLOBAL local_infile=1;
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EOF

mysql -h db -u ${MYSQL_USER} -p${MYSQL_PASSWORD} -D delivery <<EOF
-- Create temporary staging table
CREATE TEMPORARY TABLE temp_package_type LIKE package_type;

-- Load CSV into temp table
LOAD DATA LOCAL INFILE 'data.csv'
INTO TABLE temp_package_type
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(name);

-- Insert only new names
INSERT INTO package_type (name)
SELECT t.name
FROM temp_package_type t
LEFT JOIN package_type u ON t.name = u.name
WHERE u.name IS NULL;

-- Clean up
DROP TEMPORARY TABLE temp_package_type;
EOF
