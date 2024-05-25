from pydantic import BaseModel
from typing import Optional

class Competitor(BaseModel):
    id: Optional[int] = None
    name: str
    lastName: str
    number: str
    identification: str

class CompetitorGpx(BaseModel):
    vehicleId: int
    filePath: str
    stageId: int


