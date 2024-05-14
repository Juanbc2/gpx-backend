from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
import json
from validations import Validations

router = APIRouter()
competitors = []
stages = []
try:
    with open('./data/competitorsData.json', 'r') as f:
        json_data = json.load(f)
        if json_data:
            competitors = json_data
except (FileNotFoundError, json.JSONDecodeError):
    competitors = []

try:
    with open('./data/stagesData.json', 'r') as f:
        json_data = json.load(f)
        if json_data:
            stages = json_data
except (FileNotFoundError, json.JSONDecodeError):
    stages = []

class Vehicle(BaseModel):
    brand: str
    model: str
    categoryId: int
    plate: str
    securePolicy: str

# competitor model
class Competitor(BaseModel):
    id: Optional[str] = None
    name: str
    lastName: str
    number: str
    identification: str
    vehicle: Vehicle
    currentStagesIds: list[int]
    pastStagesIds: list[int]

class CompetitorGpx(BaseModel):
    competitorId: str
    filePath: str
    stageId: str


@router.get("/competitors",tags=["competitors"])
def get_competitors():
    try:
        return competitors
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error getting competitors," + e)

@router.get("/competitors/{competitor_id}",tags=["competitors"])
def get_competitor(competitor_id: str):
    for competitor in competitors:
        if str(competitor["id"]) == competitor_id:
            return competitor
    raise HTTPException(status_code=404, detail="Post not found")

@router.post("/competitors",tags=["competitors"])
def add_competitor(competitor: Competitor):
    try:
        competitor.id = str(uuid.uuid4())
        competitor_dict = competitor.model_dump()
        competitors.append(competitor_dict) 
        with open('./data/competitorsData.json', 'w') as f:
            json.dump(competitors, f,indent=4)
        return competitors
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error adding competitor" + e)

@router.delete("/competitors/{competitor_id}",tags=["competitors"])
def delete_competitor(competitor_id: str):
    for competitor in competitors:
        if str(competitor["id"]) == competitor_id:
            competitors.remove(competitor)
            with open('./data/competitorsData.json', 'w') as f:
                json.dump(competitors, f,indent=4)
            return competitors
    raise HTTPException(status_code=404, detail="competitor not found")

@router.put("/competitors/{competitor_id}",tags=["competitors"])
def update_competitor(competitor_id: str, competitor: Competitor):
    for competitor in competitors:
        if str(competitor["id"]) == competitor_id:
            competitor = competitor
            with open('./data/competitorsData.json', 'w') as f:
                json.dump(competitors, f,indent=4)
            return competitors
    raise HTTPException(status_code=404, detail="competitor not found")

# Post competition .gpx file path
@router.post("/competitors/gpx",tags=["competitors"])
def post_gpx_file(competitorGpx: CompetitorGpx):
    for competitor in competitors:
        if str(competitor["id"]) == competitorGpx.competitorId:
            if competitorGpx.stageId not in competitor["currentStagesIds"]:
                competitor["currentStagesIds"].append(competitorGpx.stageId)
            with open('./data/competitorsData.json', 'w') as f:
                json.dump(competitors, f,indent=4)
            for stage in stages:
                if str(stage["id"]) == competitorGpx.stageId:
                    # logica para comparar waypoints y gpx file
                    validations_i = Validations()
                    route = competitorGpx.filePath.replace("\\", "/")
                    validationResult = validations_i.validations(stage, route)
                    return validationResult
    raise HTTPException(status_code=404, detail="competitor not found")

