from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MessageBase(BaseModel):
    content: str
    room_id: str


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    sender_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MessageWithSender(Message):
    sender_username: str


class RoomBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = True

class RoomCreate(RoomBase):
    pass

class RoomOut(RoomBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class RoomMemberOut(BaseModel):
    user_id: int
    username: str
    joined_at: datetime

    class Config:
        from_attributes = True