"""Atualiza os últimos posts com datas normalizadas, incluindo arquivos novos."""
from pathlib import Path
import re
from gerar_posts_json import coletar_posts

def ultimos_posts(posts, quantidade=15):
    candidates = [post for post in posts if post.get("date")
                  and Path(post["href"]).name != "index.html"
                  and not Path(post["href"]).name.startswith("guia-")
                  and not post["href"].endswith("-estatico.html")]
    return sorted(candidates, key=lambda post: (post["date"], post["href"]), reverse=True)[:quantidade]

def atualizar():
    index = Path("index.qmd")
    content = index.read_text(encoding="utf-8")
    start, end = "<!-- inicio-ultimos-posts -->", "<!-- fim-ultimos-posts -->"
    if content.count(start) != 1 or content.count(end) != 1 or content.index(start) > content.index(end):
        raise ValueError("Marcadores de últimos posts ausentes, duplicados ou invertidos")
    posts = ultimos_posts(coletar_posts())
    if not posts:
        raise ValueError("Nenhum post datado encontrado; índice preservado")
    def link(post):
        title = post["title"].replace("[", "\\[").replace("]", "\\]")
        return f"- [{title}]({post['href']})"
    replacement = start + "\n" + "\n".join(map(link, posts)) + "\n\n" + end
    content = re.sub(re.escape(start) + r".*?" + re.escape(end), lambda _: replacement, content, flags=re.S)
    index.write_text(content, encoding="utf-8")
    print(f"✅ Últimos {len(posts)} posts atualizados")

if __name__ == "__main__":
    atualizar()
