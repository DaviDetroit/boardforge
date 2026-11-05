from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database.connection import engine

from app.routers import jogos, casas



app = FastAPI(
    title="Jogo Tabuleiro API",
    description="API para gerenciamento de jogos de tabuleiro personalizados.",
    version="1.0.0"
)

app.include_router(jogos.router)
app.include_router(casas.router)


@app.get("/")
def inicio():
    return {
        "mensagem": "Bem-vindo à API do Jogo Tabuleiro!",
        "status": "online"
    }


@app.get("/teste-banco", tags=["Desenvolvimento"])
def teste_banco():
    try:
        with engine.connect() as conexao:
            resultado = conexao.execute(
                text("SELECT DATABASE() AS banco, VERSION() AS versao")
            ).mappings().one()

        return {
            "status": "conectado",
            "banco": resultado["banco"],
            "versao_mysql": resultado["versao"]
        }

    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Não foi possível conectar ao banco de dados."
        )
