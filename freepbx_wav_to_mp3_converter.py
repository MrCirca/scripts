#!/usr/bin/python3

import MySQLdb
import subprocess
import os.path
import sys

file_format = sys.argv[1]
record_files =  subprocess.check_output(['find', '/var/spool/asterisk/monitor/', '-type', 'f', '-name', '*.wav']).decode()

for wav_file in record_files.splitlines():
	name, ext = os.path.splitext(wav_file)
	prefer_format_file = "{}.".format(name)+file_format
	subprocess.check_output(['ffmpeg', '-i', wav_file, prefer_format_file, '-y'])
	os.remove(wav_file)

try:
    conn = MySQLdb.connect(host="localhost", db="asteriskcdrdb")
    cursor = conn.cursor()

except Exception as e:
    error = True

cursor.execute("SELECT uniqueid,recordingfile FROM cdr")
result = cursor.fetchall()
for unique_id, record_file in result:
    name, ext = os.path.splitext(record_file)
    if ext == ".wav":
        print(ext)
        cursor.execute("UPDATE cdr SET recordingfile='{}.".format(name) + file_format + "'" + " WHERE uniqueid='{}'".format(unique_id))
        conn.commit()

