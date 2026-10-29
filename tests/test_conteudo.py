import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from gerar_posts_json import extract_post_metadata, coletar_posts
from atualizar_ultimos_posts import ultimos_posts, atualizar
from verificar_integridade import verificar_integridade

class ConteudoTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.before = Path.cwd()
        os.chdir(self.temp.name)
        Path("posts").mkdir()

    def tearDown(self):
        os.chdir(self.before)
        self.temp.cleanup()

    def post(self, name, metadata):
        path = Path("posts") / name
        path.write_text("---\n" + metadata + "\n---\nTexto", encoding="utf-8")
        return path

    def test_datas_com_e_sem_aspas_e_arquivo_novo(self):
        self.post("antigo.qmd", "title: Antigo\ntags: [curso]\ndate: 2026-05-31")
        self.post("novo.qmd", "title: Novo\ntags: [curso]\ndate: '2026-06-05'")
        result = ultimos_posts(coletar_posts())
        self.assertEqual([p["title"] for p in result], ["Novo", "Antigo"])
        self.assertEqual(result[0]["date"], "2026-06-05")

    def test_yaml_multilinha_e_rascunho(self):
        path = self.post("aula.qmd", "title: 'Título: com dois pontos'\ntags:\n  - cálculo\n  - funções\ndate: 2026-06-05")
        self.assertEqual(extract_post_metadata(path)["tags"], ["cálculo", "funções"])
        self.post("draft.qmd", "title: Rascunho\ntags: [curso]\ndraft: true")
        self.assertEqual(len(coletar_posts()), 1)

    def test_somente_front_matter(self):
        path = self.post("sem-tags.qmd", "title: Sem tags")
        path.write_text(path.read_text() + "\ntags: [não é metadado]", encoding="utf-8")
        self.assertIsNone(extract_post_metadata(path))

    def test_marcadores_invalidos_preservam_indice(self):
        Path("index.qmd").write_text("Sem marcadores", encoding="utf-8")
        with self.assertRaises(ValueError):
            atualizar()
        self.assertEqual(Path("index.qmd").read_text(), "Sem marcadores")

    def test_integridade_detecta_fonte_ausente_e_duplicata(self):
        post = {"href": "posts/ausente.html", "title": "Aula", "tags": ["curso"]}
        erros = verificar_integridade([post, post])
        self.assertTrue(any("Fonte ausente" in e for e in erros))
        self.assertTrue(any("duplicado" in e for e in erros))

if __name__ == "__main__":
    unittest.main()
