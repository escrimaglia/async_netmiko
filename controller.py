from fastapi import Depends, FastAPI, Request
import pytz
from data import Data
from model import Model
from async_serv import AsyncNetmiko
from sync_serv import SyncNetmiko

#local_timezone = pytz.timezone('America/Argentina/Buenos_Aires')
app = FastAPI(title="Netmiko", description="Sync and Async Netmiko", version="1.0.0", summary="Automate Network Devices with Netmiko")

# Injeccion de dependencias
async_netmiko = AsyncNetmiko()
sync_netmiko = SyncNetmiko()


@app.post("/api/v1/netmiko/async", response_model = dict, tags=["Netmiko"])
async def netmiko_async(request: Request, data: Data = Depends(Data)):
    return await async_netmiko.run(data=data)
    

@app.post("/api/v1/netmiko/sync", response_model = dict, tags=["Netmiko"])
def netmiko_sync(request: Request, data: Data = Depends(Data)):
    return sync_netmiko.run(data=data)
