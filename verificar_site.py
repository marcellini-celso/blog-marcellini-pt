"""Confere os arquivos gerados antes da publicação."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json

class Referencias(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if value and (key == "src" or (key == "href" and tag in ("a", "link"))):
                self.links.append(value)

def verificar():
    root = Path("docs").resolve()
    errors = []
    source = Path("posts.json").read_bytes()
    if source != (root / "posts.json").read_bytes():
        errors.append("O índice publicado difere do índice canônico")
    for post in json.loads(source):
        if not (root / post["href"]).is_file():
            errors.append(f"Post não renderizado: {post['href']}")
    pages = list(root.rglob("*.html"))
    for page in pages:
        parser = Referencias()
        parser.feed(page.read_text(encoding="utf-8", errors="replace"))
        for link in parser.links:
            url = urlsplit(link)
            if url.scheme or url.netloc or not url.path:
                continue
            path = unquote(url.path)
            target = root / path.lstrip("/") if path.startswith("/") else page.parent / path
            if not target.exists():
                errors.append(f"{page.relative_to(root)}: destino ausente {link}")
    base = root / "posts/cursos/matematica/calculo/modulo-1"
    aliases = {
        "1.2-conjuntos-ap.html": "1.18-AP-conjuntos.html",
        "1.3-valor-absoluto-AP.html": "1.19-AP-valor-absoluto.html",
    }
    for old, new in aliases.items():
        path = base / old
        if not path.is_file() or new not in path.read_text():
            errors.append(f"Redirecionamento ausente ou incorreto: {old}")
    if errors:
        print("\n".join(sorted(set(errors))))
        return 1
    print(f"✅ {len(pages)} páginas verificadas; posts, recursos e redirecionamentos íntegros")
    return 0

if __name__ == "__main__":
    raise SystemExit(verificar())
