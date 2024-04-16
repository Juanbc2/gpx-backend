from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
import json

router = APIRouter()
stages = []
try:
    with open('./data/stagesData.json', 'r') as f:
        json_data = json.load(f)
        if json_data:
            stages = json_data
except (FileNotFoundError, json.JSONDecodeError):
    stages = []

class Waypoint(BaseModel):
    wpnumber: int
    latitude: str
    longitude: str
    type: Optional[str] = None
    distance: float
    speed: Optional[float] = None
    penalization: Optional[float] = None
    ratius: Optional[int] = None

# stage model
class Stage(BaseModel):
    id: Optional[str] = None
    eventId: str
    categoriesIds: list[int]
    details: str
    stageDate: str
    waypoints: list[Waypoint]


@router.get("/stages",tags=["stages"])
def get_stages():
    try:
        return stages
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error getting stages," + e)

@router.get("/stages/{stage_id}",tags=["stages"])
def get_stage(stage_id: str):
    for stage in stages:
        if str(stage["id"]) == stage_id:
            return stage
    raise HTTPException(status_code=404, detail="Post not found")

@router.post("/stages",tags=["stages"])
def add_stage(stage: Stage):
    try:
        stage.id = str(uuid.uuid4())
        stage_dict = stage.model_dump()
        stages.append(stage_dict) 
        with open('./data/stagesData.json', 'w') as f:
            json.dump(stages, f,indent=4)
        return stages
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error adding stage" + e)

@router.delete("/stages/{stage_id}",tags=["stages"])
def delete_stage(stage_id: str):
    for stage in stages:
        if str(stage["id"]) == stage_id:
            stages.remove(stage)
            with open('./data/stagesData.json', 'w') as f:
                json.dump(stages, f,indent=4)
            return stages
    raise HTTPException(status_code=404, detail="stage not found")