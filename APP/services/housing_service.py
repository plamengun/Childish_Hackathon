from mariadb import IntegrityError
from hashlib import sha256

from data import database
from data.models import Role, User, HomeType, NumberOfRooms, Attachment, HousePostBody, HousingPostRepr
from common.responses import BadRequest, NoContent


def create(housing_post: HousePostBody, HomeType: str, NumberOfRooms: str, City: str):

    database_data = database.read_query('''SELECT * from home_type where type_name = ?
                                          UNION SELECT id from number_of_rooms where rooms = ?
                                          UNION SELECT id from cities where name =?''', (HomeType, NumberOfRooms, City))

    HomeTypeID, NumberOfRoomsID, CityID = database_data

    generated_id = database.insert_query('INSERT INTO home_posts(city_id, rent_price, description, user_id, home_type_id, number_of_rooms_id) VALUES(?,?,?,?,?,?)',
    (CityID[0], housing_post.rent_price, housing_post.description, 17, HomeTypeID[0], NumberOfRoomsID[0]))


    housing_post.id = generated_id

    return HousingPostRepr(
        id=generated_id,
        city=City,
        rent_price = housing_post.rent_price,
        description=housing_post.description,
        user='17',
        home_type=HomeType,
        number_of_rooms=NumberOfRooms,
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