from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.casa import CasaEditar, CasaResposta
from app.services import casa_service


router = APIRouter(
    prefix="/jogos/{jogo_id}/casas",
    tags=["Casas"]
)


@router.get(
    "/",
    response_model=list[CasaResposta]
)
def listar_casas(
    jogo_id: int,
    db: Session = Depends(get_db)
):
    return casa_service.consultar_casas(db, jogo_id)


@router.patch(
    "/{numero}",
    response_model=CasaResposta
)
def editar_casa(
    jogo_id: int,
    numero: int,
    dados: CasaEditar,
    db: Session = Depends(get_db)
):
    return casa_service.editar_casa(
        db=db,
        jogo_id=jogo_id,
        numero=numero,
        dados=dados
    )


@router.post(
    "/regenerar",
    response_model=list[CasaResposta]
)
def regenerar_tabuleiro(
    jogo_id: int,
    db: Session = Depends(get_db)
):
    return casa_service.regenerar_tabuleiro(
        db=db,
        jogo_id=jogo_id
    )
