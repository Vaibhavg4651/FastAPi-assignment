from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    username: str
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str

class LinkID(BaseModel):
    user_id: str
    linked_id: str

class Post(BaseModel):
    user_id: str
    title: str
    content: str