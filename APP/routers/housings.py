from fastapi import APIRouter, Header

from common.auth import get_user_or_raise_401, create_token
from common.responses import BadRequest, Forbidden, NotFound
from data.models import HousingPost, Tags, LoginData, Token, User
from services import housing_service


housing_router = APIRouter(prefix='/housings')


# @users_router.post('/register', response_model=User, tags=[Tags.users])
# def register(data: LoginData):
#     user = user_service.create(data.username, data.password)

#     return user or BadRequest(f'Username {data.username} is taken')


@housing_router.post('/', response_model=HousingPost)
def crate_housing_post():
    pass