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


def callback(manager, event):
    print(manager, event)

def parse_args():
    mode = sys.argv[1]
    item = sys.argv[2]
    action_args = sys.argv[3:]
    act_args = {}
    for action_arg in action_args:
        action_arg_key = action_arg.split('=')[0]
        action_arg_value = action_arg.split('=')[1]
        act_args[action_arg_key] = action_arg_value
    return mode, item, act_args


async def zabbix_discovery(discovery, args=None):    
    await manager.connect()
    mode, item, args = parse_args()
    if discovery == 'pjsip_trunks':
         endpoints_discovery = []
         action = {
             'Action': 'PJSIPShowRegistrationsOutbound'
         } 
         manager.register_event('OutboundRegistrationDetail', callback)
         result = await manager.send_action(action, **args)
         response, *events, end = result
         for event in events:
            if event.event == "OutboundRegistrationDetail":
                outbound_endpoint = event.endpoint
                endpoints_discovery.append({"{#ENDPOINT_NAME}": outbound_endpoint})
                print(json.dumps({'data': endpoints_discovery}))
    else:
        print("Discovery name does not exist")



async def zabbix_items(item, **args):
    await manager.connect()
    mode, item, args = parse_args()
    if item == 'pjsip_trunk_registration':
        action = {
             'Action': 'PJSIPShowRegistrationsOutbound'
         }
        result = await manager.send_action(action, **args)
        response, *events, end = result
        status = pjsip_trunk_registration(events, **args)
        return status
    elif item == 'pjsip_trunk_status':
        action = {
             'Action': 'PJSIPShowEndpoints'
         }
        result = await manager.send_action(action)
        response, *events, end = result
        status = pjsip_device_state(events, **args)
        return status
    else:
        print("Item name does not exist")      


def pjsip_device_state(endpoints, **args):
    for endpoint in endpoints:
        if endpoint.aor == args['Endpoint']:
            if endpoint.devicestate == "Available":
                print("100")
            elif endpoint.devicestate == "Not in use":
                print("200")
            elif endpoint.devicestate == "In use":
                print("300")
            elif endpoint.devicestate == "Busy":
                print("400")
            elif endpoint.devicestate == "Invalid":
                print("500")
            elif endpoint.devicestate == "Unavailable":
                print("600")
            elif endpoint.devicestate == "Ringing":
                print("700")
            elif endpoint.devicestate == "Ring in use":
                print("800")
            elif endpoint.devicestate == "On hold":
                print("900")



def pjsip_trunk_registration(trunks, **args):
    for trunk in trunks:
        if trunk.event == "OutboundRegistrationDetail":
            if trunk.endpoint == args['Endpoint']:
                 if trunk.status == "Registered":
                     print("0")
                 else:
                     print("1")

def main():
    manager.connect()
    mode, item, args = parse_args()
    try:
        args
    except IndexError:
        args = None
    loop = asyncio.get_event_loop()
    if mode == '-d':
        output = loop.run_until_complete(zabbix_discovery(item, **args))
    elif mode == '-i':
        output = loop.run_until_complete(zabbix_items(item, **args))
    return output
    manager.close()

main()
