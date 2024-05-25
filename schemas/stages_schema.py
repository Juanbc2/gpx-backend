from pydantic import BaseModel
from typing import Optional, List

class Waypoint(BaseModel):
    wpnumber: Optional[int] = None
    latitude: str
    longitude: str
    type: Optional[str] = None
    distance: float
    speed: Optional[float] = None
    penalization: Optional[str] = None
    ratius: Optional[int] = None
    neutralization: Optional[str] = None


class Stage(BaseModel):
    id: Optional[int] = None
    name: str
    eventId : int
    details: str
    stageDate: str 
    waypoints: List[Waypoint]
    categoriesIds: List[int]

class StageWithoutWaypoints(BaseModel):
    id: Optional[int] = None
    name: str
    eventId : int
    details: str
    stageDate: str 
    categoriesIds: list[int]
    



