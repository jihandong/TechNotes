# HJNotes 维护约定

本文件供不同 AI 会话及维护者快速接手。先读 `README.md` 和 `docs/maintenance-log.md`，再处理任务。

## 项目目标

- 作者专注写 `articles/<slug>/main.tex`，在本地生成并提交 `main.pdf`。
- 作者或协作 AI 填写同目录的 `metadata.toml`；站点页面、标签索引、部署均由程序完成。
- 保持简洁、快速、可阅读的静态站点，不增加不必要的服务、主题依赖或 JavaScript。

## 不变量

- `articles/<slug>/` 是文章的唯一来源；每篇必须有 `main.tex`、`main.pdf`、`metadata.toml`。
- `content/notes/`、`static/pdfs/`、`public/` 是生成目录，不要手动维护，也不要提交。
- 不在 CI 编译 TeX。PDF 由作者的 VS Code 工作流生成；构建脚本只检查 PDF 文件头并复制文件。
- URL 以项目站点路径 `/TechNotes/` 为基准。所有站内资源和导航应使用 Hugo 的 `relURL` 或 `.RelPermalink`。
- PDF 页面必须保留独立的打开或下载链接，以便内嵌预览失败时仍可访问。
- 不要忽略 `*.pdf`；只忽略 LaTeX 临时产物。

## 修改与验证

1. 每个 commit 只做一件事。站点样式、文章流水线、文档、修复分别提交。
2. 改动文章生成脚本后，运行 `python scripts/build_content.py`，并用含 PDF 的样例检查生成页面和资源。
3. 改动 Hugo 模板或配置后，运行 `hugo --minify`；如本地没有 Hugo，以 GitHub Actions 构建结果为准。
4. 发布前检查站点首页、文章页、标签页，以及 `/TechNotes/` 路径下的 PDF 链接。
5. 影响流程或架构的改动，更新 `README.md` 和 `docs/maintenance-log.md`。

## 日常维护分工

- 作者：写作、在本地生成 PDF、确认文章内容。
- AI：根据文章整理标题、标签与简介；维护模板、构建脚本、部署流程；排查构建失败；更新文档和维护日志。
- GitHub Actions：验证文章结构、生成静态网页、部署 Pages。

