#!/usr/bin/python
import requests
import json
import sys
if len(sys.argv) != 4:
	print("Required 3 arguments host, username, password", file=sys.stderr)
	sys.exit(1)

proxmox_host, proxmox_username, proxmox_password = sys.argv[1:4]
proxmox_api_url = 'https://'+proxmox_host+':8006/api2/json/'
proxmox_creds = {'username':proxmox_username, 'realm':'pam', 'password':proxmox_password}
r = requests.post(proxmox_api_url+'access/ticket', verify=False, data=proxmox_creds)
result = r.json()
ticket = result["data"]["ticket"]
token = result["data"]["CSRFPreventionToken"]
cookies = dict(PVEAuthCookie=ticket)

def discover_proxmox_cluster_nodes():
	proxmox_cluster_nodes = []
	proxmox_nodes_request = requests.get(proxmox_api_url+'nodes/', cookies=cookies, verify=False).json()
	for node in proxmox_nodes_request["data"]:
		proxmox_cluster_nodes.append({"{#PROXMOX_CLUSTER_NODE}": node["id"].split('/')[1] })
	print(json.dumps({'data' : proxmox_cluster_nodes }))

discover_proxmox_cluster_nodes()
