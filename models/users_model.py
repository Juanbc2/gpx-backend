from schemas import users_schema
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError
import bcrypt
from database import models
from datetime import datetime, timezone

SECRET_KEY = "d34391818363cfbd2545e405e4659c16fe2e43aefa160945bdc993353381e4e1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

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

def is_any_user_created(db: Session):
    return db.query(models.Users).first() is not None


def is_token_expired(token: str):
    try:
        # Decodificar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Obtener la fecha de expiración del token
        expire = payload.get('exp')
        
        # Si no hay fecha de expiración, el token no está expirado
        if expire is None:
            return False
        
        # Comprobar si la fecha de expiración es anterior a la fecha actual
        if datetime.now(timezone.utc) > datetime.fromtimestamp(expire, timezone.utc):
            return True
        else:
            return False
    except JWTError:
        # Si hay un error al decodificar el token, asumimos que está expirado
        return True



