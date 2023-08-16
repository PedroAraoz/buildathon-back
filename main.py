from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import crud, models.models as models, models.schemas as schemas
from conf.database import SessionLocal, engine
import uuid
import service


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


@app.post("/store", response_model=schemas.Store)
def create_store(store: schemas.StoreCreate, db: Session = Depends(get_db)):
    return crud.create_store(db=db, store=store)


@app.post("/drop", response_model=schemas.Drop)
def create_drop(drop: schemas.DropCreate, db: Session = Depends(get_db)):
    return crud.create_drop(db=db, drop=drop)


@app.post("/drop/{drop_id}/poap", response_model=schemas.Poap)
def create_poap(
    drop_id: uuid.UUID,
    poap: schemas.PoapCreate,
    db: Session = Depends(get_db),
):
    return crud.create_poap(db=db, drop_id=drop_id, poap=poap)


@app.get("/drop/{drop_id}/poap", response_model=list[schemas.Poap])
def get_all_poaps(drop_id: uuid.UUID, db: Session = Depends(get_db)):
    return crud.get_all_poaps(db, drop_id)

@app.get("/drop/{drop_id}", response_model=schemas.Drop)
def get_drop(drop_id: uuid.UUID, db: Session = Depends(get_db)):
    return crud.get_drop(db, drop_id)


@app.post("/drop/{drop_id}/claim", response_model=schemas.Poap)
def claim_poap(drop_id: uuid.UUID, claim: schemas.ClaimDrop, db: Session = Depends(get_db)):
    poap = service.get_unclaimed(db, drop_id=drop_id, claim=claim)
    if poap == None:
        raise HTTPException(status_code=404, detail="No more poaps")
    return poap