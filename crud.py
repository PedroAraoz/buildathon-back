from sqlalchemy.orm import Session
import models.models as models, models.schemas as schemas
import uuid


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_store(db: Session, store: schemas.StoreCreate):
    store = models.Store(name=store.name, description=store.description)
    db.add(store)
    db.commit()
    db.refresh(store)
    return store


def create_drop(db: Session, drop: schemas.DropCreate):
    drop = models.Drop(name=drop.name, description=drop.description, store_id=drop.store_id)
    db.add(drop)
    db.commit()
    db.refresh(drop)
    return drop


def get_all_poaps(db: Session, drop_id: uuid.UUID):
    return db.query(models.Poap).filter_by(drop_id=drop_id).all()


def get_drop(db: Session, drop_id: uuid.UUID):
    return db.query(models.Drop).filter_by(id=drop_id).first()

def get_unclaimed(db: Session, drop_id: uuid.UUID, coords: schemas.Coordinates):
    drop = get_drop(db, drop_id)
    # todo implement
    return db.query(models.Poap).filter_by(drop_id=drop_id, claimed_by=None).first()


def create_poap(db: Session, drop_id: uuid.UUID, poap: schemas.PoapCreate):
    poap = models.Poap(url=poap.url, drop_id=drop_id)
    db.add(poap)
    db.commit()
    db.refresh(poap)
    return poap


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
