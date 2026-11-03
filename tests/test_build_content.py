from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.build_content import build

TEST_TMP = Path(__file__).resolve().parents[1] / ".test-tmp"
TEST_TMP.mkdir(exist_ok=True)


class BuildContentTest(unittest.TestCase):
    def test_tex_and_pdf_alone_publish_with_tags(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TMP) as temporary:
            root = Path(temporary)
            article = root / "articles" / "gpu-memory"
            article.mkdir(parents=True)
            (article / "main.tex").write_text(
                "% HJNotes-Tags: GPU, Memory\n"
                "% HJNotes-Summary: 显存分配笔记\n"
                "\\title{GPU 内存管理}\n",
                encoding="utf-8",
            )
            (article / "main.pdf").write_bytes(b"%PDF-1.7\nexample")

            self.assertEqual(build(root), 1)
            page = (root / "content" / "notes" / "gpu-memory.md").read_text(encoding="utf-8")
            self.assertIn('title = "GPU 内存管理"', page)
            self.assertIn('tags = ["GPU", "Memory"]', page)
            self.assertIn('description = "显存分配笔记"', page)

    def test_article_generates_page_and_pdf(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TMP) as temporary:
            root = Path(temporary)
            article = root / "articles" / "gpu-memory"
            article.mkdir(parents=True)
            (article / "main.tex").write_text("\\title{GPU 内存管理}\n", encoding="utf-8")
            (article / "main.pdf").write_bytes(b"%PDF-1.7\nexample")
            (article / "metadata.toml").write_text(
                'title = "GPU 内存管理"\n'
                "date = 2026-11-01\n"
                'tags = ["GPU", "Memory"]\n'
                'summary = "显存分配笔记"\n',
                encoding="utf-8",
            )

            self.assertEqual(build(root), 1)
            page = (root / "content" / "notes" / "gpu-memory.md").read_text(encoding="utf-8")
            self.assertIn('title = "GPU 内存管理"', page)
            self.assertIn('tags = ["GPU", "Memory"]', page)
            self.assertIn('pdf = "pdfs/gpu-memory.pdf"', page)
            self.assertIn("articles/gpu-memory/main.tex", page)
            self.assertEqual((root / "static" / "pdfs" / "gpu-memory.pdf").read_bytes(), b"%PDF-1.7\nexample")

    def test_missing_pdf_fails(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TMP) as temporary:
            root = Path(temporary)
            article = root / "articles" / "gpu-memory"
            article.mkdir(parents=True)
            (article / "main.tex").write_text("\\title{GPU}\n", encoding="utf-8")
            (article / "metadata.toml").write_text(
                'title = "GPU"\ndate = 2026-11-01\ntags = ["GPU"]\n', encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "main.pdf"):
                build(root)

    def test_empty_summary_does_not_consume_title(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TMP) as temporary:
            root = Path(temporary)
            article = root / "articles" / "collective-communication"
            article.mkdir(parents=True)
            (article / "main.tex").write_text(
                "% HJNotes-Tags: AI Infra, MPI\n"
                "% HJNotes-Summary:\n"
                "\\title{Collective Communication}\n",
                encoding="utf-8",
            )
            (article / "main.pdf").write_bytes(b"%PDF-1.7\nexample")

            self.assertEqual(build(root), 1)
            page = (root / "content" / "notes" / "collective-communication.md").read_text(encoding="utf-8")
            self.assertIn('title = "Collective Communication"', page)
            self.assertIn('description = ""', page)


if __name__ == "__main__":
    unittest.main()

