from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
import json

router = APIRouter()
events = []
try:
    with open('./data/eventsData.json', 'r') as f:
        json_data = json.load(f)
        if json_data:
            events = json_data
except (FileNotFoundError, json.JSONDecodeError):
    events = []

# event model
class Event(BaseModel):
    id: Optional[str] = None
    name: str
    location: str
    details: Optional[str] = None
    eventStartDate: str
    eventEndDate: str
    stagesIds: Optional[list] = [int]
    categoryIds: list[int]


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
    event.id = str(uuid.uuid4())
    event_dict = event.model_dump()
    events.append(event_dict) 
    with open('./data/eventsData.json', 'w') as f:
        json.dump(events, f,indent=4)
    return events

@router.delete("/events/{event_id}",tags=["events"])
def delete_event(event_id: str):
    for event in events:
        if str(event["id"]) == event_id:
            events.remove(event)
            with open('./data/eventsData.json', 'w') as f:
                json.dump(events, f,indent=4)
            return events
    raise HTTPException(status_code=404, detail="event not found")