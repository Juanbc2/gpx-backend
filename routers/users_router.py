
from fastapi import APIRouter,Depends, HTTPException
from database import models
from schemas import users_schema
from database.database import SessionLocal, engine
from sqlalchemy.orm import Session
from models import users_model

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/register",response_model= users_schema.UserRegister,
             tags=["users"])
def create_user(user: users_schema.UserLogin,db: Session= Depends(get_db)):
    new_user = users_model.create_user(db=db, user=user)
    if new_user is not None:
        raise HTTPException(status_code=200, detail="User created successfully")
    else:
        raise HTTPException(status_code=500, detail="Error creating user")

@router.post("/users/login",tags=["users"])
def login(user: users_schema.UserLogin,db: Session= Depends(get_db)):
    token = users_model.login(db=db, user=user)
    if token is not False:
        return token
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
@router.get("/users/masterCreated",tags=["users"])
def is_any_user_created(db: Session= Depends(get_db)):
    return users_model.is_any_user_created(db=db)


@router.post("/users/verifyToken",tags=["users"])
def verify_token(token: users_schema.Token):
    return users_model.is_token_expired(token=token.token)


