from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import crud, models.models as models, models.schemas as schemas
from conf.database import SessionLocal, engine
import uuid
import service
from geolib import geohash
from datetime import date, timedelta

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    s1 = crud.create_store(
        db,
        schemas.StoreCreate(
            name="Store 1",
            geohash=geohash.encode(1, 1, 25),
        ),
    )
    s2 = crud.create_store(
        db,
        schemas.StoreCreate(
            name="Store 2",
            geohash=geohash.encode(-1.004, 0.002, 25),
        ),
    )

    d1 = crud.create_drop(
        db,
        schemas.DropCreate(
            name="Drop 1",
            description="woooow!",
            store_id=s1.id,
            image_url="somelink.com",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
        ),
    )
    d2 = crud.create_drop(
        db,
        schemas.DropCreate(
            name="Drop 2",
            description="so fun!",
            store_id=s2.id,
            image_url="somelink.com",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
        ),
    )

    for i in range(20):
        crud.create_poap(
            db, d1.id, schemas.PoapCreate(url="http://poap-d1-" + str(i) + ".com")
        )
        crud.create_poap(
            db, d2.id, schemas.PoapCreate(url="http://poap-d2-" + str(i) + ".com")
        )


@app.get("/drop/{drop_id}", response_model=schemas.DropInfo)
def get_drop(drop_id: uuid.UUID, db: Session = Depends(get_db)):
    return service.get_drop_info(db, drop_id)


@app.post("/drop/{drop_id}/claim", response_model=schemas.Poap)
def claim_poap(
    drop_id: uuid.UUID, claim: schemas.ClaimDrop, db: Session = Depends(get_db)
):
    poap = service.get_unclaimed(db, drop_id=drop_id, claim=claim)
    if poap == None:
        raise HTTPException(status_code=404, detail="No more poaps")
    return poap

@app.get("/collection", response_model=list[schemas.PoapInfo])
def get_claimed_poaps_from_wallet(wallet: str, db: Session = Depends(get_db)):
    return service.get_claimed_poaps_from_wallet(db, wallet)