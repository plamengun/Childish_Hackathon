from fastapi import APIRouter, Header
from common.auth import get_user_or_raise_401, create_token
from common.responses import BadRequest, Forbidden, NotFound
from data.models import HomeType, HousingPostRepr, NumberOfRooms, Tags, HousePostBody, Cities
from services import housing_service
from services import user_service


housing_router = APIRouter(prefix='/v1/housings')



@housing_router.post('/', response_model=HousingPostRepr, tags=[Tags.housings])
def create_housing_post(data: HousePostBody, token = Header()):
    
    user = get_user_or_raise_401(token)
    if user_service.get_user_type(user.id) != 'landlord':
        return BadRequest('User is not an landlord')
    data.user_id = user.id
    housing_post = housing_service.create(data)
    return housing_post


@housing_router.put('/{id}', response_model=HousingPostRepr, tags=[Tags.housings])
def update_housing_post(id: int, payload: HousePostBody, token = Header()):
    
    user = get_user_or_raise_401(token)
    if user_service.get_user_type(user.id) != 'landlord':
        return BadRequest('User is not an landlord')
    
    housing_post = housing_service.update_housing_post(id, payload)
    return housing_post or BadRequest(content='Database constrains are violated')


@housing_router.get('/', tags = [Tags.housings])
def get_housing_posts(city_id: Cities | None = None, home_type_id: HomeType | None = None, number_of_rooms_id: NumberOfRooms | None = None, search: str | None = None, limit: int = 10, offset: int = 0 ):
    housing_ads = housing_service.all(city_id, home_type_id, number_of_rooms_id, search, limit, offset)
    return housing_ads