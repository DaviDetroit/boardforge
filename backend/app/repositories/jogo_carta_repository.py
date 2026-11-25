from sqlalchemy import text
from sqlalchemy.orm import Session


# Listar cartas associadas a um jogo
def listar_cartas_do_jogo(db: Session, jogo_id: int):
    consulta = text("""
        SELECT c.*
        FROM cartas c
        INNER JOIN jogo_cartas jc
            ON jc.carta_id = c.id
        WHERE jc.jogo_id = :jogo_id
        ORDER BY c.id
    """)

    return db.execute(
        consulta,
        {"jogo_id": jogo_id}
    ).mappings().all()


# Verificar se a associação já existe
def buscar_associacao(
    db: Session,
    jogo_id: int,
    carta_id: int
):
    consulta = text("""
        SELECT jogo_id, carta_id
        FROM jogo_cartas
        WHERE jogo_id = :jogo_id
          AND carta_id = :carta_id
    """)

    return db.execute(
        consulta,
        {
            "jogo_id": jogo_id,
            "carta_id": carta_id
        }
    ).mappings().first()


# Associar uma carta ao jogo
def associar_carta(
    db: Session,
    jogo_id: int,
    carta_id: int
):
    consulta = text("""
        INSERT INTO jogo_cartas (
            jogo_id,
            carta_id
        )
        VALUES (
            :jogo_id,
            :carta_id
        )
    """)

    db.execute(
        consulta,
        {
            "jogo_id": jogo_id,
            "carta_id": carta_id
        }
    )


# Remover a associação
def desassociar_carta(
    db: Session,
    jogo_id: int,
    carta_id: int
):
    consulta = text("""
        DELETE FROM jogo_cartas
        WHERE jogo_id = :jogo_id
          AND carta_id = :carta_id
    """)

    db.execute(
        consulta,
        {
            "jogo_id": jogo_id,
            "carta_id": carta_id
        }
    )