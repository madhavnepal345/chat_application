from typing import List, Optional

from sqlalchemy.orm import Session

from app.database.models import Message, Room, RoomMember,User
from app.schemas.chat import MessageCreate


def get_messages(db: Session, room_id: str, limit: int = 100, offset: int = 0) -> List[Message]:
    return (
        db.query(Message)
        .filter(Message.room_id == room_id)
        .order_by(Message.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def create_message(db: Session, message: MessageCreate, sender_id: int) -> Message:
    db_message = Message(**message.model_dump(), sender_id=sender_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def create_room(db: Session, name: str, description: str = None, is_public: bool = True):
    db_room = Room(name=name, description=description, is_public=is_public)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def get_room(db: Session, room_id: int, user_id: int = None):
    query = db.query(Room)
    if user_id:
        query = query.join(RoomMember).filter(RoomMember.user_id == user_id)
    return query.filter(Room.id == room_id).first()

def add_room_member(db: Session, user_id: int, room_id: int):
    member = RoomMember(user_id=user_id, room_id=room_id)
    db.add(member)
    db.commit()
    return member

def get_user_rooms(db: Session, user_id: int):
    return db.query(Room).join(RoomMember).filter(RoomMember.user_id == user_id).all()

def get_room_members(db: Session, room_id: int):
    return (
        db.query(User, RoomMember.joined_at)
        .join(RoomMember, User.id == RoomMember.user_id)
        .filter(RoomMember.room_id == room_id)
        .all()
    )