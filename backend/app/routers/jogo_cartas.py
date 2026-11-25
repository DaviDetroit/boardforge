from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.carta import CartaResposta
from app.services import jogo_carta_service


router = APIRouter(
    prefix="/jogos/{jogo_id}/cartas",
    tags=["Cartas do Jogo"]
)


# Listar cartas associadas ao jogo
@router.get("/", response_model=list[CartaResposta])
def listar(
    jogo_id: int,
    db: Session = Depends(get_db)
):
    return jogo_carta_service.consultar_cartas_do_jogo(
        db,
        jogo_id
    )


# Associar carta ao jogo
@router.post(
    "/{carta_id}",
    status_code=status.HTTP_201_CREATED
)
def vincular(
    jogo_id: int,
    carta_id: int,
    db: Session = Depends(get_db)
):
    return jogo_carta_service.vincular_carta(
        db,
        jogo_id,
        carta_id
    )


# Desvincular carta do jogo
@router.delete("/{carta_id}")
def desvincular(
    jogo_id: int,
    carta_id: int,
    db: Session = Depends(get_db)
):
    return jogo_carta_service.desvincular_carta(
        db,
        jogo_id,
        carta_id
    )