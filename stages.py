from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
from uuid import uuid4 as uuid
import json

router = APIRouter()

f = open("./data/stagesData.json")
json_data = json.load(f)
stages = json_data

class Waypoint(BaseModel):
    wpnumber: int
    latitude: float
    longitude: float
    type: Text
    distance: float
    speed: float
    penalization: str
    ratius: int

# stage model
class Stage(BaseModel):
    id: Optional[str] = str(uuid())
    eventId: str
    categoriesIds: list
    details: str
    stageDate: str
    waypoints: Waypoint


@router.get("/stages",tags=["stages"])
def get_stages():
    return stages

@router.get("/stages/{stage_id}",tags=["stages"])
def get_stage(stage_id: str):
    for stage in stages:
        if str(stage["id"]) == stage_id:
            return stage
    raise HTTPException(status_code=404, detail="Post not found")

@router.post("/stages",tags=["stages"])
def add_stage(stage: Stage):
    stages.append(stage)
    return stages