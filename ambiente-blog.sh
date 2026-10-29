#!/bin/bash
# Prefere um ambiente explicitamente selecionado ou o ambiente habitual do usuário.
BLOG_PYTHON_ENV="${BLOG_PYTHON_ENV:-${VIRTUAL_ENV:-$HOME/.env}}"
if [[ ! -f "$BLOG_PYTHON_ENV/bin/activate" && -f .venv/bin/activate ]]; then
  BLOG_PYTHON_ENV="$PWD/.venv"
fi
if [[ -f "$BLOG_PYTHON_ENV/bin/activate" ]]; then
  source "$BLOG_PYTHON_ENV/bin/activate"
  export QUARTO_PYTHON="$BLOG_PYTHON_ENV/bin/python"
  export RETICULATE_PYTHON="$QUARTO_PYTHON"
fi
