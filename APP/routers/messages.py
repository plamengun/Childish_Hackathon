from fastapi import APIRouter, Header

from common.auth import get_user_or_raise_401
from common.responses import NotFound
from data.models import Tags, Message, MessageResponseModel
from services import message_service


messages_router = APIRouter(prefix='/messages')


@messages_router.post('/', response_model=MessageResponseModel, tags=[Tags.messages])
def create_message(message: Message, token: str = Header()):
    user = get_user_or_raise_401(token)

    result = message_service.create(message, user)
    
    return result or NotFound(f'User with id: {message.receiver_id} not found')