#!/bin/bash

LATEST_BACKUP_FILE="$(ls -tr /var/spool/asterisk/backup/test/*.tgz | tail -1)"
EXTRACTED_DIRECTORY="/var/spool/asterisk/backup/Full_Backup/last_backup_extracted"

if [ ! -d "$EXTRACTED_DIRECTORY" ]; then
	mkdir "$EXTRACTED_DIRECTORY"
else
	echo "Directory exists"
fi
tar xzf "$LATEST_BACKUP_FILE" -C "$EXTRACTED_DIRECTORY"
gunzip $EXTRACTED_DIRECTORY/mysql-*.sql.gz
