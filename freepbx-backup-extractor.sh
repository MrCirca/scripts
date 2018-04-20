#!/bin/bash

LATEST_BACKUP_FILE="$(ls -tr /var/spool/asterisk/backup/Full_Backup/*.tgz | tail -1)"
EXTRACTED_DIRECTORY="/var/spool/asterisk/backup/Full_Backup/last_backup_extracted"

if [ ! -d "$EXTRACTED_DIRECTORY" ]; then
	CREATE_EXTRACTED_DIRECTORY=$(mkdir "$EXTRACTED_DIRECTORY")
else
	echo "File Exist"
fi
DECOMPRESS_BACKUP_FILE=$(tar xzf "$LATEST_BACKUP_FILE" -C "$EXTRACTED_DIRECTORY")
EXTRACT_DATABASES="$(gunzip "$EXTRACTED_DIRECTORY/mysql-2.sql.gz" && gunzip "$EXTRACTED_DIRECTORY/mysql-3.sql.gz")"
