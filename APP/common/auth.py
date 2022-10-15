import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status

from data.models import Token, User
from services.user_service import find_by_username
from data.database import read_query

ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = 'secret'
# HS256 Signing Algorithm
ALGORITHM = 'HS256'


def create_token(user: User):
    to_encode = {'sub': user.username}
    # issued_at = datetime.utcnow()
    # to_encode.update({"iat": issued_at})

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return Token(token=encoded)


def from_token(token: str) -> User | None:
    return find_by_username(decode_username_from_token(token))


def is_authenticated(token: str) -> bool:
    username = decode_username_from_token(token)
    data = read_query(
        '''SELECT id, username FROM users WHERE username =  ?''', (username,))

    return bool(data)


def decode_username_from_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
    except jwt.exceptions.ExpiredSignatureError:
        #Raised when a token’s exp claim indicates that it has expired
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Your session has expired")
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials")

    return username
    
def get_user_or_raise_401(token: str) -> User:
    if not is_authenticated(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials")

    return from_token(token)