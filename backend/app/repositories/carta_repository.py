from sqlalchemy import text
from sqlalchemy.orm import Session


# Listar todas as cartas
def listar_cartas(db: Session):
    consulta = text("""
        SELECT
            id,
            jogo_origem_id,
            tipo,
            descricao,
            dificuldade,
            criado_em,
            atualizado_em
        FROM cartas
        ORDER BY id
    """)

    return db.execute(consulta).mappings().all()


# Buscar uma carta pelo ID
def buscar_carta(db: Session, carta_id: int):
    consulta = text("""
        SELECT *
        FROM cartas
        WHERE id = :carta_id
    """)

    return db.execute(
        consulta,
        {"carta_id": carta_id}
    ).mappings().first()


# Cadastrar uma nova carta
def cadastrar_carta(db: Session, dados: dict):
    consulta = text("""
        INSERT INTO cartas (
            jogo_origem_id,
            tipo,
            descricao,
            dificuldade
        )
        VALUES (
            :jogo_origem_id,
            :tipo,
            :descricao,
            :dificuldade
        )
    """)

    resultado = db.execute(consulta, dados)

    return resultado.lastrowid


# Editar uma carta existente
def atualizar_carta(
    db: Session,
    carta_id: int,
    dados: dict
):
    consulta = text("""
        UPDATE cartas
        SET
            jogo_origem_id = :jogo_origem_id,
            tipo = :tipo,
            descricao = :descricao,
            dificuldade = :dificuldade
        WHERE id = :carta_id
    """)

    db.execute(
        consulta,
        {**dados, "carta_id": carta_id}
    )


# Excluir uma carta
def excluir_carta(db: Session, carta_id: int):
    consulta = text("""
        DELETE FROM cartas
        WHERE id = :carta_id
    """)

    db.execute(
        consulta,
        {"carta_id": carta_id}
    )