#/usr/bin/python
import os
import sys
import subprocess as sp

fping_count = sys.argv[1]
fping_target = sys.argv[5]
fping_period = sys.argv[2]
fping_bytes_size = sys.argv[3]
fping_timeout = sys.argv[4]

with open(os.devnull, 'w') as devnull:
    fping_command = sp.check_output(['fping', '-q', '-c', fping_count, '-p', fping_period, '-b', fping_bytes_size, '-t', fping_timeout, fping_target], stderr=devnull).decode()

print(fping_command)
