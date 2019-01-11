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
         action = {
             'Action': 'PJSIPShowRegistrationsOutbound'
         }
         result = await manager.send_action(action, **args)
         response, *events, end = result
         print(events)


def main():
    manager.connect()
    mode, item, args = parse_args()
    try:
        args
    except IndexError:
        args = None
    loop = asyncio.get_event_loop()
    if mode == '-d':
        discovery_output = loop.run_until_complete(zabbix_discovery(item, **args))
    return discovery_output

main()
