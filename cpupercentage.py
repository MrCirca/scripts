#!/usr/bin/python
import subprocess
import sys
import re

vm = str(sys.argv[1])
cpu_number = int(sys.argv[2])
cpu_seconds_line_number = cpu_number * 3 + 1
command_output = subprocess.check_output(["virsh", "cpu-stats", vm ])
lines_list = command_output.split("\n")
line = lines_list[cpu_seconds_line_number]
#line_column = line.split()
#cpu_time =  line_column[1]
#print cpu_time
regex = re.search(r'^\D+(\d+\.\d+).*$', line)
print regex.group(1)
