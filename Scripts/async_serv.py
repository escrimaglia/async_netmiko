# Async Netmiko Class
# Ed Scrimaglia

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import asyncio
from concurrent.futures import ThreadPoolExecutor
from netmiko import ConnectHandler
from datetime import datetime as dt
import logging
logging.basicConfig(filename='../Logs/netmiko.log', level=logging.INFO)
logger = logging.getLogger("netmiko")
from FastApi.model import Model, Devices, Commands
from pydantic import ValidationError
from typing import List

class AsyncNetmiko:
    def netmiko_connection(self, device: dict, commands: list[str]) -> str:
        try:
            connection = ConnectHandler(**device)
            output = connection.send_multiline(commands=commands)
            connection.disconnect()
            return output
        except Exception as error:
            logger.error(f"Error connecting to {device['host']}: {str(error)}")
            return f"Error connecting to {device['host']}: {str(error)}"

    async def run_device_command(self, device: dict, executor: ThreadPoolExecutor, commands: list[str]) -> str:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(executor, self.netmiko_connection, device, commands)
        return result

    async def main(self, devices: List[Devices], commands: dict) -> list[str]:
        with ThreadPoolExecutor(max_workers=10) as executor:
            tasks = [self.run_device_command(device, executor, commands=commands['commands']) for device in devices]
            results = await asyncio.gather(*tasks)
            return results
        
    def data_validation(self, devices: List[Devices], commands: Commands) -> None:
        try:
            Model(devices=devices, commands=commands)
        except ValidationError as error:
            logger.error(f"Data validation error: {error}\n")
            raise ValidationError(f"Data validation error: {error}")
    
    async def run(self, data) -> dict:
        self.data_validation(data.devices, data.commands)
        start = dt.now()
        results = await self.main(devices=data.devices, commands=data.commands)
        end = dt.now()
        with open("../outputs/netmiko_async.log", "w") as f:
            for result in results:
                f.write(f"-> {result}\n")
            f.write(f"Tiempo total: {end - start}\n")

        return {'result': f"Tiempo total: {end - start}"}

# If running as a script
if __name__ == "__main__":
    from data import Data
    data = Data()
    netmiko = AsyncNetmiko()
    print (asyncio.run(netmiko.run(data=data)))
