from datetime import datetime
from enum import Enum
from pydantic import BaseModel, constr

# ---------------
#  Enum classes
# ---------------
class Tags(str, Enum):
    home = 'Home Page'
    users = 'Users'


# ---------------
#  Schemas
# ---------------

class Token(BaseModel):
    token: str

            
class Role:
    USER = 'user'
    ADMIN = 'admin'

TUsername = constr(regex='^\w{2,30}$')
# Minimum eight characters, at least one letter and one number
TPassword = constr(regex='^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')


class User(BaseModel):
    id: int | None
    username: TUsername
    password = ''

    @classmethod
    def from_query_result(cls, id, username, password):
        return cls(
            id=id,
            username=username,
            password=password)


class LoginData(BaseModel):
    username: TUsername
    password: TPassword


class Message(BaseModel):
    id: int | None = None
    text: str
    receiver_id: int


class MessageResponseModel(BaseModel):
    id: int
    text: str
    created_at: datetime
    sender_id: int
    receiver_id: int


class MessageResponseModelShort(BaseModel):
    sender: str
    text: str
    created_at: datetime

    @classmethod
    def from_query_result(cls, sender, text, created_at):
        return cls(sender=sender, text=text, created_at=created_at)


class UserResponseModel(BaseModel):
    id: int | None
    username: TUsername

    @classmethod
    def from_query_result(cls, id, username):
        return cls(id=id, username=username)














































class HomeType(str, Enum):
    rental = 'Rental Housing'
    resource_housing = 'Resource Housing'


class NumberOfRooms(str, Enum):
    studio = 'Studio Appartment'
    one_room = '1 Room Appartment'
    two_rooms = '2 Room Appartment'
    house_floor = 'House Flooring Rental'

class City(str, Enum):
    plovdiv = '1'
    sofia = '2'

class Attachment(BaseModel):
    id: int
    home_post_id: int
    image: None


class HousingPost(BaseModel):
    id: int | None
    city_id: int
    rent_price: int
    description: str
    user_id: str
    home_type_id: str
    number_of_rooms_id: str

    attachments: list[Attachment]