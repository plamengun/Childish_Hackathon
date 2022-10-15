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
    messages = 'Messages'
    conversations = 'Conversations'

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


class CompanyInfoBody(BaseModel):
    id: int | None = None
    name: str
    reg_number: str
    address: str
    phone: str
    website: str | None = None
    city_id : int | None = None
    company_type_id: int
    job_sector_id: int


class UserAttributesBody(BaseModel):
    city_id: Cities | None = None
    email: str | None = None
    phone_number: str | None = None
    firstname: str | None = None
    lastname: str | None = None
    company_info_id: int | None = None


class UserUpdated(BaseModel):
    id: int | None = None
    username: TUsername
    password: str = ''
    city_id: int | None = None
    email: str | None = None
    phone_number: str | None = None
    firstname: str | None = None
    lastname: str | None = None
    company_info_id: int | None = None

    @classmethod
    def from_query_result(cls, id, username, city_id, email, phone_number, firstname, lastname, company_info_id, password=''):
        return cls(
            id=id,
            username=username,
            password=password,
            city_id=city_id,
            email=email,
            phone_number=phone_number,
            first_name=firstname,
            lastname=lastname,
            company_info_id=company_info_id
            )


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
    id: int | None
    user_id: int | None
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








































class Attachment(BaseModel):
    id: int
    home_post_id: int
    image: None


class HousingPostRepr(BaseModel):
    id: int
    city: str
    rent_price: int | None
    description: str
    user: UserResponseModel
    home_type: str
    number_of_rooms: str

    # attachments: list[Attachment] | None

    @classmethod
    def from_query_result(cls, id, city, rent_price, description, user_id, username, home_type, number_of_rooms):
        return cls(
            id = id,
            city=city,
            rent_price=rent_price,
            description=description,
            user = UserResponseModel(id=user_id, username=username),
            home_type=home_type,
            number_of_rooms=number_of_rooms)

class HousePostBody(BaseModel):
    city_id: Cities
    rent_price: int | None
    description: str
    user_id: int | None
    home_type_id: HomeType
    number_of_rooms_id: NumberOfRooms
    