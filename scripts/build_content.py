"""Turn committed TeX/PDF article pairs into Hugo pages. No TeX build is performed."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tomllib
from datetime import date, datetime
from pathlib import Path


SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
SOURCE_BASE = "https://github.com/jihandong/TechNotes/blob/main/articles"


def quoted(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def metadata(path: Path) -> dict:
    with path.open("rb") as handle:
        item = tomllib.load(handle)
    title = item.get("title")
    published = item.get("date")
    tags = item.get("tags")
    summary = item.get("summary", "")
    if not isinstance(title, str) or not title.strip():
        raise ValueError("title 必须是非空字符串")
    if not isinstance(published, date) or isinstance(published, datetime):
        raise ValueError("date 必须是 YYYY-MM-DD 格式的 TOML 日期")
    if not isinstance(tags, list) or not tags or any(not isinstance(tag, str) or not tag.strip() for tag in tags):
        raise ValueError("tags 必须是非空字符串数组")
    if len({tag.strip().casefold() for tag in tags}) != len(tags):
        raise ValueError("tags 不能重复")
    if not isinstance(summary, str):
        raise ValueError("summary 必须是字符串")
    return {"title": title.strip(), "date": published.isoformat(), "tags": [tag.strip() for tag in tags], "summary": summary.strip()}


def build(root: Path) -> int:
    articles = root / "articles"
    notes = root / "content" / "notes"
    pdfs = root / "static" / "pdfs"
    notes.mkdir(parents=True, exist_ok=True)
    pdfs.mkdir(parents=True, exist_ok=True)
    for old in notes.glob("*.md"):
        old.unlink()
    for old in pdfs.glob("*.pdf"):
        old.unlink()
    (notes / "_index.md").write_text("+++\ntitle = '全部文章'\n+++\n", encoding="utf-8")

    count = 0
    for folder in sorted(articles.iterdir()):
        if not folder.is_dir() or folder.name.startswith("_"):
            continue
        slug = folder.name
        if not SLUG.fullmatch(slug):
            raise ValueError(f"{slug}: 文件夹名须使用小写英文、数字和连字符")
        tex = folder / "main.tex"
        pdf = folder / "main.pdf"
        meta = folder / "metadata.toml"
        for required in (tex, pdf, meta):
            if not required.is_file():
                raise ValueError(f"{slug}: 缺少 {required.name}")
        with pdf.open("rb") as handle:
            header = handle.read(5)
        if header != b"%PDF-":
            raise ValueError(f"{slug}: main.pdf 不是有效的 PDF 文件头")
        try:
            item = metadata(meta)
        except (ValueError, tomllib.TOMLDecodeError) as error:
            raise ValueError(f"{slug}: metadata.toml: {error}") from error
        tag_list = ", ".join(quoted(tag) for tag in item["tags"])
        page = (
            "+++\n"
            f"title = {quoted(item['title'])}\n"
            f"date = {item['date']}\n"
            f"description = {quoted(item['summary'])}\n"
            f"tags = [{tag_list}]\n"
            f"slug = {quoted(slug)}\n"
            f"pdf = {quoted('pdfs/' + slug + '.pdf')}\n"
            f"source = {quoted(SOURCE_BASE + '/' + slug + '/main.tex')}\n"
            "+++\n"
        )
        (notes / f"{slug}.md").write_text(page, encoding="utf-8")
        shutil.copyfile(pdf, pdfs / f"{slug}.pdf")
        count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        count = build(args.root.resolve())
    except (OSError, ValueError) as error:
        print(f"文章检查失败：{error}", file=sys.stderr)
        return 1
    print(f"已生成 {count} 篇文章的页面和 PDF 资源")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

