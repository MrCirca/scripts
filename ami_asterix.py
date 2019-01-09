#!/root/pyenv/bin/python3
import panoramisk
import asyncio
import sys
import json
import asterisk_ami_config


conf = asterisk_ami_config.ami_config
manager = panoramisk.Manager(loop=asyncio.get_event_loop(),host=conf['host'], username=conf['username'], secret=conf['secret'], port=5038, ssl=False, encoding='utf8')
action = sys.argv[1]

@manager.register_event('*')
def callback(manager, event):
    print(manager, event)

async def send_ami_action(ami_action):
    await manager.connect()
    result = await manager.send_action({'Action': ami_action, 'Endpoint': '500'})    
    print(result)
    manager.close()
    response, *events, end = result
    if not response.response == 'Success':
        return "ERROR"
    return events

def zabbix_endpoints_discovery(endpoints):    
    endpoints_discovery = []
    for endpoint in endpoints:
        if endpoint.contacts:
            endpoints_discovery.append({"{#ENDPOINT_NAME}": endpoint.contacts.rstrip(",")})
    print(json.dumps({'data': endpoints_discovery}))

def tt(endpoints):
    for endpoint in endpoints:
        print(endpoints)

def main():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(send_ami_action(action))
    loop.run_forever()
#    endpoints = loop.run_until_complete(send_ami_action(action))
#    zabbix_endpoints_discovery(endpoints)
#    get_endpoint_info(endpoints, sys.argv[2])
    loop.close()

def get_endpoint_info(endpoints, endpoint_name):
    for endpoint in endpoints:
       if endpoint.contacts:
           print(endpoint.devicestate) 
main()
