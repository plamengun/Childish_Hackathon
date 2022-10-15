from mariadb import IntegrityError
from hashlib import sha256

from data import database
from data.models import HousePostBody, HousingPostRepr
from common.responses import BadRequest, NoContent


def create(housing_post: HousePostBody):


    generated_id = database.insert_query('INSERT INTO home_posts(city_id, rent_price, description, user_id, home_type_id, number_of_rooms_id) VALUES(?,?,?,?,?,?)',
    (housing_post.city_id, housing_post.rent_price, housing_post.description, 17, housing_post.home_type_id, housing_post.number_of_rooms_id))


    return HousingPostRepr(
        id=generated_id,
        city_id=int(housing_post.city_id),
        rent_price = housing_post.rent_price,
        description=housing_post.description,
        user_id=17,
        home_type_id=int(housing_post.home_type_id),
        number_of_rooms_id=int(housing_post.number_of_rooms_id),
        attachments=[]
    )



# class HousingPost(BaseModel):
#     id: int | None
#     city_id: int
#     rent_price: int
#     description: str
#     user_id: str
#     home_type_id: int
#     number_of_rooms_id: int

#     attachments: list[Attachment]

# class HousingPostRepr(BaseModel):
#     id: int
#     city: str
#     rent_price: int
#     description: str
#     user: str
#     home_type: str
#     number_of_rooms: str

#     attachments: list[Attachment]

def all(search):
    if search:
        data = database.read_query('''SELECT id, city, rent_price, description, user, home_type, number_of_rooms WHERE description LIKE ? ORDER BY id''', (f'%{search}%',))
    else:
        data = data = database.read_query('''SELECT id, city, rent_price, description, user, home_type, number_of_rooms ORDER BY id''')
    return [HousingPostRepr(id=id, city=city, rent_price=rent_price, description=description, user=user, home_type=home_type, number_of_rooms=number_of_rooms) for 
    id, city, rent_price, description, user, home_type, number_of_rooms in data]