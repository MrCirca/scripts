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

def backend_info(backend):
    nodes = nodes_names()
    for virt_id in nodes:
        virt_info = endpoint_info('nodes/{}/{}/'.format(virt_id,backend))
    return virt_info

def backend_ids(backend):
    virt_id_list = []
    virt_info = backend_info(backend)
    for virt_id in virt_info["data"]:
        virt_id_list.append(virt_id["vmid"])
    return virt_id_list

def backend_names(backend):
    virt_name_list = []
    virt_info = backend_info(backend)
    for virt_name in virt_info["data"]:
        virt_name_list.append(virt_name["name"])
    return virt_name_list

def discover_backend_names(backend):
    discover_backend_name_list = []
    virt_names = backend_names(backend)
    for name in virt_names:
        discover_backend_name_list.append({"{{#PROXMOX_{}_NAME}}".format(backend.upper()): name })
    return discover_backend_name_list 

def backend_status(backend):
    virt_ids = backend_ids(backend)
    nodes = nodes_names()
    for node in nodes:
        for virt_id in virt_ids:
            virt_status = endpoint_info('nodes/{}/{}/{}/status/current'.format(node,backend,virt_id))


print(json.dumps({'data' : discover_backend_names('qemu')+discover_backend_names('lxc') }))
