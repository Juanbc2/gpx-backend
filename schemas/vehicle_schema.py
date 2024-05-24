from pydantic import BaseModel
from typing import Optional
from schemas.competitors_schema import Competitor

class Vehicle(BaseModel):
    id: Optional[int] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    plate: Optional[str] = None
    securePolicy: Optional[str] = None
    competitorId: int

class VehicleWithCompetitor(BaseModel):
    id: Optional[int] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    plate: Optional[str] = None
    securePolicy: Optional[str] = None
    competitorId: int
    competitor: Competitor