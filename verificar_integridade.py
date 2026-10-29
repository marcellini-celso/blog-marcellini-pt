"""Valida o índice canônico antes de renderizar ou publicar."""
import json
from datetime import date
from pathlib import Path

ARQUIVO_JSON = Path("posts.json")

def carregar_posts():
    return json.loads(ARQUIVO_JSON.read_text(encoding="utf-8"))

def verificar_integridade(posts):
    erros, seen = [], set()
    if not isinstance(posts, list) or not posts:
        return ["Índice vazio ou inválido"]
    for post in posts:
        caminho = post.get("href", "")
        if not post.get("title") or not post.get("tags"):
            erros.append(f"Título ou tags ausentes: {caminho}")
        if not caminho or not Path(caminho).with_suffix(".qmd").is_file():
            erros.append(f"Fonte ausente: {caminho}")
        if caminho in seen:
            erros.append(f"Endereço duplicado: {caminho}")
        seen.add(caminho)
        if post.get("date"):
            try:
                date.fromisoformat(post["date"])
            except (ValueError, TypeError):
                erros.append(f"Data inválida: {caminho}")
    return erros

def main():
    try:
        erros = verificar_integridade(carregar_posts())
    except (OSError, ValueError, TypeError) as error:
        print(f"❌ {error}")
        return 1
    if erros:
        print("\n".join(erros))
        return 1
    print("✅ Índice de posts íntegro")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
