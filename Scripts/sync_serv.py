# Sync Netmiko Class
# Ed Scrimaglia

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from netmiko import ConnectHandler
import logging
from datetime import datetime as dt
logging.basicConfig(filename='../Logs/netmiko.log', level=logging.INFO)
logger = logging.getLogger("netmiko")
from FastApi.model import Model, Devices, Commands
from pydantic import ValidationError

class SyncNetmiko:
    def netmiko_connection(self, device: dict, commands: list[str]) -> str:
        try:
            connection = ConnectHandler(**device)
            output = connection.send_multiline(commands=commands)
            connection.disconnect()
            return output
        except Exception as error:
            logger.error(f"Error connecting to {device['host']}: {str(error)}")
            return f"Error connecting to {device['host']}: {str(error)}"

    def data_validation(self, devices: list[Devices], commands: Commands) -> None:
        try:
            Model(devices=devices, commands=commands)
        except ValidationError as error:
            logger.error(f"Data validation error: {str(error)}\n")
            raise ValidationError(f"Data validation error: {str(error)}")

    def run(self, data) -> dict:
        self.data_validation(data.devices, data.commands)
        with open("../outputs/netmiko_sync.log", "w") as f:
            start = dt.now()
            for device in data.devices:
                f.write(f"-> Host {device['host']}\n")
                output = self.netmiko_connection(device, commands=data.commands['commands'])
                f.write(f"Output from {device['host']}:\n{output}\n\n")
            end = dt.now()
            f.write(f"Total time: {end - start}")
        
        return {'result': f"Tiempo total: {end - start}"} 

# If running as a script
if __name__ == "__main__":
    from data import Data
    datos = Data()
    sync_netmiko = SyncNetmiko()
    print(sync_netmiko.run(datos))

