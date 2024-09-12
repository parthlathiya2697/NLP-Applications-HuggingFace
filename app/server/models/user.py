from typing import Optional, List, Dict, Set
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, validator
from fastapi import Form

class TypeChoices(Enum):
    normal = 'normal'
    google = 'google'
    facebook = 'facebook'

class AccountModel(BaseModel):
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    password: str = Field(...)
    image_url: Optional[str] = None
    type: TypeChoices
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False
    is_staff: Optional[bool] = True
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    @validator('phone')
    def contact_check(cls, v, **kwargs):
        # try:
        #     code, number = v.split('-')
        # except:
        #     raise ValueError('Please fill contact detail in the correct formate')
        if not (v.isdecimal() and len(v) >= 10):
            raise ValueError('Please enter correct contact number')
        return v

class UpdateAccount(BaseModel):
    acts: List[str]
    lat: str
    long: str
    connections: List[str]
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class ProfileModel(BaseModel):
    full_name: str = Field(...)
    email: str = Field(...)
    phone: Optional[str] = None
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    @classmethod
    def as_form(cls, full_name: str = Form(...), email: str = Form(...), phone: Optional[str] = Form(None)):
        return cls(full_name=full_name, email=email, phone=phone)

    @validator('phone')
    def contact_check(cls, v, **kwargs):
        # try:
        #     code, number = v.split('-')
        # except:
        #     raise ValueError('Please fill contact detail in the correct formate')
        if v is not None and not (v.isdecimal() and len(v) >= 10):
            raise ValueError('Please enter correct contact number')
        return v

    class Config:
        schema_extra = {
            "example": {
                "full_name": "John Doe",
                "email": "jdoe@x.edu.ng",
                "phone": "91-9999999999",
            }
        }

class AccountCreatedModel(BaseModel):
    created_at: datetime
    updated_at: datetime

class ProfileUpdateModel(BaseModel):
    full_name: Optional[str]
    email: Optional[str]
    contact: Optional[str]
    birth_date: Optional[str]
    lat: str
    long: str

    class Config:
        schema_extra = {
            "example": {
                "full_name": "John Doe",
                "email": "jdoe@x.edu.ng",
                "contact": "91-9999999999",
                "birth_date": "2001-07-25",
                "let": "36.2234",
                "long": "67.432",
            }
        }

# this is to add fried list to user
class ConnectionModel(BaseModel):
    connections: List[str] = None
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "connections": []
            }
        }

class LoginModel(BaseModel):
    username: str
    password: Optional[str]
    last_login: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "username": "jon@doe.jn.in",
                "password": "password@demo1212",
            }
        }

class BindActivities(BaseModel):
    acts: List[str]
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "acts": ["61417359dc6eefe022f44fd2", "61417359dc6eefe022f44fd7"]
            }
        }

class AccessChoices(Enum):
    everyone = "everyone"
    only_friends = "only_friends"
    no_one = "no_one"

class PrivacyModel(BaseModel):
    profile_access: AccessChoices
    friend_access: AccessChoices
    acts_access: AccessChoices
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


    class Config:
        schema_extra = {
            "example": {
                "profile_access": 0,
                "friend_access": 0,
                "acts_access": 0
            }
        }

class Chatname(BaseModel):
    chatname: str



