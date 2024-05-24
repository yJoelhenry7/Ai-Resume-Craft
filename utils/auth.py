from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.dbhelpers import get_user_by_username

# create your own 16bit random secret key - (openssl rand -hex 16)
SECRET_KEY = "3372e4835885edae8daf1609a1ae7b3c"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user_by_token(db: Session,token: str):
    try:
        payload = jwt.decode(token,SECRET_KEY , algorithms=[ALGORITHM] )
        print(payload)
        username: str = payload.get("sub")
        if username is None:
            return None
        db_user = get_user_by_username(db, username)
        return db_user
    except JWTError:
        return None