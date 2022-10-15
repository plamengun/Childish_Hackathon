from data import database
from data.models import MessageResponseModelShort, User, UserResponseModel
from common.responses import NoContent, NotFound
from services.user_service import find_by_username


def view_conversations(user: User):
    data = database.read_query(f'''
        SELECT distinct u.id, u.username from messages as m
        JOIN users as u on m.receiver_id = u.id or m.sender_id = u.id 
        WHERE (m.sender_id = ? or m.receiver_id = ?) and u.id != ? 
        ORDER BY u.id''', (user.id, user.id, user.id)
    )

    if data:
        return (UserResponseModel.from_query_result(*row) for row in data)


def view_conversation_with(user: User, username: str):
    user1 = user
    user2 = find_by_username(username)

    if user2:
        data = _has_conversation(user1, user2)
        if data:
            return (MessageResponseModelShort.from_query_result(*row) for row in data)
    
        return NotFound(content=f'You have no conversation with {username}')


def remove_conversation_with(user: User, username: str):
    user1 = user
    user2 = find_by_username(username)

    if user2:
        if _has_conversation(user1, user2):
            database.update_query('''
                DELETE FROM messages 
                WHERE (sender_id = ? and receiver_id = ?) or (sender_id = ? and receiver_id = ?)''', 
                (user1.id, user2.id, user2.id, user1.id)
            )

            return NoContent()
        
        return NotFound(content=f'You have no conversation with {username}')


def _has_conversation(user1: User, user2: User):
    data = database.read_query(f'''
            SELECT u.username, m.text, m.created_at from messages as m
            JOIN users as u on m.sender_id = u.id
            WHERE (sender_id = ? and receiver_id = ?) or (sender_id = ? and receiver_id = ?) 
            ORDER BY created_at''', (user1.id, user2.id, user2.id, user1.id)
        )
    
    return data