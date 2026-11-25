from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.schemas.jogo import (
    JogoCriar,
    JogoResposta,
    JogoEditar
)

from app.services import jogo_service

router = APIRouter(
    prefix="/jogos",
    tags=["Jogos"]
)


@router.get("/", response_model=list[JogoResposta])
def listar(db: Session = Depends(get_db)):
    return jogo_service.listar_jogos(db)


@router.post(
    "/",
    response_model=JogoResposta,
    status_code=status.HTTP_201_CREATED
)
def cadastrar(
    dados: JogoCriar,
    db: Session = Depends(get_db)
):
    return jogo_service.criar_jogo(db, dados)

@router.get(
    "/{jogo_id}",
    response_model=JogoResposta
)
def consultar(
    jogo_id: int,
    db: Session = Depends(get_db)
):
    return jogo_service.consultar_jogo(
        db,
        jogo_id
    )


@router.put(
    "/{jogo_id}",
    response_model=JogoResposta
)
def editar(
    jogo_id: int,
    dados: JogoEditar,
    db: Session = Depends(get_db)
):
    return jogo_service.editar_jogo(
        db,
        jogo_id,
        dados
    )


@router.delete("/{jogo_id}")
def excluir(
    jogo_id: int,
    db: Session = Depends(get_db)
):
    return jogo_service.remover_jogo(
        db,
        jogo_id
    )