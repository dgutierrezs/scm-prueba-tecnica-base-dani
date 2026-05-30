from contextlib import asynccontextmanager
from typing import Annotated, Any

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import (
    authenticate,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    get_current_user,
)
from app.database import Base, engine, get_session
from app.filters import apply_filters
from app.models import Item


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

# CORS abierto para que el frontend del candidato pueda conectarse sin fricción
# en local. En producción se restringiría a orígenes conocidos.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str

class Filter(BaseModel):
    field: str
    operator: str
    value: Any | None = None

class SearchRequest(BaseModel):
    # TODO (candidato): diseña aquí el contrato de filtros estructurados.
    filters: list[Filter] | None = None


class ItemOut(BaseModel):
    id: int
    sku: str
    status: str
    warehouse_id: int

    model_config = {"from_attributes": True}


@app.post("/auth/login")
async def login(payload: LoginRequest) -> TokenPair:
    if not authenticate(payload.username, payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )
    return TokenPair(
        access_token=create_access_token(payload.username),
        refresh_token=create_refresh_token(payload.username),
    )


@app.post("/auth/refresh")
async def refresh(payload: RefreshRequest) -> TokenPair:
    subject = decode_refresh_token(payload.refresh_token)
    return TokenPair(
        access_token=create_access_token(subject),
        refresh_token=create_refresh_token(subject),
    )


@app.post("/items/search")
async def search_items(
    payload: SearchRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
    _user: Annotated[str, Depends(get_current_user)],
) -> list[ItemOut]:
    stmt = select(Item)
    stmt = apply_filters(stmt, payload.filters)
    result = await session.execute(stmt)
    return [ItemOut.model_validate(i) for i in result.scalars().all()]
