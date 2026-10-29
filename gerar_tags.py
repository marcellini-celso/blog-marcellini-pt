import unicodedata
import json
from collections import Counter
from pathlib import Path

ARQUIVO_JSON = "posts.json"
ARQUIVO_FREQ = "tags_freq.txt"
ARQUIVO_QMD = "tags.qmd"
ARQUIVO_HTML = "lista_tags_gerada.html"

def carregar_tags(arquivo_json):
    tags = []
    with open(arquivo_json, encoding="utf-8") as f:
        posts = json.load(f)
        for post in posts:
            tags_unicas = set()
            for tag in post.get("tags", []):
                tag_norm = unicodedata.normalize("NFC", tag.strip())
                tags_unicas.add(tag_norm)
            tags.extend(tags_unicas)
    return tags

    tags = []
    with open(arquivo_json, encoding="utf-8") as f:
        posts = json.load(f)
        for post in posts:
            tags.extend(post.get("tags", []))
    return tags

def gerar_relatorios(tags):
    contagem = Counter(tags)
    # Ordenar por frequência decrescente, depois alfabética
    ordenadas = sorted(contagem.items(), key=lambda x: (-x[1], x[0]))

    # Gerar tags_freq.txt
    with open(ARQUIVO_FREQ, "w", encoding="utf-8") as f:
        for tag, freq in ordenadas:
            f.write(f"{freq} {tag}\n")

    # Gerar tags.qmd
    with open(ARQUIVO_QMD, "w", encoding="utf-8") as f:
        f.write("# Tags\n\n")
        for tag, freq in ordenadas:
            f.write(f"- **{tag}** ({freq})\n")

    # Gerar lista_tags_gerada.html
    with open(ARQUIVO_HTML, "w", encoding="utf-8") as f:
        f.write("<html><head><meta charset='utf-8'><title>Tags</title></head><body>\n")
        f.write("<h1>Lista de Tags</h1>\n<ul>\n")
        for tag, freq in ordenadas:
            f.write(f"<li><b>{tag}</b> ({freq})</li>\n")
        f.write("</ul></body></html>\n")

if __name__ == "__main__":
    tags = carregar_tags(ARQUIVO_JSON)
    if not tags:
        print("❌ Nenhuma tag encontrada.")
    else:
        gerar_relatorios(tags)
        print("✅ Arquivos de tags gerados com sucesso.")