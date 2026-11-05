from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import Jogo
from app.schemas.jogo import JogoCriar


def listar_jogos(db: Session):
    consulta = select(Jogo).order_by(Jogo.id)

    return db.scalars(consulta).all()


def criar_jogo(db: Session, dados: JogoCriar):
    jogo = Jogo(**dados.model_dump())

    try:
        db.add(jogo)
        db.commit()
        db.refresh(jogo)
        return jogo
    except Exception:
        db.rollback()
        raise
