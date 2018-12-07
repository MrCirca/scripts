#!/usr/bin/python
import requests
import json
import sys

proxmox_api_url = 'https://'+sys.argv[1]+':8006/api2/json/'
proxmox_creds = {'username':sys.argv[2], 'realm':'pam', 'password':sys.argv[3]}
r = requests.post(proxmox_api_url+'access/ticket', verify=False, data=proxmox_creds)
result = r.json()
ticket = result["data"]["ticket"]
token = result["data"]["CSRFPreventionToken"]
cookies = dict(PVEAuthCookie=ticket)

main_request = requests.get(proxmox_api_url, cookies=cookies, verify=False)
print(main_request.json())
