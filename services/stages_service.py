from schemas import stages_schema
from sqlalchemy.orm import Session
from database import models
import json 

def get_stages(db: Session):
    stages = db.query(models.Stages).all()
    for stage in stages:
        stage.waypoints = json.loads(stage.waypoints)
        stage.categoriesIds = json.loads(stage.categoriesIds)
    return stages

def get_stage_by_id(db: Session, stage_id: int):
    stage = db.query(models.Stages).filter(models.Stages.id == stage_id).first()
    if stage is not None:
        stage.waypoints = json.loads(stage.waypoints)
        stage.categoriesIds = json.loads(stage.categoriesIds)
    return stage

def get_stage_waypoints(db: Session, stage_id: int):
    stage = db.query(models.Stages).filter(models.Stages.id == stage_id).first()
    if stage is not None:
        waypoints = json.loads(stage.waypoints)
    return waypoints

def create_stage(db: Session, stage: stages_schema.Stage):
    waypoints_json = json.dumps([waypoint.model_dump() for waypoint in stage.waypoints])
    categories_str = json.dumps(stage.categoriesIds)    
    new_stage = models.Stages(name=stage.name, eventId=stage.eventId, details=stage.details, stageDate=stage.stageDate, waypoints=waypoints_json, categoriesIds=categories_str)
    db.add(new_stage)
    db.commit()
    return new_stage

def get_stages_by_event(db: Session, event_id: int):
    stages = db.query(models.Stages).filter(models.Stages.eventId == event_id).all()
    for stage in stages:
        stage.waypoints = json.loads(str(stage.waypoints))
        stage.categoriesIds = json.loads(str(stage.categoriesIds))
    return stages

def delete_stage_by_id(db: Session, stage_id: int):
    stage = db.query(models.Stages).filter(models.Stages.id == stage_id).first()
    if stage is not None:
        db.delete(stage)
        db.commit()
        return True
    return False

def update_stage_by_id(db: Session, stage_id: int, stage: stages_schema.Stage):
    stage_to_update = db.query(models.Stages).filter(models.Stages.id == stage_id).first()
    if stage_to_update is not None:
        stage_to_update.name = stage.name
        stage_to_update.eventId = stage.eventId
        stage_to_update.details = stage.details
        stage_to_update.stageDate = stage.stageDate
        stage_to_update.waypoints = json.dumps([waypoint.model_dump() for waypoint in stage.waypoints])
        stage_to_update.categoriesIds = json.dumps(stage.categoriesIds)
        db.commit()
        return True
    return False


