from sqlalchemy import BigInteger, DateTime, String, Text, SmallInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Jogo(Base):
    __tablename__ = "jogos"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    nome: Mapped[str] = mapped_column(String(100))
    descricao: Mapped[str | None] = mapped_column(Text)
    tema: Mapped[str | None] = mapped_column(String(100))
    quantidade_casas: Mapped[int] = mapped_column(SmallInteger)

    criado_em: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    atualizado_em: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now()
    )
