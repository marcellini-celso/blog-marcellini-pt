#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
python3 atualizar_ultimos_posts.py
