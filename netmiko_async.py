import asyncio
from concurrent.futures import ThreadPoolExecutor
from netmiko import ConnectHandler
from datetime import datetime as dt
import logging
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

async def run_device_command(device: dict, executor: ThreadPoolExecutor, commands: list[str]) -> str:
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, netmiko_connection, device, commands)
    return result

async def main(devices: list[dict], commands: list) -> list[str]:
    # Crear un ThreadPoolExecutor para las tareas en paralelo
    with ThreadPoolExecutor(max_workers=10) as executor:
        tasks = [run_device_command(device, executor, commands=commands) for device in devices]
        results = await asyncio.gather(*tasks)
        return results

if __name__ == "__main__":
    start = dt.now()
    results = asyncio.run(main(devices, commands))
    end = dt.now()

    with open("./outputs/netmiko_async.log", "w") as f:
        for result in results:
            f.write(f"-> {result}\n")
        f.write(f"Tiempo total: {end - start}\n")

    print(f"Tiempo total: {end - start}")
