from pydantic import BaseModel
from typing import List, Dict

class Model(BaseModel):
    devices: List[Dict]
    commands: List[str]
