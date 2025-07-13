# Dicionários com palavras-chave para categorias e subcategorias
CATEGORIAS_KEYWORDS = {
    "Tributos": ["IR", "Imposto", "Fiscal", "Receita", "Tributo", "Isenção", "Congresso"],
    "Saúde": ["hospital", "vacina", "saúde", "SUS", "doença", "pandemia"],
    "Trabalhista": ["CLT", "trabalho", "sindicato", "emprego", "FGTS"],
    "Poder": ["Congresso", "STF", "presidente", "governo", "senado", "decreto"]
}

SUBCATEGORIAS_KEYWORDS = {
    "Aposta da Semana": ["aposta", "expectativa", "projeção", "semanal"],
    "Matinal": ["matinal", "resumo do dia", "manhã"]
}

def classificar(texto: str):
    """
    Recebe o texto (título + corpo) da notícia e retorna:
    - categoria (str ou None)
    - subcategoria (str ou None)
    - lista de tags (list de str)
    """
    texto_lower = texto.lower()
    categoria = None
    subcategoria = None
    tags = set()

    # Classificar categoria
    for cat, keywords in CATEGORIAS_KEYWORDS.items():
        if any(k.lower() in texto_lower for k in keywords):
            categoria = cat
            break

    # Classificar subcategoria
    for subcat, keywords in SUBCATEGORIAS_KEYWORDS.items():
        if any(k.lower() in texto_lower for k in keywords):
            subcategoria = subcat
            break

    # Tags: todos os keywords que aparecem, de todas categorias e subcategorias
    for keywords in list(CATEGORIAS_KEYWORDS.values()) + list(SUBCATEGORIAS_KEYWORDS.values()):
        for k in keywords:
            if k.lower() in texto_lower:
                tags.add(k)

    return categoria, subcategoria, sorted(tags)
