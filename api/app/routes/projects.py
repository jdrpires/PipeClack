from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..schemas import ProjectCreate, ProjectRead, DiscoveryResponseCreate, DiscoveryTemplateRead
from ..models import Project, Board, Column, Card, DiscoveryResponse, DiscoveryTemplate
from ..models.board import BoardType
from ..models.project import ProjectStatus
from ..models.card import CardPriority
from ..core.deps import get_session, require_roles

router = APIRouter(prefix="/projects", tags=["projects"])

DEFAULT_COLUMNS = {
    BoardType.COMERCIAL: ["Prospecção", "Em Proposta", "Proposta Fechada", "Aguardando Discovery"],
    BoardType.PO: ["Backlog", "Especificação Funcional", "Especificação Técnica", "QA", "Pronto para Desenvolvimento"],
    BoardType.DEV: ["Backlog", "Refinado", "Em Desenvolvimento", "Pronto para Teste", "Em Teste", "Validado", "Pronto"],
}

@router.post("/", response_model=ProjectRead)
async def create_project(project_in: ProjectCreate, session: AsyncSession = Depends(get_session), user=Depends(require_roles("ADMIN","PO"))):
    project = Project(name=project_in.name, status=project_in.status or ProjectStatus.EM_DISCOVERY)
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project

@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(project_id: int, session: AsyncSession = Depends(get_session), user=Depends(require_roles("ADMIN","PO","COMMERCIAL","DEV","QA"))):
    project = await session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Not found")
    return project

@router.post("/{project_id}/boards", response_model=dict)
async def create_board(project_id: int, data: dict, session: AsyncSession = Depends(get_session), user=Depends(require_roles("ADMIN","PO","COMMERCIAL"))):
    tipo = BoardType(data.get("tipo"))
    board = Board(project_id=project_id, tipo=tipo)
    session.add(board)
    await session.flush()
    for idx, name in enumerate(DEFAULT_COLUMNS[tipo]):
        col = Column(board_id=board.id, nome=name, ordem=idx)
        session.add(col)
    await session.commit()
    await session.refresh(board)
    return {"id": board.id, "tipo": board.tipo}

@router.get("/{project_id}/boards", response_model=list[dict])
async def list_boards(project_id: int, tipo: BoardType | None = None, session: AsyncSession = Depends(get_session), user=Depends(require_roles("ADMIN","PO","COMMERCIAL","DEV","QA"))):
    stmt = select(Board).where(Board.project_id == project_id)
    if tipo:
        stmt = stmt.where(Board.tipo == tipo)
    res = await session.execute(stmt)
    boards = res.scalars().all()
    return [{"id": b.id, "tipo": b.tipo} for b in boards]

@router.get("/discovery/template", response_model=DiscoveryTemplateRead)
async def get_template(session: AsyncSession = Depends(get_session), user=Depends(require_roles("ADMIN","PO","COMMERCIAL","DEV","QA"))):
    stmt = select(DiscoveryTemplate)
    res = await session.execute(stmt)
    template = res.scalars().first()
    return template

@router.post("/{project_id}/discovery", response_model=dict)
async def save_discovery(project_id: int, payload: DiscoveryResponseCreate, session: AsyncSession = Depends(get_session), user=Depends(require_roles("ADMIN","PO"))):
    response = DiscoveryResponse(project_id=project_id, template_id=payload.template_id, respostas_json=payload.respostas_json)
    session.add(response)
    await session.commit()
    return {"status": "saved"}

@router.post("/{project_id}/discovery/complete", response_model=dict)
async def complete_discovery(project_id: int, session: AsyncSession = Depends(get_session), user=Depends(require_roles("ADMIN","PO"))):
    stmt = select(DiscoveryResponse).where(DiscoveryResponse.project_id == project_id)
    res = await session.execute(stmt)
    resp = res.scalars().first()
    if not resp:
        raise HTTPException(status_code=400, detail="No discovery response")
    # ensure PO board
    stmt = select(Board).where(Board.project_id==project_id, Board.tipo==BoardType.PO)
    resb = await session.execute(stmt)
    board = resb.scalars().first()
    if not board:
        board = Board(project_id=project_id, tipo=BoardType.PO)
        session.add(board)
        await session.flush()
        for idx, name in enumerate(DEFAULT_COLUMNS[BoardType.PO]):
            session.add(Column(board_id=board.id, nome=name, ordem=idx))
    # create cards from requisitos_funcionais
    backlog_col_stmt = select(Column).where(Column.board_id==board.id).order_by(Column.ordem)
    col_res = await session.execute(backlog_col_stmt)
    first_col = col_res.scalars().first()
    requisitos = resp.respostas_json.get("requisitos_funcionais", [])
    for idx, item in enumerate(requisitos):
        titulo = item.get("titulo")
        descricao = item.get("descricao", "")
        prioridade = CardPriority[item.get("prioridade", "MEDIA")]
        card = Card(board_id=board.id, column_id=first_col.id, project_id=project_id, titulo=titulo, descricao=descricao, prioridade=prioridade, position=1000+idx, created_by=user.id)
        session.add(card)
    project = await session.get(Project, project_id)
    project.status = ProjectStatus.EM_PO
    await session.commit()
    return {"status": "completed"}
