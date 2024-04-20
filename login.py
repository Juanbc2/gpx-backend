from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from jose import jwt
import json
from typing import Optional
import bcrypt

router = APIRouter()

SECRET_KEY = "d34391818363cfbd2545e405e4659c16fe2e43aefa160945bdc993353381e4e1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3600


class User(BaseModel):
    username: str
    password: str
    hashed_password: Optional[str] = None

users = []
try:
    with open('./data/usersData.json', 'r') as f:
        json_data = json.load(f)
        if json_data:
            users = json_data
except (FileNotFoundError, json.JSONDecodeError):
    users = []

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

@router.post("/users/register",tags=["users"])
def create_user(user: User):
    hashed_password = password_context.hash(user.password)
    users.append({"username": user.username, "hashed_password": hashed_password})
    with open('./data/usersData.json', 'w') as f:
        json.dump(users, f,indent=4)
    raise HTTPException(status_code=200, detail="User created successfully")

def get_user(username: str):
    for user in users:
        if user["username"] == username:
            return user
    return None

@router.post("/users/login",tags=["users"])
async def login(user: User):
    print(user)
    user_in_db = get_user(user.username)
    if not user_in_db or not verify_password(user.password, user_in_db["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.put("/users/{username}",tags=["users"])
def update_user(username: str, new_data: User):
    for user in users:
        if user["username"] == username:
            hashed_password = password_context.hash(new_data.password)
            user["hashed_password"] = hashed_password
            with open('./data/usersData.json', 'w') as f:
                json.dump(users, f,indent=4)
    raise HTTPException(status_code=200, detail="User updated successfully")
