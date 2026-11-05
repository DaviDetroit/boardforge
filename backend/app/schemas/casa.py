from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


TipoCasa = Literal[
    "normal",
    "inicio",
    "fim",
    "tarefa",
    "duelo",
    "explosao",
    "escudo",
    "prisao",
    "troca",
]

Dificuldade = Literal["facil", "media", "dificil"]
TipoMovimento = Literal["nenhum", "avancar", "voltar"]


class CasaEditar(BaseModel):
    tipo: TipoCasa
    dificuldade: Dificuldade | None = None
    nivel_explosao: int | None = Field(default=None, ge=1, le=4)
    texto_acao: str | None = None
    tipo_movimento: TipoMovimento = "nenhum"
    quantidade_movimento: int = Field(default=0, ge=0, le=99)
    fixada: bool = False

    @model_validator(mode="after")
    def validar_casa(self):
        if self.tipo in ("inicio", "fim"):
            raise ValueError(
                "Início e fim não podem ser definidos manualmente."
            )

        if self.tipo == "tarefa":
            if self.dificuldade is None:
                raise ValueError(
                    "Casas de tarefa precisam de uma dificuldade."
                )

        elif self.dificuldade is not None:
            raise ValueError(
                "Somente casas de tarefa possuem dificuldade."
            )

        if self.tipo == "explosao":
            if self.nivel_explosao is None:
                raise ValueError(
                    "Casas de explosão precisam de um nível."
                )

        elif self.nivel_explosao is not None:
            raise ValueError(
                "Somente explosões possuem nível."
            )

        if self.tipo_movimento == "nenhum":
            if self.quantidade_movimento != 0:
                raise ValueError(
                    "Movimento 'nenhum' exige quantidade zero."
                )
        else:
            if self.tipo != "normal":
                raise ValueError(
                    "Movimentos personalizados só são permitidos "
                    "em casas normais."
                )

            if self.quantidade_movimento < 1:
                raise ValueError(
                    "Informe quantas casas avançar ou voltar."
                )

            if not self.texto_acao or not self.texto_acao.strip():
                raise ValueError(
                    "Movimento personalizado exige texto de ação."
                )

        if self.tipo != "normal" and self.texto_acao is not None:
            raise ValueError(
                "Texto de ação personalizado só é permitido "
                "em casas normais."
            )

        return self


class CasaResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    jogo_id: int
    numero: int
    tipo: TipoCasa
    dificuldade: Dificuldade | None
    nivel_explosao: int | None
    texto_acao: str | None
    tipo_movimento: TipoMovimento
    quantidade_movimento: int
    fixada: bool
