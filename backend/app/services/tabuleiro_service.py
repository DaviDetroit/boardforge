import random

from app.database.models import Casa


PROPORCOES = {
    "normal": 0.40,
    "tarefa": 0.20,
    "duelo": 0.12,
    "explosao": 0.12,
    "escudo": 0.06,
    "prisao": 0.05,
    "troca": 0.05,
}


def distribuir_com_espacamento(tipos: list[str]) -> list[str]:
    """
    Distribui casas especiais evitando três consecutivas,
    sempre que houver casas normais suficientes.
    """
    normais = tipos.count("normal")
    especiais = [tipo for tipo in tipos if tipo != "normal"]
    random.shuffle(especiais)

    # As casas normais criam espaços para distribuir especiais.
    grupos = [[] for _ in range(normais + 1)]

    # Cada grupo pode conter até duas casas especiais.
    capacidade = 2 * len(grupos)
    if len(especiais) > capacidade:
        # Não é possível garantir o espaçamento.
        # Mantém a distribuição aleatória.
        resultado = tipos.copy()
        random.shuffle(resultado)
        return resultado

    # Distribui as especiais entre os grupos disponíveis.
    for especial in especiais:
        disponiveis = [
            grupo for grupo in grupos
            if len(grupo) < 2
        ]
        menor_tamanho = min(len(grupo) for grupo in disponiveis)
        candidatos = [
            grupo for grupo in disponiveis
            if len(grupo) == menor_tamanho
        ]
        random.choice(candidatos).append(especial)

    # Intercala os grupos com casas normais.
    resultado = []
    for indice, grupo in enumerate(grupos):
        resultado.extend(grupo)
        if indice < normais:
            resultado.append("normal")
    return resultado


def distribuir_tipos(quantidade: int) -> list[str]:
    """
    Distribui os tipos de casas proporcionalmente.
    """
    tipos = []

    quantidades = {
        tipo: int(quantidade * proporcao)
        for tipo, proporcao in PROPORCOES.items()
    }

    restantes = quantidade - sum(quantidades.values())

    # Distribui as casas que sobraram pelos maiores restos.
    restos = sorted(
        PROPORCOES,
        key=lambda tipo: quantidade * PROPORCOES[tipo]
        - quantidades[tipo],
        reverse=True
    )

    for tipo in restos[:restantes]:
        quantidades[tipo] += 1

    for tipo, total in quantidades.items():
        tipos.extend([tipo] * total)

    tipos = distribuir_com_espacamento(tipos)

    return tipos

def distribuir_valores(
    valores: list,
    quantidade: int
) -> list:
    """
    Distribui valores de forma equilibrada,
    mantendo uma ordem aleatória.
    """
    resultado = []

    for indice in range(quantidade):
        resultado.append(valores[indice % len(valores)])

    random.shuffle(resultado)

    return resultado


def gerar_casas_iniciais(
    jogo_id: int,
    quantidade_casas: int
) -> list[Casa]:

    if not 20 <= quantidade_casas <= 100:
        raise ValueError(
            "O tabuleiro deve ter entre 20 e 100 casas."
        )

    quantidade_intermediarias = quantidade_casas - 2

    tipos = distribuir_tipos(quantidade_intermediarias)
    dificuldades = distribuir_valores(
        ["facil", "media", "dificil"],
        tipos.count("tarefa")
    )
    niveis_explosao = distribuir_valores(
        [1, 2, 3, 4],
        tipos.count("explosao")
    )

    casas = []

    for numero in range(1, quantidade_casas + 1):

        if numero == 1:
            tipo = "inicio"

        elif numero == quantidade_casas:
            tipo = "fim"

        else:
            tipo = tipos[numero - 2]

        dificuldade = None
        nivel_explosao = None

        if tipo == "tarefa":
            dificuldade = dificuldades.pop()

        elif tipo == "explosao":
            nivel_explosao = niveis_explosao.pop()

        casa = Casa(
            jogo_id=jogo_id,
            numero=numero,
            tipo=tipo,
            dificuldade=dificuldade,
            nivel_explosao=nivel_explosao,
            fixada=False,
            texto_acao=None,
            tipo_movimento="nenhum",
            quantidade_movimento=0
        )

        casas.append(casa)

    return casas
