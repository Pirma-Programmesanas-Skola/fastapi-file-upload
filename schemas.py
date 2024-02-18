from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Object(BaseModel):
    owner: str
    file_name: str
    upload_date: datetime
    preview_link: Optional[str] = None

class ObjectCreate(BaseModel):
    file_name: str
