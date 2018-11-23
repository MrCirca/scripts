#!/usr/bin/python

import json
import subprocess as sp
import sys

nargs = len(sys.argv)

if nargs == 1:
    services = []
    supervisor_services = sp.check_output(["supervisorctl", "status"]).decode()
    for line in supervisor_services.splitlines():
        service_name = line.split()[0]
        services.append({"#SUPERVISOR_SERVICE": service_name })
    print(json.dumps({'data' : services }))

elif nargs == 3:
    supervisor_service = sys.argv[1]
    service_status = sp.check_output(["supervisorctl", "status", supervisor_service]).decode()
    if "(no such process)" in service_status:
        print("Process does not exists")
    else:
        if sys.argv[2] == "uptime":
            service_uptime = service_status.split()[5]
            print(service_uptime)
        elif sys.argv[2] == "state":
            service_state = service_status.split()[1]
            print(service_state)
        else:
            print("Wrong Argument")
else:
    print("Wrong")

