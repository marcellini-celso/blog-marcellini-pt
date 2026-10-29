# Blog do Marcellini

Blog pessoal de Celso Marcellini sobre Matemática, Estatística, Física e Programação, com explicações didáticas, exemplos em R/Python e tipografia matemática.

🌐 **[Acesse o Blog do Marcellini](https://blogdomarcellini.com.br/)**

## Conteúdo

- [Curso de Cálculo Diferencial e Integral](https://blogdomarcellini.com.br/posts/cursos/matematica/calculo/index.html): Módulo 1 com 17 aulas principais e 6 aprofundamentos; demais módulos em construção.
- [Curso sobre a Distribuição Normal](https://blogdomarcellini.com.br/posts/cursos/estatistica/distribuicao_normal/index.html).
- [Física, História e Epistemologia](https://blogdomarcellini.com.br/posts/fisica/historia-epistemologia/index.html).
- [Inteligência Artificial](https://blogdomarcellini.com.br/posts/programacao/ia/index.html).
- [Modelos e templates de Quarto](https://blogdomarcellini.com.br/posts/programacao/quarto/modelos-hub.html).

## Ferramentas

O site usa Quarto e GitHub Pages, com saída em `docs/`, tema `cosmo` e estilos em `styles.css` e `assets/css/`. A publicação no Pages acompanha a branch `main`.

O ambiente precisa de Quarto, Python 3, PyYAML, matplotlib e wordcloud. Os exemplos executáveis também usam R/Python e os respectivos pacotes; mantenha as dependências dos artigos instaladas no ambiente de renderização.

## Atualizar e conferir

O ambiente habitual está em /home/celso/.env. Na raiz do projeto:

```bash
source ./ambiente-blog.sh
```

O auxiliar usa o ambiente ativo ou $HOME/.env, com .venv local como alternativa. Para selecionar outro ambiente, defina BLOG_PYTHON_ENV. Em outra máquina, crie um ambiente virtual e instale requirements.txt.

Depois, atualize e confira:

```bash
bash atualizar_tudo.sh
python3 -m unittest discover -s tests -v
quarto render
python3 verificar_site.py
quarto preview
```

`atualizar_tudo.sh` atualiza os últimos posts, gera o índice, atualiza tags e valida a integridade. Os metadados vêm do front matter YAML dos arquivos `.qmd`; use datas ISO (`AAAA-MM-DD`) e `draft: true` para textos que não devem entrar nos índices. Arquivos novos entram na seleção sem precisar de um commit prévio.

`posts.json` na raiz é o índice canônico gerado por `gerar_posts_json.py`; Quarto o copia para `docs/posts.json` como recurso. Os geradores de tags leem a versão da raiz. Não edite o JSON manualmente. Empates de data na lista de últimos posts são resolvidos pelo caminho do arquivo, de forma determinística.

Os aprofundamentos 1.18-AP e 1.19-AP preservam suas URLs anteriores por meio de `aliases` nos metadados Quarto.

## Publicar

Confira as diferenças e os arquivos novos antes de publicar:

```bash
git status --short
git diff
bash publicar-blog.sh "Atualiza o blog e o Módulo 1 de Cálculo"
```

O script exige `main`, verifica se o remoto avançou, atualiza os índices, renderiza o site, confere o JSON gerado e registra as alterações antes do push. Ele interrompe a publicação quando uma etapa falha. Arquivos já preparados para commit devem ser revisados e tratados antes de executar o script. Novos arquivos fora dos padrões previstos devem ser adicionados explicitamente ao fluxo.

Após o push, acompanhe a execução em [GitHub Actions](https://github.com/marcellini-celso/blog-marcellini-pt/actions) e confira o blog publicado.

## Contato

[prof.marcellini@gmail.com](mailto:prof.marcellini@gmail.com)
