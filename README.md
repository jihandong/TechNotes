# HJNotes

以 LaTeX 写作、PDF 阅读的 AI Infra 技术笔记。网站使用 Hugo 构建，由 GitHub Pages 发布。

## 发布一篇文章

1. 复制 `articles/_template/`，把新文件夹命名为英文小写、数字和连字符组成的短名，例如 `gpu-memory`。
2. 在新文件夹中编写 `main.tex`，用你自己的 VS Code 工作流渲染出 `main.pdf`。
3. 修改 `metadata.toml` 的标题、发布日期、标签和一句话简介。日期使用 `YYYY-MM-DD`，标签至少一个。
4. 提交这三个文件并推送到 `main`。GitHub Actions 会检查文章、生成网站页面和标签索引，然后发布。

例如：

```text
articles/
  gpu-memory/
    main.tex
    main.pdf
    metadata.toml
```

```toml
title = "GPU 内存管理笔记"
date = 2026-11-01
tags = ["GPU", "Memory"]
summary = "记录显存分配、复用和排查方法。"
```

PDF 和 TeX 源文件都保留在仓库中。页面中的 PDF 预览、下载、标签及 TeX 源码链接由构建流程生成，无需手工编辑网页文件。LaTeX 的 `.aux`、`.log`、`.synctex.gz` 等临时文件已被忽略，`main.pdf` 不会被忽略。

## 本地预览

安装 Python 3.11+ 和 Hugo 0.169.0 后，在仓库根目录运行：

```sh
python scripts/build_content.py
hugo server
```

构建产物位于 `content/notes/`、`static/pdfs/` 和 `public/`，这些目录由程序生成且已加入 `.gitignore`。

## 首次启用 GitHub Pages

在仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。首次成功发布后，站点地址为 <https://jihandong.github.io/TechNotes/>。后续推送到 `main` 会自动重新发布。

## 维护

AI 接手维护前，请先阅读 [AGENTS.md](AGENTS.md) 和 [维护日志](docs/maintenance-log.md)。网站仅依赖 Hugo、Python 标准库与 GitHub Actions；PDF 编译由作者本地完成。

