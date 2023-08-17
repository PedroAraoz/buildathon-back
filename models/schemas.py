import uuid
from pydantic import BaseModel
from datetime import date


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
    start_date: date
    end_date: date


class PoapInfo(BaseModel):
    claimed_by: str
    claimed_on: date
    drop: DropInfo


class Drop(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    store_id: uuid.UUID
    image_url: str
    start_date: date
    end_date: date
    poaps: list[Poap] = []

    class Config:
        orm_mode = True


class DropCreate(BaseModel):
    name: str
    description: str
    store_id: uuid.UUID
    image_url: str
    start_date: date
    end_date: date


class Store(BaseModel):
    id: uuid.UUID
    name: str
    geohash: str
    drops: list[Drop] = []

    class Config:
        orm_mode = True


class StoreCreate(BaseModel):
    name: str
    geohash: str
