from fastapi import APIRouter, Header

from common.auth import get_user_or_raise_401, create_token
from common.responses import BadRequest, Forbidden, NotFound
from data.models import Tags, LoginData, Token, User, UserResponseModel, UserTypes
from services import user_service


users_router = APIRouter(prefix='/users')


@users_router.post('/login', response_model=Token, tags=[Tags.users])
def login(data: LoginData):
    user = user_service.try_login(data.username, data.password)
    if user: 
        return create_token(user)
    else:
        return BadRequest(content='Invalid login data')


@users_router.post('/register', response_model=User, tags=[Tags.users])
def register(data: LoginData, q: UserTypes = UserTypes.normal):
    user = user_service.create(data.username, data.password, user_type_id=int(q))

    return user or BadRequest(f'Username {data.username} is taken')


@users_router.get('/info', response_model=UserResponseModel, tags=[Tags.users])
def user_info(token: str = Header()):
    user = get_user_or_raise_401(token)

    if user:
        return UserResponseModel(id=user.id, username=user.username)