from sqlalchemy.orm import Session
import models.models as models, models.schemas as schemas
import uuid


def create_store(db: Session, store: schemas.StoreCreate):
    store = models.Store(
        name=store.name, description=store.description, geohash=store.geohash
    )
    db.add(store)
    db.commit()
    db.refresh(store)
    return store


def create_drop(db: Session, drop: schemas.DropCreate):
    drop = models.Drop(
        name=drop.name,
        description=drop.description,
        store_id=drop.store_id,
        image_url=drop.image_url,
    )
    db.add(drop)
    db.commit()
    db.refresh(drop)
    return drop


def already_claimed(db: Session, drop_id: uuid.UUID, wallet: str):
    poap = db.query(models.Poap).filter_by(drop_id=drop_id, claimed_by=wallet).first()
    print(poap)
    return poap


def get_all_poaps(db: Session, drop_id: uuid.UUID):
    return db.query(models.Poap).filter_by(drop_id=drop_id).all()


def get_drop(db: Session, drop_id: uuid.UUID):
    return db.query(models.Drop).filter_by(id=drop_id).first()


def get_unclaimed(db: Session, drop_id: uuid.UUID, wallet: str):
    poap = db.query(models.Poap).filter_by(drop_id=drop_id, claimed_by=None).first()
    if poap == None:
        return poap
    poap.claimed_by = wallet
    db.add(poap)
    db.commit()
    db.refresh(poap)
    return poap


def get_store(db: Session, store_id: uuid.UUID):
    return db.query(models.Store).filter_by(id=store_id).first()


def create_poap(db: Session, drop_id: uuid.UUID, poap: schemas.PoapCreate):
    poap = models.Poap(url=poap.url, drop_id=drop_id)
    db.add(poap)
    db.commit()
    db.refresh(poap)
    return poap
