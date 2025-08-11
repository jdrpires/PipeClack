from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..schemas import UserCreate, UserRead, Token
from ..models import User
from ..core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, decode_token
from ..core.deps import get_session, require_roles

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead)
async def register(user_in: UserCreate, session: AsyncSession = Depends(get_session), user: User = Depends(require_roles("ADMIN"))):
    stmt = select(User).where(User.email == user_in.email)
    result = await session.execute(stmt)
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(name=user_in.name, email=user_in.email, password_hash=get_password_hash(user_in.password), roles=user_in.roles)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@router.post("/login", response_model=Token)
async def login(form: UserCreate, session: AsyncSession = Depends(get_session)):
    stmt = select(User).where(User.email == form.email)
    res = await session.execute(stmt)
    user = res.scalars().first()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access = create_access_token({"sub": str(user.id), "roles": user.roles})
    refresh = create_refresh_token({"sub": str(user.id)})
    return Token(access_token=access, refresh_token=refresh)

@router.post("/refresh", response_model=Token)
async def refresh(token: Token, session: AsyncSession = Depends(get_session)):
    try:
        payload = decode_token(token.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=400, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid token")
    user_id = payload.get("sub")
    user = await session.get(User, user_id)
    access = create_access_token({"sub": str(user.id), "roles": user.roles})
    refresh = create_refresh_token({"sub": str(user.id)})
    return Token(access_token=access, refresh_token=refresh)

@router.get("/me", response_model=UserRead)
async def me(user: User = Depends(require_roles("ADMIN","PO","COMMERCIAL","DEV","QA"))):
    return user
