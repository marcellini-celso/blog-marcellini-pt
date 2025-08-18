# Blog do Marcellini

Este é o repositório do meu blog pessoal, criado com [Quarto](https://quarto.org/). Aqui compartilho conteúdos sobre estatística, matemática, programação e física, com foco em explicações didáticas e exemplos práticos.

This is the repository for my personal blog, created with [Quarto](https://quarto.org/). Here, I share content on statistics, mathematics, programming, and physics, with a focus on clear explanations and practical examples.

---

## 📚 Publicações em destaque

- [📘 🧮 A Beleza é o Primeiro Teste — G. H. Hardy e a Matemática como Arte](https://blogdomarcellini.com.br/posts/matematica/beleza-matematica.html)
- [📘 🧮 Por que \( 0! = 1 \)?](https://blogdomarcellini.com.br/posts/matematica/fatorial-zero.html)
- [📘 🧬 100 Anos da Mecânica Quântica (1925-2025)](https://blogdomarcellini.com.br/posts/fisica/100-anos-mecanica-quantica.html)
- [🧭 📚 🧬 Guia de Leitura da Série 100 Anos da Mecânica Quântica](https://blogdomarcellini.com.br/posts/fisica/guia-100-anos-mecanica-quantica.html)
- [🎓 📊 Curso de Estatística: A Distribuição Normal (Parte 1)](https://blogdomarcellini.com.br/posts/estatistica/distribuicao-normal.html)
- [📘 👨‍💻 📄 Modelo de Markdown com Quarto – Parte 2](https://blogdomarcellini.com.br/posts/programacao/outros-modelos-markdown.html)

---

## ⚙️ Como este blog foi feito

- Desenvolvido com [Quarto](https://quarto.org/)
- Publicado via **GitHub Pages**
- Códigos escritos em **R**, **Python** e **LaTeX**
- Tema: `cosmo`, com ajustes em `styles.css`

---

## 🚀 Fluxo de trabalho para atualizar e publicar um post

### 1. Atualizar conteúdo localmente
Execute o script de atualização completo:

```bash
./atualizar_tudo.sh
```

Esse script executa:
- `atualizar-ultimos-posts.sh`
- `gerar_posts_json.py`
- `atualizar_tags.sh`

### 2. Visualizar no navegador local

```bash
quarto preview
```

Confirme se o post aparece corretamente, com tags e layout funcionando.

### 3. Publicar no GitHub Pages

```bash
./publicar-blog.sh
```

Esse script realiza:
- `quarto render` com saída na pasta `docs/`
- `git add` dos arquivos relevantes
- `git commit` com mensagem personalizada
- `git push` para a branch `main`

Após isso, o GitHub Pages atualizará automaticamente o site publicado.

---

## 🧱 Navegação por Tags

O blog possui um sistema automatizado para geração de páginas de tags, nuvem de palavras e navegação visual.

### Scripts mantidos

- `gerar_posts_json.py`: extrai `title`, `tags`, `href` dos posts `.qmd` e salva em `docs/posts.json`
- `nuvem_tags.py`: gera a imagem `nuvem_tags.png` com base em `tags_freq.txt`
- `atualizar_tags.sh`: script completo que:
  - Gera `tags.qmd` com visual limpo
  - Cria `tags/*.qmd` com os posts de cada tag
  - Adiciona botão de retorno para `tags.qmd` em cada página de tag
  - Gera a imagem da nuvem

### Scripts substituídos (podem ser removidos)

- `gerar_paginas_de_tags.py`

### Como usar (fluxo manual alternativo)

1. Gere `posts.json` com:

```bash
python3 gerar_posts_json.py
```

2. Execute o script principal:

```bash
chmod +x atualizar_tags.sh
./atualizar_tags.sh
```

3. Renderize o blog normalmente:

```bash
quarto render
```

---

## 🎨 Estilo

- CSS personalizado em: `assets/css/custom.css`
- Adicionado no `_quarto.yml`:

```yaml
format:
  html:
    css:
      - styles.css
      - assets/css/custom.css
```

---

## 🌐 Acesse o blog

➡️ [https://marcellini-celso.github.io/blog-marcellini-pt/](https://marcellini-celso.github.io/blog-marcellini-pt/)

➡️ [https://blogdomarcellini.com.br)

---

## 📬 Contato

Para dúvidas, sugestões ou colaborações, entre em contato por e-mail:  
✉️ **[prof.marcellini@gmail.com](mailto:prof.marcellini@gmail.com)**
# blog-marcellini-pt
Teste seg 18 ago 2025 05:41:50 -03
Teste seg 18 ago 2025 05:59:32 -03
