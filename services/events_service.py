from schemas import events_schema
from sqlalchemy.orm import Session
from database import models
from services import stages_service
import json

def get_events(db: Session):
    events = db.query(models.Events).all()
    for event in events:
        event.categoriesIds = json.loads(event.categoriesIds)
    return events

def get_event_by_id(db: Session, event_id: int):
    event = db.query(models.Events).filter(models.Events.id == event_id).first()
    if event is not None:
        event.categoriesIds = json.loads(event.categoriesIds)
    return event

def get_events_with_stages(db: Session):
    events = db.query(models.Events).all()
    for event in events:
        event.categoriesIds = json.loads(event.categoriesIds)
        event.stages = stages_service.get_stages_by_event(db=db, event_id=event.id)
    return events

def create_event(db: Session, event: events_schema.Event):
    categories_str = json.dumps(event.categoriesIds)
    new_event = models.Events(name=event.name, location=event.location, details=event.details, eventStartDate=event.eventStartDate, eventEndDate=event.eventEndDate, categoriesIds=categories_str)
    db.add(new_event)
    db.commit()
    return new_event

def delete_event_by_id(db: Session, event_id: int):
    event = db.query(models.Events).filter(models.Events.id == event_id).first()
    if event is not None:
        db.delete(event)
        db.commit()
        return True
    return False
