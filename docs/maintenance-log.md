# 维护日志

## 2026-11-01 · 初始化

- 采用 Hugo 自有极简模板，不依赖第三方主题。站点名为 HJNotes，部署到 `jihandong/TechNotes` 项目 Pages 路径。
- 文章源文件位于 `articles/<slug>/`；作者本地生成 PDF 并与 TeX 一起提交。
- 每篇使用一份简短 `metadata.toml`；Python 标准库脚本从文章文件自动生成 Hugo 页面，并复制 PDF 到站点资源目录。
- 标签由 Hugo taxonomy 生成。PDF 文章页同时提供内嵌预览、独立打开、下载和 TeX 源码入口。
- GitHub Actions 在推送 `main` 后验证、构建和部署。首次发布需在仓库 Pages 设置中选用 GitHub Actions。
- 提交遵循单一职责。后续维护者应在这里记录影响写作或发布流程的变更。

