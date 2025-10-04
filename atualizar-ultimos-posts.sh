#!/bin/bash

# Número de posts mais recentes a listar
NUM_POSTS=10
echo "🔍 Procurando os $NUM_POSTS posts mais recentes com metadados válidos..."

# Arquivo temporário para armazenar os candidatos válidos
TMP_CANDIDATOS=$(mktemp)
TMP_LISTA=$(mktemp)

# Etapa 1: Filtrar apenas arquivos válidos
find posts -name '*.qmd' ! -name '*-estatico.qmd' -type f | while read -r FILE; do
  TITLE=$(grep -m 1 '^title:' "$FILE" | sed -E 's/^title:[[:space:]]*["'\'']?([^"'\'']+)["'\'']?/\1/')
  DATE=$(grep -m 1 '^date:' "$FILE" | sed -E 's/^date:[[:space:]]*//')

  if [[ -z "$TITLE" ]]; then
    echo "⚠️  Ignorando $FILE (sem título)"
    continue
  fi

  if [[ -z "$DATE" ]]; then
    echo "⚠️  Ignorando $FILE (sem data)"
    continue
  fi

  echo "✅ Incluído: $FILE | $DATE | $TITLE"
  echo "$DATE|$TITLE|$FILE" >> "$TMP_CANDIDATOS"
done

# Etapa 2: Ordenar por data (decrescente) e gerar lista
sort -r "$TMP_CANDIDATOS" | head -n "$NUM_POSTS" | while IFS='|' read -r DATE TITLE FILE; do
  LINK=${FILE%.qmd}.html
  echo "- [$TITLE]($LINK)"
done > "$TMP_LISTA"

# Etapa 3: Substituir no index.qmd o bloco entre as marcações
awk -v new="$(cat "$TMP_LISTA")" '
  /<!-- inicio-ultimos-posts -->/ {
    print
    print new
    in_block=1
    next
  }
  /<!-- fim-ultimos-posts -->/ { in_block=0 }
  !in_block
' index.qmd > index_temp.qmd && mv index_temp.qmd index.qmd

# Limpeza
rm "$TMP_CANDIDATOS" "$TMP_LISTA"

echo "✅ Últimos posts atualizados com sucesso no index.qmd"

