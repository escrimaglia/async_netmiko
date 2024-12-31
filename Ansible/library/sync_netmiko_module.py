# Netmiko module for Ansible
# Ed Scrimaglia

from netmiko import ConnectHandler
from datetime import datetime as dt
from ansible.module_utils.basic import AnsibleModule

unconnected_devices = []
connected_devices = []

def netmiko_connection(device: dict, commands: list[str]) -> str:
    status = False
    try:
        connection = ConnectHandler(**device)
        output = connection.send_multiline(commands=commands)
        connection.disconnect()
        status = True
        return status, output
    except Exception as error:
        return status, f"Error connecting to {device['host']}: {str(error)}"


def run(device: dict, commands: list[str]) -> dict:
    msg = "Sync Netmiko module run successfully"
    results = {}
    start = dt.now()

    status, response = netmiko_connection(device, commands)
    if status:
        response = response.splitlines()
        connected_devices.append({'host': device['host'], 'output': response})
    else:
        unconnected_devices.append({'host': device['host'], 'output': response})
   
    end = dt.now()
    results['connected_devices'] = connected_devices
    results['unconnected_devices'] = unconnected_devices
    results['time'] = {'result': f"Tiempo host: {end - start}"}
    
    return True, msg, results

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
        success, msg_ret, output = run(device=connection, commands=commands)
    else:
        success = False
        output = {}

    if success:
        module.exit_json(failed=False, msg=msg_ret, content=output)
    else:
        module.fail_json(failed=True, msg=msg_ret, content=output)

if __name__ == "__main__":
    main()

