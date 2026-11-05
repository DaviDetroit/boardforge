from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class JogoCriar(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    descricao: str | None = None
    tema: str | None = Field(default=None, max_length=100)
    quantidade_casas: int = Field(ge=20, le=100)


class JogoResposta(JogoCriar):
    id: int
    criado_em: datetime | None = None
    atualizado_em: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
