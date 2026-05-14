
from pydantic import BaseModel

class UserSchema(BaseModel):
    name:str
    username:str
    password:str
    email:str
    user_role:str

class UserResponseSchema(BaseModel):
    name:str
    username:str
    email:str
    id:int
    user_role:str

class LoginSchema(BaseModel):
    username:str
    password:str