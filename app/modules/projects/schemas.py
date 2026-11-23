from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class ProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: str | None = None

class ProjectOut(BaseModel):
    id: int
    name: str
    description: str | None
    owner_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
