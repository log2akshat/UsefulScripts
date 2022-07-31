#!/bin/bash

USER='root'
PASSWORD='topsecret'
OUTPUT='/home/akshat/SCRIPTS/BACKUPS/MySQLBKP/'

rm "$OUTPUT/*gz" > /dev/null 2>&1

databases=`mysql --user=$USER --password=$PASSWORD -e "SHOW DATABASES;" | tr -d "| " | grep -v Database`

for db in $databases; do
    if [[ "$db" != "information_schema" ]] && [[ "$db" != _* ]] ; then
        echo "Dumping database: $db"
        mysqldump --force --opt --user=$USER --password=$PASSWORD --databases $db > $OUTPUT/$db.sql_`date +%d"-"%m"-"%Y_%H":"%M":"%S`
        #gzip $OUTPUT/`date +%Y%m%d`.$db.sql
    fi
done

