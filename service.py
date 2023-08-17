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
        raise HTTPException(status_code=400, detail="You are too far away!")
    if already_claimed(db, drop.id, claim.wallet):
        raise HTTPException(status_code=400, detail="You already claied this drop")
    return crud.get_unclaimed(db, drop.id, claim.wallet)


def already_claimed(db: Session, drop_id: uuid.UUID, wallet: str):
    poap = crud.already_claimed(db, drop_id, wallet)
    return poap != None


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


def get_drop_info(db: Session, drop_id: uuid.UUID):
    drop = get_drop(db, drop_id)
    return schemas.DropInfo(
        name=drop.name,
        description=drop.description,
        image_url=drop.image_url,
        start_date=drop.start_date,
        end_date=drop.end_date,
    )


def get_drop(db: Session, drop_id: uuid.UUID):
    drop = crud.get_drop(db, drop_id)
    if drop == None:
        raise HTTPException(status_code=404, detail="Drop does not exist")
    return drop


def get_claimed_poaps_from_wallet(db: Session, wallet: str):
    poaps: list[models.Poap] = crud.get_all_poaps_from_wallet(db, wallet)
    if len(poaps) == 0:
        return list()
    lst = list()
    for poap in poaps:
        drop: models.Drop = poap.drop
        lst.append(
            schemas.PoapInfo(
                claimed_by=poap.claimed_by,
                claimed_on=poap.claimed_on,
                drop=schemas.DropInfo(
                    name=drop.name,
                    description=drop.description,
                    image_url=drop.image_url,
                    start_date=drop.start_date,
                    end_date=drop.end_date,
                ),
            )
        )
    return lst
