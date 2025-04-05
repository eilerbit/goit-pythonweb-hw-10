from datetime import date
from pydantic import BaseModel, EmailStr, Field

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
