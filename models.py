from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID, uuid4
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    user = "user"

# User model
class User(BaseModel):
    id: Optional[UUID] = uuid4()
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    roles: List[Role]

# StationInfo model
class StationInfo(BaseModel):
    evaNumber: str
    name: str

# BusInfo model for serialization
class BusInfoModel(BaseModel):
    bus_line: str
    route: str
    total_stations: int
    stations: List[dict]  # You can define a more specific model for stations if needed
