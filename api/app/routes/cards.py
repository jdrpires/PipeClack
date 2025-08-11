from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..schemas import CardCreate, CardRead, CardMove, CommentCreate, CommentRead, AttachmentRead
from ..models import Card, Board, Comment, Attachment
from ..core.deps import get_session, require_roles
from ..core.config import settings
import os

router = APIRouter(tags=["cards"])

@router.post("/boards/{board_id}/cards", response_model=CardRead)
async def create_card(board_id: int, card_in: CardCreate, session: AsyncSession = Depends(get_session), user=Depends(require_roles("ADMIN","PO","DEV","QA","COMMERCIAL"))):
    board = await session.get(Board, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    card = Card(board_id=board_id, column_id=card_in.column_id, project_id=board.project_id, titulo=card_in.titulo, descricao=card_in.descricao, prioridade=card_in.prioridade, position=1000, created_by=user.id)
    session.add(card)
    await session.commit()
    await session.refresh(card)
    return card

@router.post("/cards/{card_id}/move", response_model=CardRead)
async def move_card(card_id: int, payload: CardMove, session: AsyncSession = Depends(get_session), user=Depends(require_roles("ADMIN","PO","DEV","QA","COMMERCIAL"))):
    card = await session.get(Card, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    card.column_id = payload.to_column_id
    card.position = payload.position
    await session.commit()
    await session.refresh(card)
    return card

@router.get("/cards/{card_id}/comments", response_model=list[CommentRead])
async def list_comments(card_id: int, session: AsyncSession = Depends(get_session), user=Depends(require_roles("ADMIN","PO","DEV","QA","COMMERCIAL"))):
    stmt = select(Comment).where(Comment.card_id == card_id)
    res = await session.execute(stmt)
    return res.scalars().all()

@router.post("/cards/{card_id}/comments", response_model=CommentRead)
async def create_comment(card_id: int, payload: CommentCreate, session: AsyncSession = Depends(get_session), user=Depends(require_roles("ADMIN","PO","DEV","QA","COMMERCIAL"))):
    comment = Comment(card_id=card_id, author_user_id=user.id, texto=payload.texto)
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return comment

@router.post("/cards/{card_id}/attachments", response_model=AttachmentRead)
async def upload_attachment(card_id: int, file: UploadFile = File(...), session: AsyncSession = Depends(get_session), user=Depends(require_roles("ADMIN","PO","DEV","QA","COMMERCIAL"))):
    contents = await file.read()
    if len(contents) > 10*1024*1024:
        raise HTTPException(status_code=400, detail="File too large")
    filename = file.filename
    path = os.path.join(settings.upload_dir, filename)
    with open(path, "wb") as f:
        f.write(contents)
    attach = Attachment(card_id=card_id, filename=filename, path=path, uploaded_by=user.id)
    session.add(attach)
    await session.commit()
    await session.refresh(attach)
    return attach
