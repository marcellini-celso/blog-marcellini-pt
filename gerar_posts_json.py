"""Gera o índice canônico a partir do front matter YAML dos posts."""
import json
from datetime import date, datetime
from pathlib import Path
import yaml

POSTS_DIR = Path("posts")
SAIDA_JSON = Path("posts.json")

def extract_post_metadata(qmd_file):
    content = qmd_file.read_text(encoding="utf-8")
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        raise ValueError(f"Front matter sem fechamento: {qmd_file}")
    metadata = yaml.safe_load("\n".join(lines[1:end])) or {}
    if not isinstance(metadata, dict):
        raise ValueError(f"Front matter inválido: {qmd_file}")
    if metadata.get("draft") is True:
        return None
    title, tags = metadata.get("title"), metadata.get("tags")
    if not title or not tags:
        return None
    if not isinstance(title, str) or not isinstance(tags, list) or any(not isinstance(tag, str) for tag in tags):
        raise ValueError(f"Título ou tags inválidos: {qmd_file}")
    post = {"title": title, "href": qmd_file.with_suffix(".html").as_posix(),
            "tags": list(dict.fromkeys(tag.strip() for tag in tags if tag.strip()))}
    published = metadata.get("date")
    if published is not None:
        if isinstance(published, datetime):
            published = published.date()
        elif not isinstance(published, date):
            published = date.fromisoformat(str(published))
        post["date"] = published.isoformat()
    return post

def coletar_posts():
    return [post for path in sorted(POSTS_DIR.rglob("*.qmd"))
            if (post := extract_post_metadata(path)) is not None]

def salvar_json(posts):
    SAIDA_JSON.write_text(json.dumps(posts, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"✅ {len(posts)} posts salvos em {SAIDA_JSON}")

if __name__ == "__main__":
    salvar_json(coletar_posts())
