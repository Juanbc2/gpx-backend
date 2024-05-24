from pydantic import BaseModel
from typing import Optional

class Competitor(BaseModel):
    id: Optional[int] = None
    name: str
    lastName: str
    number: str
    identification: str

class CompetitorGpx(BaseModel):
    vehicleId: str
    filePath: str
    stageId: str

class CompetitorGpxResult(BaseModel):
    penaltieTime: str
    routeTime: str
    penalties: list[str]
    route: list[str]


