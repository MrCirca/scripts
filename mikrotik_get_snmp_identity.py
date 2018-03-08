#!/usr/bin/python3
import subprocess
import sys

path_file = sys.argv[1]
with open(path_file) as f:
    for line in f:
       line = line.strip()
       command = subprocess.run(['snmpget', '-v1', '-c', 'public', line, '.1.3.6.1.2.1.1.5.0'], stdout=subprocess.PIPE)
       print(line, command.stdout.decode().split()[-1])

    
    
