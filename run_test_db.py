from db import salvar_noticia, listar_noticias

noticia_exemplo = {
    "titulo": "STF aprova reforma tributária com novas regras de isenção",
    "corpo": "O Supremo Tribunal Federal definiu que a nova proposta de isenção será válida a partir de 2026.",
    "fonte": "Jota",
    "data_publicacao": "2025-07-11T12:30:00",
    "categoria": "Tributos",
    "subcategoria": "Aposta da Semana",
    "tags": ["STF", "isenção", "reforma tributária"]
}

salvar_noticia(noticia_exemplo)

print("📰 Últimas notícias:")
for noticia in listar_noticias():
    print("-", noticia["titulo"])
