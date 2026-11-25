from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class CartaCriar(BaseModel):
    jogo_origem_id: int | None = Field(default=None, gt=0)

    tipo: Literal["tarefa", "duelo"]

    descricao: str = Field(min_length=1)

    dificuldade: Literal[
        "facil", "media", "dificil"
    ] | None = None

    @model_validator(mode="after")
    def validar_configuracao(self):
        if self.tipo == "tarefa" and self.dificuldade is None:
            raise ValueError(
                "Uma tarefa deve possuir dificuldade."
            )

        if self.tipo == "duelo" and self.dificuldade is not None:
            raise ValueError(
                "Um duelo não deve possuir dificuldade."
            )

        return self


class CartaEditar(CartaCriar):
    pass


class CartaResposta(CartaCriar):
    id: int
    criado_em: datetime
    atualizado_em: datetime