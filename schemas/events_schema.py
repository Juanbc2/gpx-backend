from pydantic import BaseModel

class Event(BaseModel):
    name: str
    location: str
    details: str
    eventStartDate: str
    eventEndDate: str