from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    SmallInteger,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Classe base para os modelos do banco
class Base(DeclarativeBase):
    pass


# Tabela de jogos
class Jogo(Base):
    __tablename__ = "jogos"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    nome: Mapped[str] = mapped_column(String(100), nullable=False)

    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)

    tema: Mapped[str | None] = mapped_column(String(100), nullable=True)

    quantidade_casas: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False
    )

    criado_em: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )


# Tabela de casas do tabuleiro
class Casa(Base):
    __tablename__ = "casas"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    jogo_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("jogos.id", ondelete="CASCADE"),
        nullable=False
    )

    numero: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False
    )

    tipo: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    dificuldade: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True
    )

    nivel_explosao: Mapped[int | None] = mapped_column(
        SmallInteger,
        nullable=True
    )

    fixada: Mapped[bool] = mapped_column(
        default=False,
        nullable=False
    )

    texto_acao: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    tipo_movimento: Mapped[str] = mapped_column(
        String(10),
        default="nenhum",
        nullable=False
    )

    quantidade_movimento: Mapped[int] = mapped_column(
        SmallInteger,
        default=0,
        nullable=False
    )
