from schemas import events_schema
from sqlalchemy.orm import Session
from database import models

def get_events(db: Session):
    return db.query(models.Events).all()

def get_event_by_id(db: Session, event_id: int):
    return db.query(models.Events).filter(models.Events.id == event_id).first()

def create_event(db: Session, event: events_schema.Event):
    new_event = models.Events(name=event.name, location=event.location, details=event.details, eventStartDate=event.eventStartDate, eventEndDate=event.eventEndDate)
    db.add(new_event)
    db.commit()
    return new_event

