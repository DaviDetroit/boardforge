from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.repositories import carta_repository
from app.schemas.carta import CartaCriar, CartaEditar


# Validar se o jogo de origem existe
def validar_jogo_origem(db: Session, jogo_id: int | None):
    if jogo_id is None:
        return

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
            detail="Jogo de origem não encontrado."
        )


# Consultar todas as cartas
def consultar_cartas(db: Session):
    return carta_repository.listar_cartas(db)


# Consultar uma carta específica
def consultar_carta(db: Session, carta_id: int):
    carta = carta_repository.buscar_carta(db, carta_id)

    if carta is None:
        raise HTTPException(
            status_code=404,
            detail="Carta não encontrada."
        )

    return carta


# Criar uma nova carta
def criar_carta(db: Session, dados: CartaCriar):
    validar_jogo_origem(db, dados.jogo_origem_id)

    try:
        carta_id = carta_repository.cadastrar_carta(
            db,
            dados.model_dump()
        )

        carta = consultar_carta(db, carta_id)

        db.commit()

        return carta

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Erro ao cadastrar a carta."
        )


# Editar uma carta existente
def editar_carta(
    db: Session,
    carta_id: int,
    dados: CartaEditar
):
    consultar_carta(db, carta_id)

    validar_jogo_origem(db, dados.jogo_origem_id)

    try:
        carta_repository.atualizar_carta(
            db,
            carta_id,
            dados.model_dump()
        )

        carta = consultar_carta(db, carta_id)

        db.commit()

        return carta

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Erro ao atualizar a carta."
        )


# Excluir uma carta existente
def remover_carta(db: Session, carta_id: int):
    consultar_carta(db, carta_id)

    try:
        carta_repository.excluir_carta(db, carta_id)

        db.commit()

        return {
            "mensagem": "Carta excluída com sucesso."
        }

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Erro ao excluir a carta."
        )