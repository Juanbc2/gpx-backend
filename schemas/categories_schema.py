from pydantic import BaseModel
from typing import Optional

class Category(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    