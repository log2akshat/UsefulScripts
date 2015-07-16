#!/bin/bash

#    Copyright (C) <2015>  <Akshat Singh>
#    <akshat-pg8@iiitmk.ac.in>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# This Shell Script can be used to take take MySQL automated backup and tranfer
# the dump to remote server. This script will also deletes the dumps which are
# older than 3 days. Then it will take the backup of the databases and transfer
# the dumps to the remote server.
# NOTE : FEEL FREE TO EDIT FOR YOUR OWN CUSTOMIZED USAGE.


cd /home/akshat/MySQLBKP/
find . -name '*' -mtime +3 -exec rm -R {} \;

SUFFIX=`date +%d-%m-%Y`
DBUSER="root"
DBHOST="localhost"
DBPASS='password'
BACKUPDIR="/home/akshat/MySQLBKP"

DBS=`mysql -u$DBUSER -h$DBHOST -p$DBPASS -e"show databases"`

for DATABASE in $DBS
do
if [ $DATABASE != "Database" ]; then
FILENAME=$SUFFIX-bkp-$DATABASE.gz
mysqldump -u$DBUSER -h$DBHOST -p$DBPASS $DATABASE | gzip --best > $BACKUPDIR/$FILENAME
fi
done

## Server Location
ServerIP="XXX.XXX.XXX.XXX"
ServerLoc="/home/server/BACKUP/MySQL"
ServerUsername="server"
ServerBKPDirectory="MyBackup"

#Server Rsync
echo "======================================================"
echo "Server XXX.XXX.XXX.XXX  Database Rsyncing in Progress..."
echo "======================================================"
cd $BACKUPDIR
rsync -av $BACKUPDIR/$ServerBKPDirectory/ $ServerUsername@$ServerIP:$ServerLoc
