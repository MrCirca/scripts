#!/usr/bin/python
import requests
import json
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

def proxmox_endpoint_info(endpoint):
	proxmox_information = requests.get(proxmox_api_url+endpoint, cookies=cookies, verify=False).json()
	return proxmox_information

def proxmox_nodes_names():
	node_list = []
	proxmox_nodes_info = proxmox_endpoint_info('nodes/')
	for proxmox_node in proxmox_nodes_info["data"]:
		node_list.append(proxmox_node["id"].split('/')[1])
	return node_list

def discover_proxmox_cluster_nodes():
	discovered_nodes = []
	proxmox_nodes = proxmox_nodes_names()
	for node in proxmox_nodes:
		discovered_nodes.append({"{#PROXMOX_CLUSTER_NODE}": node })
	print(json.dumps({'data' : discovered_nodes }))

def proxmox_vms_names():
	proxmox_node_vms = []
	proxmox_nodes = proxmox_nodes_names()
	for node in proxmox_nodes:
		proxmox_vms_info = proxmox_endpoint_info('nodes/'+node+'/qemu/')
		for vm in proxmox_vms_info["data"]:
			proxmox_node_vms.append({"{#PROXMOX_VM}": vm["name"] })
	print(json.dumps({'data' : proxmox_node_vms }))

def proxmox_cts_names():
        proxmox_node_cts = []
        proxmox_nodes = proxmox_nodes_names()
        for node in proxmox_nodes:
                proxmox_cts_info = proxmox_endpoint_info('nodes/'+node+'/lxc/')
                for ct in proxmox_cts_info["data"]:
                        proxmox_node_cts.append({"{#PROXMOX_CT}": ct["name"] })
        print(json.dumps({'data' : proxmox_node_cts }))
			
			
#proxmox_nodes_names()
#discover_proxmox_cluster_nodes()
proxmox_vms_names()
proxmox_cts_names()
#discover_proxmox_cluster_nodes()
