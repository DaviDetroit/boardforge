from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.repositories import (
    carta_repository,
    jogo_carta_repository
)


# Verificar se o jogo existe
def validar_jogo(db: Session, jogo_id: int):
    consulta = text("""
        SELECT id
        FROM jogos
        WHERE id = :jogo_id
    """)

    jogo = db.execute(
        consulta,
        {"jogo_id": jogo_id}
    ).first()

    if jogo is None:
        raise HTTPException(
            status_code=404,
            detail="Jogo não encontrado."
        )


# Verificar se a carta existe
def validar_carta(db: Session, carta_id: int):
    carta = carta_repository.buscar_carta(
        db,
        carta_id
    )

    if carta is None:
        raise HTTPException(
            status_code=404,
            detail="Carta não encontrada."
        )


# Listar cartas associadas ao jogo
def consultar_cartas_do_jogo(
    db: Session,
    jogo_id: int
):
    validar_jogo(db, jogo_id)

    return jogo_carta_repository.listar_cartas_do_jogo(
        db,
        jogo_id
    )


# Associar uma carta ao jogo
def vincular_carta(
    db: Session,
    jogo_id: int,
    carta_id: int
):
    validar_jogo(db, jogo_id)
    validar_carta(db, carta_id)

    associacao = jogo_carta_repository.buscar_associacao(
        db,
        jogo_id,
        carta_id
    )

    if associacao is not None:
        raise HTTPException(
            status_code=409,
            detail="Esta carta já está associada ao jogo."
        )

    try:
        jogo_carta_repository.associar_carta(
            db,
            jogo_id,
            carta_id
        )

        db.commit()

        return {
            "mensagem": "Carta associada com sucesso.",
            "jogo_id": jogo_id,
            "carta_id": carta_id
        }

    except IntegrityError as erro:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Conflito ao associar a carta."
        ) from erro

    except SQLAlchemyError as erro:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Erro ao associar a carta."
        ) from erro


# Desvincular uma carta do jogo
def desvincular_carta(
    db: Session,
    jogo_id: int,
    carta_id: int
):
    validar_jogo(db, jogo_id)

    associacao = jogo_carta_repository.buscar_associacao(
        db,
        jogo_id,
        carta_id
    )

    if associacao is None:
        raise HTTPException(
            status_code=404,
            detail="Esta carta não está associada ao jogo."
        )

    try:
        jogo_carta_repository.desassociar_carta(
            db,
            jogo_id,
            carta_id
        )

        db.commit()

        return {
            "mensagem": "Carta desvinculada com sucesso.",
            "jogo_id": jogo_id,
            "carta_id": carta_id
        }

    except SQLAlchemyError as erro:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Erro ao desvincular a carta."
        ) from erro