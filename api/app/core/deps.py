from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator, List
from .config import settings
from .security import decode_token
from ..models import Base, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

engine = create_async_engine(settings.db_url, echo=False, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)) -> User:
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = await session.get(User, user_id)
    if not user or not user.active:
        raise HTTPException(status_code=401, detail="Inactive user")
    return user

def require_roles(*roles: List[str]):
    async def dependency(user: User = Depends(get_current_user)) -> User:
        if not set(user.roles).intersection(set(roles)):
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return dependency
