from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models import Board, Column
from ..core.deps import get_session, require_roles

router = APIRouter(prefix="/boards", tags=["boards"])

@router.get("/{board_id}/columns", response_model=list[dict])
async def list_columns(board_id: int, session: AsyncSession = Depends(get_session), user=Depends(require_roles("ADMIN","PO","COMMERCIAL","DEV","QA"))):
    stmt = select(Column).where(Column.board_id == board_id).order_by(Column.ordem)
    res = await session.execute(stmt)
    cols = res.scalars().all()
    return [{"id": c.id, "nome": c.nome, "ordem": c.ordem} for c in cols]
