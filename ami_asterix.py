#!/root/pyenv/bin/python3
import panoramisk
import asyncio
import sys
import json
import asterisk_ami_config


conf = asterisk_ami_config.ami_config
manager = panoramisk.Manager(
        loop=asyncio.get_event_loop(),
        host=conf['host'],
        username=conf['username'],
        secret=conf['secret'],
        port=5038,
        ssl=False,
        encoding='utf8')


action = sys.argv[1]

@manager.register_event('')
def callback(manager, event):
    print(manager, event)

async def send_ami_action(ami_action, **kwargs):
    await manager.connect()
    kwargs['Action'] = ami_action
    result = await manager.send_action(kwargs)
#    print(result)
    response, *events, end = result
    if not response.response == 'Success':
        return "ERROR"
    return events
    manager.close()

def zabbix_endpoints_discovery(endpoints):    
    endpoints_discovery = []
    for endpoint in endpoints:
        if endpoint.contacts:
            endpoints_discovery.append({"{#ENDPOINT_NAME}": endpoint.contacts.split("/")[0]})
    print(json.dumps({'data': endpoints_discovery}))

def main():
    loop = asyncio.get_event_loop()
    tt = loop.run_until_complete(send_ami_action(action))
    for gg in tt:
        print(gg.aor)
    manager.loop.close()

def get_endpoint_info(endpoints, endpoint_name):
    for endpoint in endpoints:
       if endpoint.contacts:
           print(endpoint.devicestate)

def pjsip_outbound_registrations(endpoints):
    for endpoint in endpoints:
        print(endpoint.status)
    
main()
