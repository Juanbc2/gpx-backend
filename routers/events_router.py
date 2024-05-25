from fastapi import APIRouter,Depends, HTTPException
from database import models
from schemas import events_schema
from database.database import SessionLocal, engine
from sqlalchemy.orm import Session
from services import events_service

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/events",tags=["events"])
def get_events(db: Session= Depends(get_db)):
    events = events_service.get_events(db=db)
    if events is not None:
        return events
    else:
        raise HTTPException(status_code=404, detail="Events not found")
    


@router.get("/events/{event_id}",tags=["events"])
def get_event(event_id: int,db: Session= Depends(get_db)):
    event = events_service.get_event_by_id(db=db, event_id=event_id)
    if event is not None:
        return event
    else:
        raise HTTPException(status_code=404, detail="Event not found")
    
@router.get("/events/stages/",tags=["events"], response_model=list[events_schema.EventWithStages])
def get_events_with_stages(db: Session= Depends(get_db)):
    events = events_service.get_events_with_stages(db=db)
    if events is not None:
        return events
    else:
        raise HTTPException(status_code=404, detail="Events not found")

@router.post("/events",tags=["events"])
def add_event(event: events_schema.Event,db: Session= Depends(get_db)):
    new_event = events_service.create_event(db=db, event=event)
    if new_event is not None:
        raise HTTPException(status_code=200, detail="Event created successfully")
    else:
        raise HTTPException(status_code=500, detail="Error creating event")
    
@router.delete("/events/{event_id}",tags=["events"])
def delete_event(event_id: int,db: Session= Depends(get_db)):
    event = events_service.delete_event_by_id(db=db, event_id=event_id)
    if event is not None:
        raise HTTPException(status_code=200, detail="Event deleted successfully")
    else:
        raise HTTPException(status_code=500, detail="Error deleting event")