from pydantic import BaseModel
from typing import List, Dict

class Devices(BaseModel):
    host: str
    username: str
    password: str
    device_type: str
    port: int | None = None
    ssh_config_file: str | None = None

class Commands(BaseModel):
    commands: List[str]

class Model(BaseModel):
    devices: List[Devices]
    commands: Commands


