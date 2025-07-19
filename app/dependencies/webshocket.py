from typing import Annotated, Optional

from fastapi import WebSocket, WebSocketException, status
from jose import JWTError, jwt

from app.config import settings
from app.database import get_db
from app.schemas.auth import TokenData
from app.crud.user import get_user


async def get_websocket_user(
    websocket: WebSocket,
    token: Optional[str] = None,
) -> TokenData:
    if token is None:
        raise WebSocketException(
            code=status.HTTP_400_BAD_REQUEST,
            reason="Authorization token is missing"
        )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise WebSocketException(
                code=status.HTTP_401_UNAUTHORIZED,
                reason="Invalid authentication credentials"
            )
        return TokenData(username=username, role=role)
    except JWTError:
        raise WebSocketException(
            code=status.HTTP_401_UNAUTHORIZED,
            reason="Invalid authentication credentials"
        )