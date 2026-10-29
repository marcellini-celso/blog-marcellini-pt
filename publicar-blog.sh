#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
source ./ambiente-blog.sh
if [[ $# -ne 1 || -z "$1" ]]; then
  echo 'Uso: ./publicar-blog.sh "Mensagem do commit"' >&2
  exit 1
fi
if [[ "$(git branch --show-current)" != main ]]; then
  echo 'A publicação deve partir da branch main.' >&2
  exit 1
fi
git diff --cached --quiet || { echo 'Há arquivos já preparados para commit; revise-os antes de publicar.' >&2; exit 1; }
git fetch origin main
git merge-base --is-ancestor origin/main HEAD || { echo 'A branch remota avançou. Integre as alterações antes de publicar.' >&2; exit 1; }
bash atualizar_tudo.sh
python3 -m unittest discover -s tests -v
quarto render
python3 verificar_integridade.py
cmp posts.json docs/posts.json
python3 verificar_site.py
# Inclui arquivos existentes e apenas as fontes/saídas previstas do blog.
git add -u
git add -- index.qmd posts.json tags.qmd tags_freq.txt nuvem_tags.png docs tags \
  gerar_posts_json.py atualizar_ultimos_posts.py atualizar-ultimos-posts.sh \
  gerar_tags.py atualizar_tags.sh atualizar_tudo.sh verificar_integridade.py \
  publicar-blog.sh ambiente-blog.sh README.md requirements.txt verificar_site.py tests
git add -- ':(glob)posts/**/*.qmd' ':(glob)posts/**/*.png' ':(glob)posts/**/*.svg' \
  ':(glob)posts/**/*.jpg' ':(glob)posts/**/*.jpeg'
if git diff --cached --quiet; then
  echo 'Nenhuma alteração para publicar.'
  exit 0
fi
git diff --cached --stat
git commit -m "$1"
git push origin HEAD:main
