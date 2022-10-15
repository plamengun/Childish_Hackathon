from mariadb import IntegrityError
from hashlib import sha256

from data import database
from data.models import Role, User, HomeType, HousingPost, NumberOfRooms, Attachment
from common.responses import BadRequest, NoContent


def create(housing_post: HousingPost):
    generated_id = database.insert_query('INSERT INTO home_posts(city_id, rent_price, description, user_id, home_type_id, number_of_rooms_id) VALUES(?,?,?,?,?,?)',
    (housing_post.city_id, housing_post.rent_price, housing_post.description, housing_post.user_id, housing_post.home_type_id, housing_post.number_of_rooms_id))

    housing_post.id = generated_id

    return housing_post



# class HousingPost(BaseModel):
#     id: int | None
#     city_id: int
#     rent_price: int
#     description: str
#     user_id: str
#     home_type_id: int
#     number_of_rooms_id: int

#     attachments: list[Attachment]