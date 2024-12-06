from netmiko import ConnectHandler
import logging
from datetime import datetime as dt
logging.basicConfig(filename='netmiko.log', level=logging.CRITICAL)
logger = logging.getLogger("netmiko")
from data import devices, commands

# Methods
def netmiko_connection(device: dict, commands: list[str]) -> str:
    try:
        connection = ConnectHandler(**device)
        output = connection.send_multiline(commands=commands)
        connection.disconnect()
        return output
    except Exception as e:
        logger.error(f"Error connecting to {device['host']}: {e}")
        return f"Error connecting to {device['host']}: {e}"

with open("./outputs/netmico_sync.log", "w") as f:
    start = dt.now()
    for device in devices:
        f.write(f"-> Host {device['host']}\n")
        output = netmiko_connection(device, commands=commands)
        f.write(f"Output from {device['host']}:\n{output}\n\n")
    end = dt.now()
    f.write(f"Total time: {end - start}")

print(f"Total time: {end - start}")

