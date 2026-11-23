from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict, Field

class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
