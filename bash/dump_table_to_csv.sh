#!/usr/bin/env bash
# taken from http://stackoverflow.com/questions/4589891/mysql-dump-into-csv-text-files-with-column-names-at-the-top
DBNAME=mhealth_apps
TABLE=$1

FNAME=$2/dump_$(date +%Y.%m.%d)-$TABLE.csv

#(1)creates empty file and sets up column names using the information_schema
mysql -u root -proot $DBNAME -B -e "SELECT COLUMN_NAME FROM information_schema.COLUMNS C WHERE table_name = '$TABLE' AND TABLE_SCHEMA = 'mhealth_apps' order by ordinal_position;" | awk '{print $1}' | grep -iv ^COLUMN_NAME$ | sed 's/^/"/g;s/$/"/g' | tr '\n' ',' > $FNAME
echo $FNAME
#(2)appends newline to mark beginning of data vs. column titles
echo "" >> $FNAME

#(3)dumps data from DB into /var/mysql/tempfile.csv

mysql -u root -proot $DBNAME -B -e "SELECT * INTO OUTFILE '`pwd`/bash/tempfile.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' FROM $TABLE;"

#(4)merges data file and file w/ column names
cat `pwd`/bash/tempfile.csv >> $FNAME

#(5)deletes tempfile
rm -rf `pwd`/bash/tempfile.csv