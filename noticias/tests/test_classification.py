from noticias.classification import classificar

def test_classificar_tributos():
    texto = "Projeto de isenção do IR deve ser apresentado ao Congresso"
    categoria, subcategoria, tags = classificar(texto)
    assert categoria == "Tributos"
    assert "IR" in tags
    assert "Congresso" in tags

def test_classificar_saude():
    texto = "Novo hospital abre vagas para tratamento de doenças raras"
    categoria, subcategoria, tags = classificar(texto)
    assert categoria == "Saúde"
    assert "hospital" in tags

def test_classificar_com_subcategoria():
    texto = "Aposta da semana: mudanças no IR podem sair hoje"
    categoria, subcategoria, tags = classificar(texto)
    assert subcategoria == "Aposta da Semana"

def test_classificar_tags_variadas():
    texto = "Matinal: presidente anuncia novas regras para o FGTS"
    _, subcategoria, tags = classificar(texto)
    assert subcategoria == "Matinal"
    assert "FGTS" in tags
    assert "matinal" in tags
