from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import Jogo
from app.repositories.casa_repository import adicionar_casas
from app.schemas.jogo import JogoCriar
from app.services.tabuleiro_service import gerar_casas_iniciais


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
