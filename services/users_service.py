from schemas import users_schema
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
import bcrypt
from database import models

SECRET_KEY = "d34391818363cfbd2545e405e4659c16fe2e43aefa160945bdc993353381e4e1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3600

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

def create_user(db: Session,user: users_schema.UserRegister):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    new_user = models.Users(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    return new_user

def login(db: Session,user: users_schema.UserLogin):
    user_in_db = db.query(models.Users).filter(models.Users.username == user.username).first()
    if not user_in_db or not verify_password(user.password, user_in_db.hashed_password):
        return False
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

