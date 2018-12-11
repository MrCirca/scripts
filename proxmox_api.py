#!/usr/bin/python
import requests
import json
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if len(sys.argv) != 4:
	print("Required 3 arguments host, username, password", file=sys.stderr)
	sys.exit(1)

host, username, password = sys.argv[1:4]
api_url = 'https://'+host+':8006/api2/json/'
creds = {'username':username, 'realm':'pam', 'password':password}
r = requests.post(api_url+'access/ticket', verify=False, data=creds)
result = r.json()
ticket = result["data"]["ticket"]
token = result["data"]["CSRFPreventionToken"]
cookies = dict(PVEAuthCookie=ticket)

def endpoint_info(endpoint):
	information = requests.get(api_url+endpoint, cookies=cookies, verify=False).json()
	return information

def nodes_names():
	node_list = []
	nodes_info = endpoint_info('nodes/')
	for node in nodes_info["data"]:
		node_list.append(node["id"].split('/')[1])
	return node_list

def backend_ids(backend):
	vms_id_list = []
	nodes = nodes_names()
	for vm_id in nodes:
		vms_info = endpoint_info('nodes/'+vm_id+'/'+backend+'/')
		for vm in vms_info["data"]:
			vms_id_list.append(vm["vmid"])
	print(vms_id_list)
	return vms_id_list

def discover_cluster_nodes():
	discovered_nodes = []
	nodes = nodes_names()
	for node in nodes:
		discovered_nodes.append({"{#PROXMOX_CLUSTER_NODE}": node })
	print(json.dumps({'data' : discovered_nodes }))

def vms_names():
	node_vms = []
	nodes = nodes_names()
	for node in nodes:
		vms_info = endpoint_info('nodes/'+node+'/qemu/')
		for vm in vms_info["data"]:
			node_vms.append({"{#PROXMOX_VM_ID}": vm["id"] })
	print(json.dumps({'data' : node_vms }))

def cts_names():
        node_cts = []
        nodes = nodes_names()
        for node in nodes:
                cts_info = endpoint_info('nodes/'+node+'/lxc/')
                for ct in cts_info["data"]:
                        node_cts.append({"{#PROXMOX_CT_ID}": ct["id"] })
        print(json.dumps({'data' : node_cts }))
			
backend_ids('lxc')
#discover_cluster_nodes()
#vms_names()
#cts_names()
#discover_cluster_nodes()
