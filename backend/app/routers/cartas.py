from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.carta import (
    CartaCriar,
    CartaEditar,
    CartaResposta
)
from app.services import carta_service


router = APIRouter(
    prefix="/cartas",
    tags=["Cartas"]
)


@router.get("/", response_model=list[CartaResposta])
def listar(db: Session = Depends(get_db)):
    return carta_service.consultar_cartas(db)


@router.get("/{carta_id}", response_model=CartaResposta)
def consultar(
    carta_id: int,
    db: Session = Depends(get_db)
):
    return carta_service.consultar_carta(db, carta_id)


@router.post(
    "/",
    response_model=CartaResposta,
    status_code=status.HTTP_201_CREATED
)
def cadastrar(
    dados: CartaCriar,
    db: Session = Depends(get_db)
):
    return carta_service.criar_carta(db, dados)


@router.put("/{carta_id}", response_model=CartaResposta)
def editar(
    carta_id: int,
    dados: CartaEditar,
    db: Session = Depends(get_db)
):
    return carta_service.editar_carta(db, carta_id, dados)


@router.delete("/{carta_id}")
def excluir(
    carta_id: int,
    db: Session = Depends(get_db)
):
    return carta_service.remover_carta(db, carta_id)