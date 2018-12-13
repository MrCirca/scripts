#!/usr/bin/python3
import requests
import proxmox_api_config as config
import json
from proxmoxer import ProxmoxAPI

proxmox = ProxmoxAPI(config.api_config["host"], user=config.api_config["username"], password=config.api_config["password"], verify_ssl=False)

def discover_cts_vms(backend):
    vm_names = []
    for node in proxmox.nodes.get():
        for vm in proxmox.nodes(node["node"]).get('{}'.format(backend)):
            vm_names.append({"{{#PROXMOX_{}_NAME}}".format(backend.upper()): vm["name"]})
    return vm_names

print(json.dumps({'data' : discover_cts_vms('lxc')+discover_cts_vms('qemu') }))

