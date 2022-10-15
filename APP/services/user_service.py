from mariadb import IntegrityError
from hashlib import sha256

from data import database
from data.models import Role, User
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


def find_by_id(user_id: int) -> User | None:
    data = database.read_query(
        'SELECT id, username, password, role FROM users WHERE id = ?',
        (user_id,)
    )

    return next((User.from_query_result(*row) for row in data), None)


def try_login(username: str, password: str) -> User | None:
    user = find_by_username(username)

    return user if (user and user.password == _hash_password(password)) else None


def create(username: str, password: str) -> User | None:
    try:
        generated_id = database.insert_query(
            'INSERT INTO users(username, password) VALUES (?,?)',
            (username, _hash_password(password))
        )

        return User(id=generated_id, username=username)

    except IntegrityError:
        # mariadb raises this error when a constraint is violated
        # in that case we have duplicate usernames
        return None


def _hash_password(password: str):
    return sha256(password.encode('utf-8')).hexdigest()