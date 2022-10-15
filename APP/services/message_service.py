from datetime import datetime

from data import database
from data.models import Message, MessageResponseModel, User


def create(message: Message, user: User, datetime_now = datetime.now()): # Dependency Injection
    user_ids = database.read_query('SELECT id FROM users')
    
    receiver_id_in_user_ids = False
    for i in user_ids:
        if message.receiver_id in i:
            receiver_id_in_user_ids = True
            break

    if receiver_id_in_user_ids:
        # datetime_now = datetime.now()
        generated_id = database.insert_query(
            'INSERT into messages(created_at, text, sender_id, receiver_id) VALUES (?,?,?,?)',
            (datetime_now, message.text, user.id, message.receiver_id)
        )

        message.id = generated_id

        return MessageResponseModel(
            id=message.id, text=message.text, created_at=datetime_now, 
            sender_id=user.id, receiver_id=message.receiver_id
        )
