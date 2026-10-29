"""Atualiza os artigos e as aulas recentes a partir das datas dos posts."""
from datetime import date
from pathlib import Path
import re
from gerar_posts_json import coletar_posts

def _ordem_natural(caminho):
    return tuple((p.isdigit(), int(p) if p.isdigit() else p.lower())
                 for p in re.split(r"(\d+)", caminho))

def ultimos_posts(posts, quantidade=15, tipo=None):
    if tipo not in (None, "artigos", "aulas"):
        raise ValueError("Tipo de publicação inválido")
    candidates = [post for post in posts if post.get("date")
                  and Path(post["href"]).name != "index.html"
                  and not Path(post["href"]).name.startswith("guia-")
                  and not post["href"].endswith("-estatico.html")]
    if tipo is not None:
        candidates = [p for p in candidates
                      if p["href"].startswith("posts/cursos/") == (tipo == "aulas")]
    return sorted(candidates, key=lambda p: (p["date"], _ordem_natural(p["href"])),
                  reverse=True)[:quantidade]

def _area(post):
    path = post["href"]
    if "/programacao/ia/" in path:
        return "Inteligência Artificial"
    for pasta, nome in (("matematica", "Matemática"), ("estatistica", "Estatística"),
                        ("fisica", "Física"), ("programacao", "Programação"),
                        ("pessoal", "Blog Pessoal"), ("biografias", "Biografias")):
        if f"/{pasta}/" in path:
            return nome
    return "Blog"

def _lista(posts):
    if not posts:
        return "Novas leituras em preparação."
    entries = []
    for post in posts:
        title = post["title"].replace("[", "\\[").replace("]", "\\]")
        published = date.fromisoformat(post["date"]).strftime("%d/%m/%Y")
        entries.append(f'- [{title}]({post["href"]})  \n'
                       f'  [{_area(post)}]{{.home-topic}} · [{published}]{{.home-date}}')
    return "\n\n".join(entries)

def atualizar():
    index = Path("index.qmd")
    content = index.read_text(encoding="utf-8")
    start, end = "<!-- inicio-ultimos-posts -->", "<!-- fim-ultimos-posts -->"
    if content.count(start) != 1 or content.count(end) != 1 or content.index(start) > content.index(end):
        raise ValueError("Marcadores de últimos posts ausentes, duplicados ou invertidos")
    posts = coletar_posts()
    if not ultimos_posts(posts):
        raise ValueError("Nenhum post datado encontrado; índice preservado")
    articles = ultimos_posts(posts, quantidade=6, tipo="artigos")
    lessons = ultimos_posts(posts, quantidade=6, tipo="aulas")
    panels = ('::: {.home-updates}\n\n'
              '::: {.home-update-panel}\n\n'
              '### 📝 Artigos recentes {#artigos-recentes}\n\n'
              + _lista(articles) + '\n\n:::\n\n'
              '::: {.home-update-panel}\n\n'
              '### 🎓 Novas aulas {#novas-aulas}\n\n'
              + _lista(lessons) + '\n\n:::\n\n:::\n')
    replacement = start + "\n" + panels + "\n" + end
    content = re.sub(re.escape(start) + r".*?" + re.escape(end), lambda _: replacement, content, flags=re.S)
    index.write_text(content, encoding="utf-8")
    print(f"✅ Atualizados {len(articles)} artigos e {len(lessons)} aulas")

if __name__ == "__main__":
    atualizar()
