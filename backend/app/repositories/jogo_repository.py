from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.database.models import Jogo
from app.repositories.casa_repository import adicionar_casas
from app.schemas.jogo import JogoCriar
from app.services.tabuleiro_service import gerar_casas_iniciais


# Listar jogos
def listar_jogos(db: Session):
    consulta = select(Jogo).order_by(Jogo.id)
    return db.scalars(consulta).all()


# Criar jogo e gerar suas casas
def criar_jogo(db: Session, dados: JogoCriar):
    try:
        jogo = Jogo(**dados.model_dump())

        db.add(jogo)
        db.flush()

        casas = gerar_casas_iniciais(
            jogo_id=jogo.id,
            quantidade_casas=jogo.quantidade_casas
        )

        adicionar_casas(db, casas)

        db.commit()
        db.refresh(jogo)

        return jogo

    except Exception:
        db.rollback()
        raise


# Buscar jogo pelo ID
def buscar_jogo(db: Session, jogo_id: int):
    consulta = text("""
        SELECT *
        FROM jogos
        WHERE id = :jogo_id
    """)

    return db.execute(
        consulta,
        {"jogo_id": jogo_id}
    ).mappings().first()


# Atualizar jogo
def atualizar_jogo(
    db: Session,
    jogo_id: int,
    dados: dict
):
    consulta = text("""
        UPDATE jogos
        SET
            nome = :nome,
            descricao = :descricao,
            tema = :tema
        WHERE id = :jogo_id
    """)

    db.execute(
        consulta,
        {**dados, "jogo_id": jogo_id}
    )


# Excluir jogo
def excluir_jogo(db: Session, jogo_id: int):
    consulta = text("""
        DELETE FROM jogos
        WHERE id = :jogo_id
    """)

    db.execute(
        consulta,
        {"jogo_id": jogo_id}
    )