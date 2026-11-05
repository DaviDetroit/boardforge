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


def distribuir_respeitando_fixadas(
    casas: list[Casa],
    tipos: list[str]
) -> list[str]:
    editaveis = [
        casa for casa in casas
        if not casa.fixada
        and casa.tipo not in ("inicio", "fim")
    ]
    if len(editaveis) != len(tipos):
        raise ValueError(
            "Quantidade de tipos diferente das casas editáveis."
        )
    tipos_restantes = tipos.copy()
    random.shuffle(tipos_restantes)
    # As posições fixadas são conhecidas desde o início.
    tipos_por_posicao = {
        casa.numero: casa.tipo
        for casa in casas
        if casa.fixada or casa.tipo in ("inicio", "fim")
    }
    resultado = []
    for casa in editaveis:
        candidatos = tipos_restantes.copy()
        random.shuffle(candidatos)
        escolhido = None
        for tipo in candidatos:
            if tipo == "normal":
                continue
            anterior = tipos_por_posicao.get(casa.numero - 1)
            anteanterior = tipos_por_posicao.get(casa.numero - 2)
            proximo = tipos_por_posicao.get(casa.numero + 1)
            posterior = tipos_por_posicao.get(casa.numero + 2)
            # Verifica trios que incluem a posição atual.
            conflitos = (
                anterior not in (None, "normal", "inicio", "fim")
                and anteanterior not in (None, "normal", "inicio", "fim")
            ) or (
                anterior not in (None, "normal", "inicio", "fim")
                and proximo not in (None, "normal", "inicio", "fim")
            ) or (
                proximo not in (None, "normal", "inicio", "fim")
                and posterior not in (None, "normal", "inicio", "fim")
            )
            if not conflitos:
                escolhido = tipo
                break
        if escolhido is None:
            escolhido = next(
                (tipo for tipo in tipos_restantes if tipo == "normal"),
                tipos_restantes[0]
            )
        tipos_restantes.remove(escolhido)
        tipos_por_posicao[casa.numero] = escolhido
        resultado.append(escolhido)
    return resultado


def regenerar_casas(casas: list[Casa]) -> list[Casa]:
    """
    Regenera as casas não fixadas de um tabuleiro,
    preservando início, fim e casas fixadas.
    """

    casas_ordenadas = sorted(
        casas,
        key=lambda casa: casa.numero
    )

    quantidade = len(casas_ordenadas)

    if not 20 <= quantidade <= 100:
        raise ValueError(
            "O tabuleiro deve ter entre 20 e 100 casas."
        )

    # Identifica quais casas podem ser regeneradas.
    editaveis = [
        casa for casa in casas_ordenadas
        if not casa.fixada
        and casa.tipo not in ("inicio", "fim")
    ]

    if not editaveis:
        return casas_ordenadas

    # Calcula a distribuição ideal para as casas intermediárias.
    distribuicao_ideal = distribuir_tipos(quantidade - 2)

    quantidades = {
        tipo: distribuicao_ideal.count(tipo)
        for tipo in PROPORCOES
    }

    # Desconta as casas que já estão fixadas.
    for casa in casas_ordenadas:
        if casa.fixada and casa.tipo in quantidades:
            quantidades[casa.tipo] = max(
                0,
                quantidades[casa.tipo] - 1
            )

    # Monta os tipos disponíveis para regeneração.
    tipos = []

    for tipo, total in quantidades.items():
        tipos.extend([tipo] * total)

    # Ajusta a quantidade caso as casas fixadas
    # ultrapassem a proporção originalmente prevista.
    if len(tipos) > len(editaveis):
        random.shuffle(tipos)
        tipos = tipos[:len(editaveis)]

    elif len(tipos) < len(editaveis):
        tipos.extend(
            ["normal"] * (len(editaveis) - len(tipos))
        )

    tipos = distribuir_respeitando_fixadas(
        casas_ordenadas,
        tipos
    )

    dificuldades = distribuir_valores(
        ["facil", "media", "dificil"],
        tipos.count("tarefa")
    )

    niveis_explosao = distribuir_valores(
        [1, 2, 3, 4],
        tipos.count("explosao")
    )

    # Atualiza apenas as casas não fixadas.
    for casa, tipo in zip(editaveis, tipos):
        casa.tipo = tipo
        casa.dificuldade = None
        casa.nivel_explosao = None
        casa.texto_acao = None
        casa.tipo_movimento = "nenhum"
        casa.quantidade_movimento = 0

        if tipo == "tarefa":
            casa.dificuldade = dificuldades.pop()

        elif tipo == "explosao":
            casa.nivel_explosao = niveis_explosao.pop()

    return casas_ordenadas
