import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .core.config import settings
from .routes import auth, projects, cards, boards
from .models import Base
from .core.deps import engine

app = FastAPI(title="Clack Project Control")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(cards.router)
app.include_router(boards.router)

if not os.path.exists(settings.upload_dir):
    os.makedirs(settings.upload_dir)
app.mount("/files", StaticFiles(directory=settings.upload_dir), name="files")

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
