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


@manager.register_event('*')
def callback(manager, event):
    print('Callback Wild:', event)

@manager.register_event('DeviceStateChange')
def callback2(manager, event):
    print("Callback DiviceStateChange:", event)




async def send_ami_action(ami_action, **kwargs):
    while True:
        #print('Starting')
        await manager.connect()
        kwargs['Action'] = ami_action
        result = await manager.send_action(kwargs)
        print("ACTION")
        #manager.close() EROOOOOR
        response, *events, end = result
        await asyncio.sleep(5)

def zabbix_endpoints_discovery(endpoints):    
    endpoints_discovery = []
    for endpoint in endpoints:
        if endpoint.endpoint:
            endpoints_discovery.append({"{#ENDPOINT_NAME}": endpoint.endpoint})
    print(json.dumps({'data': endpoints_discovery}))

def main():
    try:
        asyncio.ensure_future(send_ami_action(action))
        #manager.loop.create_task(send_ami_action(action))
        manager.loop.run_forever()
    except KeyboardInterrupt:
        manager.loop.close()

def get_endpoint_info(endpoints, endpoint_name):
    for endpoint in endpoints:
       if endpoint.contacts:
           print(endpoint.devicestate)

def pjsip_outbound_registrations(endpoints, endpoint_name):
    for endpoint in endpoints:
        if endpoint.endpoint == endpoint_name:
            print(endpoint.status)
   
main()
