from typing import List, Optional

from sqlalchemy.orm import Session

from app.database.models import Message
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