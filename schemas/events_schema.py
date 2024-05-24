from pydantic import BaseModel
from typing import Optional
from schemas.stages_schema import StageWithoutWaypoints
class Event(BaseModel):
    id: Optional[int] = None
    name: str
    location: str
    details: str
    eventStartDate: str
    eventEndDate: str
    categoriesIds: list[int]

class EventWithStages(BaseModel):
    id: Optional[int] = None
    name: str
    location: str
    details: str
    eventStartDate: str
    eventEndDate: str
    categoriesIds: list[int]
    stages: list[StageWithoutWaypoints]

