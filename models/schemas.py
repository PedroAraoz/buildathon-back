import uuid
from pydantic import BaseModel

class ClaimDrop(BaseModel):
    wallet: str
    lat: float
    lon: float


class Poap(BaseModel):
    id: uuid.UUID
    url: str
    claimed_by: str | None = None
    drop_id: uuid.UUID
    class Config:
        orm_mode = True

class PoapCreate(BaseModel):
    url: str

class DropInfo(BaseModel):
    name: str
    description: str
    image_url: str

class Drop(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    store_id: uuid.UUID
    image_url: str
    poaps: list[Poap] = []
    class Config:
        orm_mode = True

class DropCreate(BaseModel):
    name: str
    description: str
    store_id: uuid.UUID
    image_url: str


class Store(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    geohash: str
    drops: list[Drop] = []
    class Config:
        orm_mode = True

class StoreCreate(BaseModel):
    name: str
    description: str
    geohash: str