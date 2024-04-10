from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import uuid4 as uuid
import json

router = APIRouter()

f = open("./data/eventsData.json")
json_data = json.load(f)
events = json_data

# event model
class Event(BaseModel):
    id: Optional[str] = str(uuid())
    name: str
    location: str
    eventStartDate: datetime
    eventEndDate: datetime
    stagesIds: list
    categoryIds: list
    created_at: Optional[datetime] = datetime.now()



# @app.get("/")
# def read_root():
#     return {"welcome": "my first fastapi"}

@router.get("/events",tags=["events"])
def get_events():
    return events

@router.get("/events/{event_id}",tags=["events"])
def get_event(event_id: str):
    for event in events:
        if str(event["id"]) == event_id:
            return event
    raise HTTPException(status_code=404, detail="Post not found")

@router.post("/events",tags=["events"])
def add_event(event: Event):
    events.append(event)
    return events