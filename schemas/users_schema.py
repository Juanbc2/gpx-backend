from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    username: str
    hashed_password: str

class Token(BaseModel):
    token: str