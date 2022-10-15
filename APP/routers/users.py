from fastapi import APIRouter, Header

from common.auth import get_user_or_raise_401, create_token
from common.responses import BadRequest, Forbidden, NotFound, Unauthorized
from data.models import CompanyInfoBody, Tags, LoginData, Token, User, UserAttributesBody, UserResponseModel, UserTypes, UserUpdated
from services import user_service


users_router = APIRouter(prefix='/users')


@users_router.get('/info', response_model=UserResponseModel, tags=[Tags.users])
def user_info(token: str = Header()):
    user = get_user_or_raise_401(token)

    if user:
        return UserResponseModel(id=user.id, username=user.username)


@users_router.get('/{id}', response_model=UserResponseModel, tags=[Tags.users])
def get_user_by_id(id: int, token: str = Header()):
    user = get_user_or_raise_401(token)

    if user.id == id:
        return UserResponseModel(id=user.id, username=user.username)

    return Unauthorized(content='Not valid authentication credentials')


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


@users_router.put('/{id}', response_model=UserUpdated, tags=[Tags.users])
def add_user_info(id: int, payload: UserAttributesBody, token: str = Header()):
    user = get_user_or_raise_401(token)

    if user.id == id:
        result = user_service.update_user_info(user, payload)

        return result or BadRequest(f'A user with that email address already exists.')

    #logged-in user is not the user with the {id} - path param
    return Unauthorized(content='Not valid authentication credentials')


@users_router.put('/{id}/company', response_model=UserUpdated, tags=[Tags.users])
def add_company_info(id: int, payload: CompanyInfoBody, token: str = Header()):
    user = get_user_or_raise_401(token)

    if user.id == id:
        type = user_service.get_user_type(user.id)
        if type == 'employer' or type == 'landlord':
            result = user_service.create_company_info(user, payload)

            return result or BadRequest(f'Company info database constraint is violated')

        return BadRequest(content='Employer/Landlord endpoint')

    #logged-in user is not the user with the {id} - path param
    return Unauthorized(content='Not valid authentication credentials')