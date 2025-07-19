from sqlalchemy.orm import Session
from app.database.models import Room, RoomMember

def create_room(db: Session, name: str, description: str = None, is_public: bool = True):
    db_room = Room(name=name, description=description, is_public=is_public)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def add_room_member(db: Session, user_id: int, room_id: int):
    member = RoomMember(user_id=user_id, room_id=room_id)
    db.add(member)
    db.commit()
    return member