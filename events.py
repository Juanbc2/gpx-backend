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
    stages: Optional[list] = []
    categoryIds: list[int]


@router.get("/events",tags=["events"])
def get_events():
    try:
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error getting events,"+str(e))


@router.get("/events/{event_id}",tags=["events"])
def get_event(event_id: str):
    for event in events:
        if str(event["id"]) == event_id:
            return event
    raise HTTPException(status_code=404, detail="Event not found")

@router.post("/events",tags=["events"])
def add_event(event: Event):
    try:
        event.id = str(uuid.uuid4())
        event_dict = event.model_dump()
        events.append(event_dict) 
        with open('./data/eventsData.json', 'w') as f:
            json.dump(events, f,indent=4)
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error adding event"+str(e))
    

@router.delete("/events/{event_id}",tags=["events"])
def delete_event(event_id: str):
    for event in events:
        if str(event["id"]) == event_id:
            events.remove(event)
            with open('./data/eventsData.json', 'w') as f:
                json.dump(events, f,indent=4)
            return events
    raise HTTPException(status_code=404, detail="event not found")

def add_event_stage(event_id: str, stage_id: str,stage_details: str):
    for event in events:
        if str(event["id"]) == event_id:
            event["stages"].append({"stageId":stage_id, "stageDetails":stage_details})
            with open('./data/eventsData.json', 'w') as f:
                json.dump(events, f,indent=4)
            return event
    raise HTTPException(status_code=404, detail="event not found")