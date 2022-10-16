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
        SELECT h.id, c.name, h.rent_price, h.description, u.id, u.username, ht.type_name, r.rooms
        FROM home_posts h
        JOIN users u ON h.user_id = u.id
        JOIN cities c ON h.city_id = c.id
        JOIN home_type ht ON h.home_type_id = ht.id
        JOIN number_of_rooms r ON h.number_of_rooms_id = r.id
        WHERE h.id = ?''', (id,))
    return HousingPostRepr.from_query_result(*data)


def update_housing_post(housing_post_id: int, payload: HousePostBody):
    database.update_query('''
        UPDATE home_post SET city_id = ?, rent_price = ?, description = ?, home_type_id = ?, number_of_rooms_id = ? 
        WHERE id = ?''', (payload.city_id, payload.rent_price, payload.description, payload.home_type_id, payload.number_of_rooms_id))
    
    return create_housing_repr(id=housing_post_id)


# def all(city_id: str| None, home_type_id: str|None, number_of_rooms_id: str| None, search: str | None):
#     if search:
#         data = database.read_query('''SELECT h.id, c.name, h.rent_price, h.description, u.id, u.username, ht.type_name, r.rooms
#         FROM home_posts h
#         JOIN users u ON h.user_id = u.id
#         JOIN cities c ON h.city_id = c.id
#         JOIN home_type ht ON h.home_type_id = ht.id
#         JOIN number_of_rooms r ON h.number_of_rooms_id = r.id
#         WHERE j.city_id = ? AND j.job_sectors_id = ? AND j.employment_type_id = ? AND h.description LIKE ?
#         ORDER BY h.id''', (f'%{search}%',))
#     else:
#         data = database.read_query('''SELECT h.id, c.name, h.rent_price, h.description, u.id, u.username, ht.type_name, r.rooms
#         FROM home_posts h
#         JOIN users u ON h.user_id = u.id
#         JOIN cities c ON h.city_id = c.id
#         JOIN home_type ht ON h.home_type_id = ht.id
#         JOIN number_of_rooms r ON h.number_of_rooms_id = r.id
#         ORDER BY h.id''')
#     return [HousingPostRepr.from_query_result(*row) for row in data]


def all(city_id: str| None, home_type_id: str|None, number_of_rooms_id: str| None, search: str | None, limit: int, offset: int):
    if search:
        data = database.read_query('''
            SELECT id, city_id, rent_price, description, user_id, home_type_id, number_of_rooms_id
            FROM home_posts
            WHERE description LIKE ?
            LIMIT ? OFFSET ?''', (f'%{search}%', limit, offset))
    else:
        data = database.read_query('''
            SELECT id, city_id, rent_price, description, user_id, home_type_id, number_of_rooms_id
            FROM home_posts
            LIMIT ? OFFSET ?''', (limit, offset))
    return [HousingPostRepr.from_query_result(*row) for row in data]