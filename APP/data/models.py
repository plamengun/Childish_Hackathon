from datetime import datetime
from enum import Enum
from pydantic import BaseModel, constr

# ---------------
#  Enum classes
# ---------------
class Tags(str, Enum):
    home = 'Home Page'
    users = 'Users'
    jobs = 'Jobs'
    housings = 'Housing Posts'

class UserTypes(str, Enum):
    admin = '1'
    normal = '2'
    mentor = '3'
    employer = '4'
    landlord = '5'
    other = '6'

class Cities(str, Enum):
    sofia = '1'
    plovdiv = '2'
    varna = '3'
    burgas = '4'

class JobSectors(str, Enum):
    trade = '1'
    uncategorised = '2'

class EmplType(str, Enum):
    fulltime = '1'
    parttime = '2'
    internship = '3'

class HomeType(str, Enum):
    rental = '1'
    resource_housing = '2'

class NumberOfRooms(str, Enum):
    studio = '1'
    one_room = '2'
    two_rooms = '3'
    house_floor = '4'


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


class JobAd(BaseModel):
    id: int
    user_id: int
    city_id: int
    sector_id: int
    type_id: int
    description: str

class JobAdRepr(BaseModel):
    id: int
    user: UserResponseModel
    city: str
    sector: str
    type: str
    description: str

    @classmethod
    def from_query_result(cls, id, user_id, username, city, sector, type, description):
        return cls(
            id = id,
            user = UserResponseModel(id=user_id, username=username),
            city = city,
            sector = sector,
            type = type,
            description = description)

class JobCreate(BaseModel):
    description: str







































class Attachment(BaseModel):
    id: int
    home_post_id: int
    image: None


class HousingPostRepr(BaseModel):
    id: int
    city_id: int
    rent_price: int | None
    description: str
    user_id: int
    home_type_id: int
    number_of_rooms_id: int

    attachments: list[Attachment] | None

class HousePostBody(BaseModel):
    rent_price: int | None
    description: str
    city_id: Cities
    number_of_rooms_id: NumberOfRooms
    home_type_id: HomeType