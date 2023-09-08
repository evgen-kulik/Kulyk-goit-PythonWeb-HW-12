from datetime import datetime, date
from typing import List
from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    phone_number: str = Field(max_length=20)


class ContactResponse(ContactModel):
    id: int

    class Config:
        orm_mode = True  # вказуємо, що дані повертаються з БД


class UserBase(BaseModel):
    name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    day_of_born: date
    email: EmailStr
    description: str = Field(max_length=250)
    password: str = Field(min_length=6, max_length=350)


class UserModel(UserBase):
    contacts: List[int]


class UserResponse(UserBase):
    id: int
    name: str
    last_name: str
    email: str
    created_at: datetime
    updated_at: datetime
    contacts: List[ContactResponse]

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
