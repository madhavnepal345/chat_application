import json
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.crud.chat import create_message, get_messages
from app.database import get_db
from app.dependencies.auth import get_current_active_user
from app.dependencies.websocket import get_websocket_user
from app.schemas.auth import UserInDB
from app.schemas.chat import Message, MessageCreate, MessageWithSender
from app.utils.websocket_manager import websocket_manager


router = APIRouter(prefix="/chat", tags=["chat"])


@router.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    token: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    try:
        token_data = await get_websocket_user(websocket, token)
        await websocket_manager.connect(room_id, websocket)
        
        # Send previous messages
        messages = get_messages(db, room_id=room_id, limit=50)
        for message in reversed(messages):
            message_with_sender = MessageWithSender(
                **message.__dict__,
                sender_username=message.sender.username
            )
            await websocket.send_text(message_with_sender.model_dump_json())
        
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Create and save the message
            message_create = MessageCreate(content=message_data["content"], room_id=room_id)
            db_message = create_message(db, message_create, sender_id=message_data["sender_id"])
            
            # Prepare the message with sender info
            message_with_sender = MessageWithSender(
                **db_message.__dict__,
                sender_username=db_message.sender.username
            )
            
            # Broadcast to all clients in the room
            await websocket_manager.broadcast(room_id, message_with_sender.model_dump_json())
    
    except WebSocketDisconnect:
        websocket_manager.disconnect(room_id, websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        websocket_manager.disconnect(room_id, websocket)
        await websocket.close()


@router.get("/messages/{room_id}", response_model=list[MessageWithSender])
def get_chat_messages(
    room_id: str,
    limit: Annotated[int, Query(le=100)] = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    messages = get_messages(db, room_id=room_id, limit=limit, offset=offset)
    return [
        MessageWithSender(
            **message.__dict__,
            sender_username=message.sender.username
        )
        for message in messages
    ]