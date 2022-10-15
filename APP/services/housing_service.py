from mariadb import IntegrityError
from hashlib import sha256

from data import database
from data.models import HousePostBody, HousingPostRepr
from common.responses import BadRequest, NoContent


def create(housing_post: HousePostBody):

    generated_id = database.insert_query('INSERT INTO home_posts(city_id, rent_price, description, user_id, home_type_id, number_of_rooms_id) VALUES(?,?,?,?,?,?)',
    (housing_post.city_id, housing_post.rent_price, housing_post.description, housing_post.user_id, housing_post.home_type_id, housing_post.number_of_rooms_id))

    return create_housing_repr(generated_id)


def create_housing_repr(id: int):
    data = database.read_query_one('''
        SELECT h.id, c.name, h.rent_price, h.description, u.username, ht.type_name, r.rooms, attachments
        FROM home_posts h
        JOIN users u ON h.user_id = u.id
        JOIN cities c ON h.city_id = c.id
        JOIN home_type ht ON h.home_type_id = ht.id
        JOIN number_of_rooms r ON h.number_of_rooms_id = r.id
        WHERE h.id = ?''', (id,))
    return HousingPostRepr.from_query_result(*data)


def all(search):
    if search:
        data = database.read_query('''SELECT id, city, r
        ent_price, description, user, home_type, number_of_rooms WHERE description LIKE ? ORDER BY id''', (f'%{search}%',))
    else:
        data = database.read_query('''SELECT id, city, rent_price, description, user, home_type, number_of_rooms ORDER BY id''')
    return HousingPostRepr.from_query_result(*data)