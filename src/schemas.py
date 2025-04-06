from datetime import date
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class ContactBase(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: EmailStr
    phone: str
    birthday: date | None = None
    additional_data: str | None = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class ContactResponse(ContactBase):
    id: int

    model_config = {"from_attributes": True}

class User(BaseModel):
    id: int
    username: str
    email: str
    avatar: str | None = None

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class RequestEmail(BaseModel):
    email: EmailStr
