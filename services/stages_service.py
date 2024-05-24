from schemas import stages_schema
from sqlalchemy.orm import Session
from database import models
import json 

def get_stages(db: Session):
    stages = db.query(models.Stages).all()
    for stage in stages:
        stage.waypoints = json.loads(stage.waypoints)
    return stages

def get_stage_by_id(db: Session, stage_id: int):
    stage = db.query(models.Stages).filter(models.Stages.id == stage_id).first()
    if stage is not None:
        stage.waypoints = json.loads(stage.waypoints)
    return stage

def create_stage(db: Session, stage: stages_schema.Stage):
    waypoints_json = json.dumps([waypoint.model_dump() for waypoint in stage.waypoints])
    new_stage = models.Stages(name=stage.name, eventId=stage.eventId, details=stage.details, stageDate=stage.stageDate, waypoints=waypoints_json)
    db.add(new_stage)
    db.commit()
    return new_stage

def get_stages_by_event(db: Session, event_id: int):
    stages = db.query(models.Stages).filter(models.Stages.eventId == event_id).all()
    for stage in stages:
        stage.waypoints = json.loads(stage.waypoints)
    return stages

def delete_stage_by_id(db: Session, stage_id: int):
    stage = db.query(models.Stages).filter(models.Stages.id == stage_id).first()
    if stage is not None:
        db.delete(stage)
        db.commit()
        return True
    return False


