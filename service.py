from fastapi import HTTPException
from sqlalchemy.orm import Session
import models.models as models, models.schemas as schemas
import uuid
import crud
from geolib import geohash

PRESITION = 7

def get_unclaimed(db: Session, drop_id: uuid.UUID, claim: schemas.ClaimDrop):
    drop = get_drop(db, drop_id)
    if not check_location(db, drop, claim):
        raise  HTTPException(status_code=400, detail="Drop does not exist")
    return crud.get_unclaimed(db, drop.id, claim.wallet)
    
def check_location(db: Session, drop: models.Drop, claim: schemas.ClaimDrop):
    store = get_store(db, drop.store_id)

    store_geohash = store.geohash
    user_geohash = geohash.encode(claim.lat, claim.lon, PRESITION)
    return store_geohash.startswith(user_geohash)

def get_store(db: Session, store_id: uuid.UUID):
    store = crud.get_store(db, store_id)
    if store == None:
        raise HTTPException(status_code=404, detail="Store does not exist")
    return store

def get_drop(db: Session, drop_id: uuid.UUID):
    drop = crud.get_drop(db, drop_id)
    if drop == None:
        raise HTTPException(status_code=404, detail="Drop does not exist")
    return drop