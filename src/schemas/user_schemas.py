from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    credits: Optional[int] = 0
    user_type: str = "base"

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
