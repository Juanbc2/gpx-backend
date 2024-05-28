from fastapi import APIRouter,Depends, HTTPException
from database import models
from schemas import stages_schema
from database.database import SessionLocal, engine
from sqlalchemy.orm import Session
from models import stages_model

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/stages",tags=["stages"],response_model=list[stages_schema.Stage])
def get_stages(db : Session = Depends(get_db)):
    stages = stages_model.get_stages(db=db)
    if stages is not None:
        return stages
    else:
        raise HTTPException(status_code=404, detail="stages not found")
    
@router.get("/stages/{stage_id}",tags=["stages"])
def get_stage(stage_id: str,db : Session = Depends(get_db)):
    stage = stages_model.get_stage_by_id(db=db, stage_id=stage_id)
    if stage is not None:
        return stage
    else:
        raise HTTPException(status_code=404, detail="stage not found")
    
@router.post("/stages",tags=["stages"])
def add_stage(stage: stages_schema.Stage,db : Session = Depends(get_db)):
    new_stage = stages_model.create_stage(db=db, stage=stage)
    if new_stage is not None:
        raise HTTPException(status_code=200, detail="stage created successfully")
    else:
        raise HTTPException(status_code=500, detail="Error creating stage")
    
@router.get("/stages/stages_by_event/{event_id}",tags=["stages"],response_model=list[stages_schema.Stage])
def get_stages_by_event(event_id: int,db : Session = Depends(get_db)):
    stages = stages_model.get_stages_by_event(db=db, event_id=event_id)
    if stages is not None:
        return stages
    else:
        raise HTTPException(status_code=404, detail="stages not found")

@router.delete("/stages/{stage_id}",tags=["stages"])
def delete_stage(stage_id: str,db : Session = Depends(get_db)):
    stage = stages_model.delete_stage_by_id(db=db, stage_id=stage_id)
    if stage is not None:
        raise HTTPException(status_code=200, detail="stage deleted successfully")
    else:
        raise HTTPException(status_code=404, detail="stage not found")
    
@router.put("/stages/{stage_id}",tags=["stages"])
def update_stage(stage_id: str,stage: stages_schema.Stage,db : Session = Depends(get_db)):
    stage = stages_model.update_stage_by_id(db=db, stage_id=stage_id, stage=stage)
    if stage is not None:
        raise HTTPException(status_code=200, detail="stage updated successfully")
    else:
        raise HTTPException(status_code=404, detail="stage not found")