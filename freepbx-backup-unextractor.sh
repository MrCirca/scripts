#!/bin/bash

PATH_GIVEN=$1
COMPRESS_DATABASES="$(gzip "$PATH_GIVEN/mysql-2.sql" && gzip "$PATH_GIVEN/mysql-3.sql")"
COMPRESS_BACKUP_DIRECTORY="$(tar -Pzcf "$PATH_GIVEN.tgz" "$PATH_GIVEN")"
