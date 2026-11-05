from sqlalchemy.orm import Session

from app.database.models import Casa


def adicionar_casas(db: Session, casas: list[Casa]):
    db.add_all(casas)
    db.flush()
    return casas