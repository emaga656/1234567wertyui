from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=160)
    description: str | None = None

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=160)
    description: str | None = None
    status: str | None = None

class TaskOut(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    project_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
