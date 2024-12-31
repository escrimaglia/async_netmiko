# Async Netmiko Module for Ansible
# Ed Scrimaglia

import asyncio
from netmiko import ConnectHandler
from datetime import datetime as dt
from ansible.module_utils.basic import AnsibleModule

unconnected_devices = []
connected_devices = []

async def netmiko_connection(device: dict, commands: list[str]) -> str:
    status = False
    try:
        loop = asyncio.get_event_loop()
        connection = await loop.run_in_executor(None, lambda: ConnectHandler(**device))
        output = await loop.run_in_executor(None, connection.send_multiline, commands)
        await loop.run_in_executor(None, connection.disconnect)
        status = True
        return status, output.splitlines()
    except Exception as error:
        return False, f"Error connecting to {device['host']}: {str(error)}"

async def run(device: dict, commands: list[str]) -> dict:
    msg = "Async Netmiko module run successfully"
    response = {}
    start = dt.now()
    status, result = await netmiko_connection(device, commands=commands)

    if status:
        connected_devices.append({'host': device['host'], 'output': result})
    else:
        unconnected_devices.append({'host': device['host'], 'output': result})

    #results = await asyncio.gather(*tasks)

    end = dt.now()
    response['connected_devices'] = connected_devices
    response['unconnected_devices'] = unconnected_devices
    response['time'] = {'result': f"Tiempo host: {end - start}"}
    
    return True, msg, response

def main():
    module=AnsibleModule(
        argument_spec=dict(
            device = dict(required=True, type='dict'),
            commands = dict(required=True, type='list')
        )
    )
    connection = {}
    device_param = module.params.get("device")
    connection['host'] = device_param['host']
    connection['username'] = device_param['username']
    connection['password'] = device_param['password']
    connection['device_type'] = device_param['device_type']
    connection['ssh_config_file'] = device_param['ssh_config_file']
    commands = module.params.get("commands")


    if device_param:
        success, msg_ret, output = asyncio.run(run(device=connection,commands=commands))
    else:
        success = False
        output = {}

    if success:
        module.exit_json(failed=False, msg=msg_ret, content=output)
    else:
        module.fail_json(failed=True, msg=msg_ret, content=output)

if __name__ == "__main__":
    main()
