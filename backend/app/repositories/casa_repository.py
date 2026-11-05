from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import Casa


def adicionar_casas(db: Session, casas: list[Casa]):
    db.add_all(casas)
    db.flush()
    return casas


def buscar_casa(
    db: Session,
    jogo_id: int,
    numero: int
) -> Casa | None:

    consulta = select(Casa).where(
        Casa.jogo_id == jogo_id,
        Casa.numero == numero
    )

    return db.scalar(consulta)


def listar_casas(
    db: Session,
    jogo_id: int
) -> list[Casa]:

    consulta = (
        select(Casa)
        .where(Casa.jogo_id == jogo_id)
        .order_by(Casa.numero)
    )

    return list(db.scalars(consulta).all())


def salvar_alteracoes(db: Session, casa: Casa) -> Casa:
    db.add(casa)
    db.flush()
    return casa
