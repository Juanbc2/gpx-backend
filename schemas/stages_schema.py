from pydantic import BaseModel
from typing import Optional

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
    name: str
    eventId : int
    details: str
    stageDate: str 
    waypoints: list[Waypoint]
    



