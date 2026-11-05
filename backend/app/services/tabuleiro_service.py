from app.database.models import Casa


def gerar_casas_iniciais(
    jogo_id: int,
    quantidade_casas: int
) -> list[Casa]:

    if not 20 <= quantidade_casas <= 100:
        raise ValueError(
            "O tabuleiro deve ter entre 20 e 100 casas."
        )

    casas = []

    for numero in range(1, quantidade_casas + 1):

        if numero == 1:
            tipo = "inicio"

        elif numero == quantidade_casas:
            tipo = "fim"

        else:
            tipo = "normal"

        casa = Casa(
            jogo_id=jogo_id,
            numero=numero,
            tipo=tipo,
            dificuldade=None,
            nivel_explosao=None,
            fixada=False,
            texto_acao=None,
            tipo_movimento="nenhum",
            quantidade_movimento=0
        )

        casas.append(casa)

    return casas
