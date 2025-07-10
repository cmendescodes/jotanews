# noticias/classification.py

def classificar(texto):
    """
    Classifica o texto da notícia com base em palavras-chave.
    Retorna: (categoria, subcategoria, lista_tags)
    """
    texto = texto.lower()
    tags = []

    # Categorias e palavras-chave associadas
    categorias = {
        'Tributos': ['imposto', 'ir', 'tributo', 'isenção fiscal', 'receita federal'],
        'Saúde': ['sus', 'vacina', 'hospital', 'médico', 'saúde pública'],
        'Trabalhista': ['clt', 'emprego', 'trabalho', 'reforma trabalhista'],
        'Poder': ['congresso', 'presidente', 'ministro', 'stf', 'senado', 'planalto'],
    }

    # Subcategorias opcionais
    subcategorias = {
        'Aposta da Semana': ['aposta da semana', 'expectativa', 'tendência'],
        'Matinal': ['boletim matinal', 'resumo matinal', 'informe da manhã'],
    }

    categoria_encontrada = None
    for categoria, palavras in categorias.items():
        if any(p in texto for p in palavras):
            categoria_encontrada = categoria
            tags.extend(p for p in palavras if p in texto)
            break

    subcategoria_encontrada = None
    for sub, palavras in subcategorias.items():
        if any(p in texto for p in palavras):
            subcategoria_encontrada = sub
            tags.extend(p for p in palavras if p in texto)
            break

    # Remover duplicatas das tags
    tags = list(set(tags))

    return categoria_encontrada or "Geral", subcategoria_encontrada, tags
