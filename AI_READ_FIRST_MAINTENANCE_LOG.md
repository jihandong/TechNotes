# AI 必读：HJNotes 维护规则与变更日志

本文件是 AI 的维护约定与变更日志。不同会话接手前先阅读本文件。`README.md` 留给作者将来编写，目前不创建。

## 项目目标

- 作者专注写 `articles/<slug>/main.tex`，在本地生成并提交 `main.pdf`。
- 站点页面、标签索引、部署均由程序完成；`metadata.toml` 仅在需要覆盖自动提取结果时使用。
- 保持简洁、快速、可阅读的静态站点，不增加不必要的服务、主题依赖或 JavaScript。

## 不变量

- `articles/<slug>/` 是文章的唯一来源；每篇必须有 `main.tex`、`main.pdf`，`metadata.toml` 可选。
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
5. 影响流程或架构的改动，更新本文件下方的维护日志。不要代作者撰写 README，除非作者另行要求。

## 日常维护分工

- 作者：写作、在本地生成 PDF、确认文章内容。
- AI：根据文章整理标题、标签与简介；维护模板、构建脚本、部署流程；排查构建失败；更新文档和维护日志。
- GitHub Actions：验证文章结构、生成静态网页、部署 Pages。

## 投稿格式

复制 `articles/_template/` 为 `articles/<slug>/`。文件夹名使用小写英文、数字和连字符。提交 `main.tex` 和本地渲染的 `main.pdf`。脚本从 `\title{...}` 提取标题，从 `% HJNotes-Tags: GPU, Memory` 提取标签，从 `% HJNotes-Summary: ...` 提取简介；没有标签注释时归入 `AI Infra`。发布日期取 TeX 文件首次提交日期。复杂标题或需要精确日期时，可以增加 `metadata.toml` 覆盖自动结果。推送 `main` 后网站自动更新。构建脚本 `scripts/build_content.py` 不会编译 TeX。

## 维护日志

### 2026-11-01 · 初始化

- 采用 Hugo 自有极简模板，站点名 HJNotes，部署到 `jihandong/TechNotes` 项目 Pages 路径。
- 文章源文件位于 `articles/<slug>/`；作者本地生成 PDF 并与 TeX 一起提交。
- Python 标准库脚本从 `metadata.toml` 生成 Hugo 页面，将 PDF 复制到站点资源目录。标签由 Hugo taxonomy 生成。
- GitHub Actions 在推送 `main` 后验证、构建和部署。首次发布需在仓库 Pages 设置中选择 GitHub Actions。
- 作者指定每个 commit 只做一件事，并要求 README 留待以后自己规划；AI 维护信息统一记录在本文件。
- 为方便 AI 识别，维护文档使用醒目的英文文件名 `AI_READ_FIRST_MAINTENANCE_LOG.md`，不设置额外入口文件。

### 2026-11-01 · 修正 PDF 路径

- Hugo 的 `relURL` 需要无前导斜杠的资源路径，才能保留项目站点的 `/TechNotes/` 前缀。文章生成脚本输出 `pdfs/<slug>.pdf`。

### 2026-11-01 · 简化投稿

- 每篇现在只需提交 `main.tex` 与 `main.pdf`。标题和可选标签、简介从 TeX 中提取；发布日期取首次提交日期。`metadata.toml` 改为可选覆盖文件。

