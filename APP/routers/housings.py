from fastapi import APIRouter, Header
from common.auth import get_user_or_raise_401, create_token
from common.responses import BadRequest, Forbidden, NotFound
from data.models import HousingPostRepr, Tags, HousePostBody
from services import housing_service
from services import user_service


housing_router = APIRouter(prefix='/housings')



@housing_router.post('/', response_model=HousingPostRepr, tags=[Tags.housings])
def create_housing_post(data: HousePostBody, token = Header()):
    
    user = get_user_or_raise_401(token)
    if user_service.get_user_type(user.id) != 'landlord':
        return BadRequest('User is not an landlord')
    data.user_id = user.id
    housing_post = housing_service.create(data)
    return housing_post




@housing_router.get('/')
def get_housing_posts(sort:str | None,
                        search: str | None,
                        x_token: str | None = Header(default=None)):

    pass