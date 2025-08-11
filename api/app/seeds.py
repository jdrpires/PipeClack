import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .core.deps import async_session
from .models import User, Project, Board, Column, Card, DiscoveryTemplate
from .models.board import BoardType
from .models.project import ProjectStatus
from .models.card import CardPriority
from .routes.projects import DEFAULT_COLUMNS
from .core.security import get_password_hash

USERS = [
    ("Admin", "admin@clack.com", "Admin@123", ["ADMIN"]),
    ("Commercial", "sales@clack.com", "Sales@123", ["COMMERCIAL"]),
    ("PO", "po@clack.com", "Po@123", ["PO"]),
    ("Dev", "dev@clack.com", "Dev@123", ["DEV"]),
    ("QA", "qa@clack.com", "Qa@123", ["QA"]),
]

default_template = {
  "version": 1,
  "sections": [
    {"key": "objetivos_negocio", "label": "Objetivos do Negócio", "type": "textarea", "required": True, "help": "Quais resultados o cliente busca (receita, eficiência, compliance etc.)?"},
    {"key": "stakeholders", "label": "Stakeholders", "type": "list", "itemSchema": {"fields": [
        {"key":"nome","label":"Nome","type":"text","required":True},
        {"key":"papel","label":"Papel","type":"text","required":True},
        {"key":"contato","label":"Contato","type":"text","required":False}
      ]}},
    {"key": "escopo_inicial", "label": "Escopo Inicial", "type": "textarea", "required": True},
    {"key": "requisitos_funcionais", "label": "Requisitos Funcionais", "type": "list", "itemSchema": {"fields": [
        {"key":"titulo","label":"Título","type":"text","required":True},
        {"key":"descricao","label":"Descrição","type":"textarea","required":True},
        {"key":"prioridade","label":"Prioridade","type":"select","options":["BAIXA","MEDIA","ALTA","CRITICA"],"required":True}
      ]}},
    {"key": "requisitos_tecnicos", "label": "Requisitos Técnicos", "type": "textarea"},
    {"key": "integracoes", "label": "Integrações", "type": "list", "itemSchema": {"fields": [
        {"key":"sistema","label":"Sistema","type":"text"},
        {"key":"tipo","label":"Tipo (API, arquivo, DB)","type":"text"},
        {"key":"detalhes","label":"Detalhes","type":"textarea"}
      ]}},
    {"key": "restricoes", "label": "Restrições", "type": "textarea"},
    {"key": "riscos", "label": "Riscos", "type": "list", "itemSchema": {"fields": [
        {"key":"risco","label":"Risco","type":"text"},
        {"key":"impacto","label":"Impacto","type":"select","options":["BAIXO","MEDIO","ALTO"]},
        {"key":"mitigacao","label":"Mitigação","type":"textarea"}
      ]}},
    {"key": "cronograma", "label": "Cronograma Estimado", "type": "list", "itemSchema": {"fields": [
        {"key":"entrega","label":"Entrega","type":"text"},
        {"key":"inicio","label":"Início","type":"date"},
        {"key":"fim","label":"Fim","type":"date"}
      ]}},
    {"key": "criterios_aceitacao", "label": "Critérios de Aceitação", "type": "textarea", "required": True}
  ]
}

async def seed():
    async with async_session() as session:
        # Users
        for name, email, pwd, roles in USERS:
            stmt = select(User).where(User.email == email)
            res = await session.execute(stmt)
            if not res.scalars().first():
                u = User(name=name, email=email, password_hash=get_password_hash(pwd), roles=roles)
                session.add(u)
        # discovery template
        res = await session.execute(select(DiscoveryTemplate))
        if not res.scalars().first():
            session.add(DiscoveryTemplate(titulo="Default", conteudo_json=default_template))
        await session.commit()
        # projects
        proj = Project(name="Demo Project", status=ProjectStatus.EM_DISCOVERY)
        session.add(proj)
        await session.flush()
        # create commercial board with cards
        board = Board(project_id=proj.id, tipo=BoardType.COMERCIAL)
        session.add(board)
        await session.flush()
        for idx, name in enumerate(DEFAULT_COLUMNS[BoardType.COMERCIAL]):
            col = Column(board_id=board.id, nome=name, ordem=idx)
            session.add(col)
            if idx == 0:
                first_col = col
        session.add(Card(board_id=board.id, column_id=first_col.id, project_id=proj.id, titulo="Lead", descricao="", prioridade=CardPriority.MEDIA, position=1000, created_by=1))
        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed())
