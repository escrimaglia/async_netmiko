import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi import Depends, FastAPI, Request
import pytz
from Scripts.data import Data
from Scripts.async_serv import AsyncNetmiko
from Scripts.sync_serv import SyncNetmiko
from Scripts.nb_async_serv import AsyncNbNetmiko

local_timezone = pytz.timezone('America/Argentina/Cordoba')
app = FastAPI(title="Netmiko", description="Sync and Async Netmiko", version="1.0.0", summary="Automate Network Devices with Netmiko")


@app.post("/api/v1/netmiko/async", response_model = dict, tags=["Netmiko"], summary="Netmiko Async")
async def netmiko_async(request: Request, data: Data = Depends(Data)):
    return await AsyncNetmiko().run(data=data)
    

@app.post("/api/v1/netmiko/sync", response_model = dict, tags=["Netmiko"], summary="Netmiko Sync")
def netmiko_sync(request: Request, data: Data = Depends(Data)):
    return SyncNetmiko().run(data=data)

@app.post("/api/v1/netmiko/nb-async", response_model = dict, tags=["Netmiko"], summary="Netmiko Non-Blocking Async")
async def netmiko_nb_async(request: Request, data: Data = Depends(Data)):
    return await AsyncNbNetmiko().run(data=data)