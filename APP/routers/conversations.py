from fastapi import APIRouter, Header

from common.auth import get_user_or_raise_401
from common.responses import  NotFound
from data.models import Tags, MessageResponseModelShort, UserResponseModel
from services import conversation_service


conversations_router = APIRouter(prefix='/conversations')


@conversations_router.get('/', response_model=list[UserResponseModel], tags=[Tags.conversations])
def view_conversations(token: str = Header()):
    user = get_user_or_raise_401(token)
    
    result = conversation_service.view_conversations(user)
    if result is not None:
        return result

    return NotFound(content='No conversations found')


@conversations_router.get('/{username}', response_model=list[MessageResponseModelShort], tags=[Tags.conversations])
def view_conversation_with(username: str, token: str = Header()):
    user = get_user_or_raise_401(token)

    result = conversation_service.view_conversation_with(user, username)
    if result is not None:
        return result

    return NotFound(content=f'User {username} not found')


@conversations_router.delete('/{username}', tags=[Tags.conversations])
def delete_conversation_with(username: str, token: str = Header()):
    user = get_user_or_raise_401(token)

    result = conversation_service.remove_conversation_with(user, username)
    
    if result is not None:
        return result

    return NotFound(content=f'User {username} not found')