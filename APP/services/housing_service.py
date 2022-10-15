from mariadb import IntegrityError
from hashlib import sha256

from data import database
from data.models import HousePostBody, HousingPostRepr
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