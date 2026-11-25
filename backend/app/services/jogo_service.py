from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import Jogo
from app.repositories.casa_repository import adicionar_casas
from app.schemas.jogo import JogoCriar
from app.services.tabuleiro_service import gerar_casas_iniciais

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.repositories import jogo_repository
from app.schemas.jogo import JogoEditar


def listar_jogos(db: Session):
    consulta = select(Jogo).order_by(Jogo.id)
    return db.scalars(consulta).all()


def criar_jogo(db: Session, dados: JogoCriar):
    try:
        # 1. Criar o registro do jogo
        jogo = Jogo(**dados.model_dump())

        db.add(jogo)
        db.flush()

        # 2. Gerar todas as casas
        casas = gerar_casas_iniciais(
            jogo_id=jogo.id,
            quantidade_casas=jogo.quantidade_casas
        )

        # 3. Inserir as casas
        adicionar_casas(db, casas)

        # 4. Confirmar jogo + casas juntos
        db.commit()

        # 5. Atualizar o objeto com os dados do MySQL
        db.refresh(jogo)

        return jogo

    except Exception:
        db.rollback()
        raise

def consultar_jogo(db: Session, jogo_id: int):
    jogo = jogo_repository.buscar_jogo(db, jogo_id)

    if jogo is None:
        raise HTTPException(
            status_code=404,
            detail="Jogo não encontrado."
        )

    return jogo


def editar_jogo(
    db: Session,
    jogo_id: int,
    dados: JogoEditar
):
    consultar_jogo(db, jogo_id)

    try:
        jogo_repository.atualizar_jogo(
            db,
            jogo_id,
            dados.model_dump()
        )

        jogo = consultar_jogo(db, jogo_id)

        db.commit()

        return jogo

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Erro ao atualizar o jogo."
        )


def remover_jogo(db: Session, jogo_id: int):
    consultar_jogo(db, jogo_id)

    try:
        jogo_repository.excluir_jogo(db, jogo_id)

        db.commit()

        return {
            "mensagem": "Jogo excluído com sucesso."
        }

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Erro ao excluir o jogo."
        )
