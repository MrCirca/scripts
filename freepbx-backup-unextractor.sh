#!/bin/bash

PATH_GIVEN=$1
gzip $PATH_GIVEN/mysql-*.sql
tar -Pczf $PATH_GIVEN.tgz -C $PATH_GIVEN .
