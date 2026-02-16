from fastapi import FastAPI, Depends, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
from db import engine, SessionLocal
import storage
import uuid

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def read_health():
    return {"status": "ok"}

@app.post("/assets")
def create_asset(db: Session = Depends(get_db)):
    db_asset = models.Asset(status="CREATED")
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return {"asset_id": str(db_asset.id)}

@app.post("/assets/{asset_id}/upload")
async def upload_asset(asset_id: uuid.UUID, file: UploadFile = File(...), db: Session = Depends(get_db)):
    db_asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    file_content = await file.read()
    object_name = f"{asset_id}/{file.filename}"
    
    storage.upload_file(file_content, object_name)
    
    db_asset.storage_path = object_name
    db_asset.status = "UPLOADED"
    db_asset.filename = file.filename
    
    db.commit()
    db.refresh(db_asset)
    
    return {"status": "success", "storage_path": object_name}
