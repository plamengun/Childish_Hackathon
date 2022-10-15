from mariadb import IntegrityError
from hashlib import sha256

from data import database
from data.models import CompanyInfoBody, Role, User, UserAttributesBody, UserResponseModel, UserUpdated
from common.responses import BadRequest, NoContent

ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = 'teleriktigers'
ALGORITHM = 'HS256' # HS256 Signing Algorithm


def find_by_username(username: str) -> User | None:
    data = database.read_query(
        'SELECT id, username, password FROM users WHERE username = ?',
        (username,)
    )

    return next((User.from_query_result(*row) for row in data), None)


def find_by_id(user_id: int) -> UserUpdated | None:
    data = database.read_query(
        'SELECT id, username, city_id, email, phone_number, firstname, lastname, company_info_id FROM users WHERE id = ?',
        (user_id,)
    )

    return next((UserUpdated.from_query_result(*row) for row in data), None)
 


def get_user_type(user_id: int):
    type = database.read_query_one('''
        SELECT t.name FROM types t
        JOIN user_types u ON t.id = u.type_id
        WHERE u.user_id = ?''', (user_id,))

    return type[0]


def try_login(username: str, password: str) -> User | None:
    user = find_by_username(username)

    return user if (user and user.password == _hash_password(password)) else None


def create(username: str, password: str, user_type_id: int) -> User | None:
    try:
        generated_id = database.insert_query(
            'INSERT INTO users(username, password) VALUES (?,?)',
            (username, _hash_password(password))
        )
        database.insert_query(
            'INSERT INTO user_types (user_id, type_id) VALUES (?,?)',
            (generated_id, user_type_id)
        )

        return User(id=generated_id, username=username)

    except IntegrityError:
        # mariadb raises this error when a constraint is violated
        # in that case we have duplicate usernames
        return None


def update_user_info(user: User, payload: UserAttributesBody) -> UserUpdated:
    try:
        database.update_query(
        'UPDATE users SET city_id = ?, email = ?, phone_number = ?, firstname = ?, lastname = ? WHERE id = ?', 
        (payload.city_id, payload.email, payload.phone_number, payload.firstname, payload.lastname, user.id))

        return UserUpdated(
            id=user.id, 
            username=user.username, 
            city_id=int(payload.city_id), 
            email=payload.email, 
            phone_number=payload.phone_number, 
            firstname=payload.firstname, 
            lastname=payload.lastname, 
            company_info_id=payload.company_info_id)

    except IntegrityError:
        # mariadb raises error when a constraint is violated
        # in that case we have duplicate emails
        return None


def create_company_info(user: User, payload: CompanyInfoBody):
    generated_id = database.insert_query(
        '''INSERT INTO company_info (name, reg_number, company_address, company_phone, company_website, city_id, company_type_id, job_sector_id) 
        VALUES (?,?,?,?,?,?,?,?)''',
        (payload.name, payload.reg_number, payload.address, payload.phone, payload.website, payload.city_id, payload.company_type_id, payload.job_sector_id))

    database.update_query(
            'UPDATE users SET company_info_id = ? WHERE id = ?',
            (generated_id, user.id)
        )

    result = find_by_id(user.id)
    result.company_info_id = generated_id

    return result


def _hash_password(password: str):
    return sha256(password.encode('utf-8')).hexdigest()