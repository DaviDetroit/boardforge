from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.casa_repository import (
    buscar_casa,
    listar_casas,
    salvar_alteracoes,
)
from app.schemas.casa import CasaEditar
from app.services.tabuleiro_service import regenerar_casas

def consultar_casas(db: Session, jogo_id: int):
    return listar_casas(db, jogo_id)


def editar_casa(
    db: Session,
    jogo_id: int,
    numero: int,
    dados: CasaEditar
):
    if numero == 1:
        raise HTTPException(
            status_code=400,
            detail="A casa inicial não pode ser editada."
        )

    casa = buscar_casa(db, jogo_id, numero)

    if casa is None:
        raise HTTPException(
            status_code=404,
            detail="Casa não encontrada neste jogo."
        )

    if casa.tipo in ("inicio", "fim"):
        raise HTTPException(
            status_code=400,
            detail="Casas de início e chegada não podem ser editadas."
        )

    try:
        for campo, valor in dados.model_dump().items():
            setattr(casa, campo, valor)

        salvar_alteracoes(db, casa)
        db.commit()
        db.refresh(casa)

        return casa

    except Exception:
        db.rollback()
        raise

def regenerar_tabuleiro(db: Session, jogo_id: int):
    casas = listar_casas(db, jogo_id)

    if not casas:
        raise HTTPException(
            status_code=404,
            detail="Jogo não encontrado ou sem casas."
        )

    try:
        casas_regeneradas = regenerar_casas(casas)

        # Verifica se há três casas especiais consecutivas.
        for indice in range(len(casas_regeneradas) - 2):
            trio = casas_regeneradas[indice:indice + 3]

            if all(
                casa.tipo not in ("normal", "inicio", "fim")
                for casa in trio
            ):
                raise HTTPException(
                    status_code=409,
                    detail=(
                        "Não foi possível regenerar o tabuleiro "
                        "sem criar três casas especiais consecutivas."
                    )
                )

        db.flush()
        db.commit()

        for casa in casas_regeneradas:
            db.refresh(casa)

        return casas_regeneradas

    except Exception:
        db.rollback()
        raise
