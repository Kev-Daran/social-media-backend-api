from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET = "5MYVjL3tVDMjBFlKOSt5lYzVM1KTF8oq"
ALGORITHM = "HS256"
TIME_TO_EXPIRE = 30

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=TIME_TO_EXPIRE)
    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token : str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET, ALGORITHM)

        id : str = payload.get("user_id")

        if id is None:
            raise credentials_exception
    
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception
    
    return token_data
    

def get_current_user(token : str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials", headers={"WWW-Authenticate" : "Bearer"})

    return verify_access_token(token, credentials_exception)