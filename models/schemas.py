import uuid
from pydantic import BaseModel

class Coordinates(BaseModel):
    x: float
    y: float


class Poap(BaseModel):
    id: uuid.UUID
    url: str
    claimed_by: str | None = None
    drop_id: uuid.UUID
    class Config:
        orm_mode = True

class PoapCreate(BaseModel):
    url: str

class Drop(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    store_id: uuid.UUID
    poaps: list[Poap] = []
    class Config:
        orm_mode = True

class DropCreate(BaseModel):
    name: str
    description: str
    store_id: uuid.UUID


class Store(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    drops: list[Drop] = []
    class Config:
        orm_mode = True

class StoreCreate(BaseModel):
    name: str
    description: str