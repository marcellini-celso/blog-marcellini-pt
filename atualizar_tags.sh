#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "$0")"

# Caminhos
TAGS_FREQ="tags_freq.txt"
ARQUIVO_TAGS="tags.qmd"
PASTA_TAGS="tags"
NUVEM_SCRIPT="nuvem_tags.py"
POSTS_JSON="posts.json"
SCRIPT_TEMP="gerar_paginas_de_tags_temp.py"

# Garante que a pasta de tags existe
mkdir -p "$PASTA_TAGS"
python3 gerar_tags.py

# Início do arquivo tags.qmd
echo -e "---\ntitle: \"Tags\"\nformat: html\npage-layout: full\n---\n" > "$ARQUIVO_TAGS"
echo -e "::: {.tag-nuvem}\n![](nuvem_tags.png){width=100%}\n:::\n" >> "$ARQUIVO_TAGS"
echo -e "## 📚 Todas as Tags\n\n::: {.tag-grid}\n" >> "$ARQUIVO_TAGS"

# Geração dos links de tags
while read -r linha; do
  freq=$(echo "$linha" | awk '{print $1}')
  tag=$(echo "$linha" | cut -d' ' -f2-)
  slug=$(echo "$tag" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g' | sed 's/[ç]/c/g' | iconv -f utf8 -t ascii//TRANSLIT)
  echo "<a href=\"/tags/$slug.html\" class=\"tag-card\">$tag ($freq)</a>" >> "$ARQUIVO_TAGS"
done < "$TAGS_FREQ"

echo -e ":::" >> "$ARQUIVO_TAGS"

# Gera a nuvem de tags
python3 "$NUVEM_SCRIPT"

# Script Python temporário para gerar páginas por tag com links absolutos
cat << 'EOF' > "$SCRIPT_TEMP"
import json
from pathlib import Path
from collections import defaultdict
import unicodedata

ARQUIVO_JSON = Path("posts.json")
PASTA_TAGS = Path("tags")

def slugify(tag):
    tag = tag.lower().replace(" ", "-").replace("ç", "c")
    tag = unicodedata.normalize("NFKD", tag).encode("ascii", "ignore").decode("ascii")
    return tag

def carregar_posts():
    with open(ARQUIVO_JSON, encoding="utf-8") as f:
        return json.load(f)

def agrupar_por_tag(posts):
    tags_dict = defaultdict(list)
    for post in posts:
        for tag in post["tags"]:
            tags_dict[tag].append({
                "title": post["title"],
                "href": post["href"]
            })
    return tags_dict

def gerar_paginas(tags_dict):
    PASTA_TAGS.mkdir(exist_ok=True)
    for tag, posts in tags_dict.items():
        slug = slugify(tag)
        caminho = PASTA_TAGS / f"{slug}.qmd"
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(f"---\ntitle: \"{tag}\"\nformat: html\n---\n\n")
            f.write("[⬅ Voltar para Todas as Tags](../tags.qmd)\n\n")
            f.write(f"## Posts com a tag **{tag}**\n\n")
            for post in posts:
                f.write(f"- [{post['title']}](/{post['href']})\n")
        print(f"✅ Página gerada: {caminho}")

if __name__ == "__main__":
    posts = carregar_posts()
    tags = agrupar_por_tag(posts)
    gerar_paginas(tags)
EOF

# Executa o script Python temporário
python3 "$SCRIPT_TEMP"

# Remove o script temporário
rm "$SCRIPT_TEMP"
