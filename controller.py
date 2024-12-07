from fastapi import Depends, FastAPI, Request
import pytz
from data import Data
from async_serv import AsyncNetmiko
from sync_serv import SyncNetmiko

local_timezone = pytz.timezone('America/Argentina/Cordoba')
app = FastAPI(title="Netmiko", description="Sync and Async Netmiko", version="1.0.0", summary="Automate Network Devices with Netmiko")


@app.post("/api/v1/netmiko/async", response_model = dict, tags=["Netmiko"])
async def netmiko_async(request: Request, data: Data = Depends(Data)):
    return await AsyncNetmiko().run(data=data)
    

@app.post("/api/v1/netmiko/sync", response_model = dict, tags=["Netmiko"])
def netmiko_sync(request: Request, data: Data = Depends(Data)):
    return SyncNetmiko().run(data=data)
