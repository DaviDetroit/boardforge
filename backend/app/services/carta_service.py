
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.casa_repository import (
    buscar_casa,
    listar_casas,
    salvar_alteracoes,
)
from app.schemas.casa import CasaEditar


def consultar_casas(db: Session, jogo_id: int):
    return listar_casas(db, jogo_id)


def editar_casa(
    db: Session,
    jogo_id: int,
    numero: int,
    dados: CasaEditar
):
    # Início e chegada são posições reservadas
    if numero == 1:
        raise HTTPException(
            status_code=400,
            detail="A casa inicial não pode ser editada."
        )

    # Procurar a casa no banco
    casa = buscar_casa(db, jogo_id, numero)

    if casa is None:
        raise HTTPException(
            status_code=404,
            detail="Casa não encontrada neste jogo."
        )

    # A chegada também não pode ser editada
    if casa.tipo in ("inicio", "fim"):
        raise HTTPException(
            status_code=400,
            detail="Casas de início e chegada não podem ser editadas."
        )

    # Aplicar os dados validados pelo schema
    alteracoes = dados.model_dump()

    try:
        for campo, valor in alteracoes.items():
            setattr(casa, campo, valor)

        # Enviar alterações ao MySQL
        salvar_alteracoes(db, casa)

        # Confirmar transação
        db.commit()

        # Atualizar o objeto retornado
        db.refresh(casa)

        return casa

    except Exception:
        db.rollback()
        raise
