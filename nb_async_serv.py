import asyncio
import aiofiles
from netmiko import ConnectHandler
from pydantic import ValidationError
from datetime import datetime as dt
import logging
from data import Data
from model import Model, Devices, Commands
logging.basicConfig(filename='netmiko.log', level=logging.INFO)
logger = logging.getLogger("netmiko")

class AsyncNbNetmiko:
    async def netmiko_connection(self, device: dict, commands: list[str]) -> str:
        try:
            loop = asyncio.get_event_loop()
            connection = await loop.run_in_executor(None, lambda: ConnectHandler(**device))
            output = await loop.run_in_executor(None, connection.send_multiline, commands)
            await loop.run_in_executor(None, connection.disconnect)
            return output
        except Exception as error:
            logger.error(f"Error connecting to {device['host']}: {KeyError}")
            return f"Error connecting to {device['host']}: {error}"

    def data_validation(self, devices: list[Devices], commands: Commands) -> None:
        try:
            Model(devices=devices, commands=commands)
        except ValidationError as error:
            logger.error(f"Data validation error: {error}\n")
            raise ValidationError(f"Data validation error: {error}")

    async def run(self, data: "Data") -> dict:
        self.data_validation(data.devices, data.commands)
        start = dt.now()
        async with aiofiles.open("./outputs/netmiko_nb_async.log", "w") as f:
            tasks = []
            for device in data.devices:
                tasks.append(self.netmiko_connection(device, commands=data.commands['commands']))
                await f.write(f"-> Host {device['host']}\n")

            results = await asyncio.gather(*tasks)

            for device, output in zip(data.devices, results):
                await f.write(f"Output from {device['host']}:\n{output}\n\n")

            end = dt.now()
            await f.write(f"Total time: {end - start}")

        return {'result': f"Tiempo total: {end - start}"}

if __name__ == "__main__":
    # Datos iniciales
    datos = Data()
    async_netmiko = AsyncNbNetmiko()
    print (asyncio.run(async_netmiko.run(datos)))
