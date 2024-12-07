from netmiko import ConnectHandler
import logging
from datetime import datetime as dt
logging.basicConfig(filename='netmiko.log', level=logging.INFO)
logger = logging.getLogger("netmiko")
from data import Data
from model import Model, Devices, Commands
from pydantic import ValidationError

class SyncNetmiko:
    def netmiko_connection(self, device: dict, commands: list[str]) -> str:
        try:
            connection = ConnectHandler(**device)
            output = connection.send_multiline(commands=commands)
            connection.disconnect()
            return output
        except Exception as e:
            logger.error(f"Error connecting to {device['host']}: {e}")
            return f"Error connecting to {device['host']}: {e}"

    def data_validation(self, devices: list[Devices], commands: Commands) -> None:
        try:
            Model(devices=devices, commands=commands)
        except ValidationError as error:
            logger.error(f"Data validation error: {error}\n")
            raise ValidationError(f"Data validation error: {error}")

    def run(self, data: Data) -> dict:
        self.data_validation(data.devices, data.commands)
        with open("./outputs/netmico_sync.log", "w") as f:
            start = dt.now()
            for device in data.devices:
                f.write(f"-> Host {device['host']}\n")
                output = self.netmiko_connection(device, commands=data.commands['commands'])
                f.write(f"Output from {device['host']}:\n{output}\n\n")
            end = dt.now()
            f.write(f"Total time: {end - start}")
        
        return {'result': f"Tiempo total: {end - start}"} 

if __name__ == "__main__":
    datos = Data()
    sync_netmiko = SyncNetmiko()
    print(sync_netmiko.run(datos))

