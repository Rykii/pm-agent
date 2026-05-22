# PM Agent

> AI 产品经理助手 — 帮助 PM 完成需求文档、路线图规划、用户研究、竞品分析、指标追踪、头脑风暴、迭代规划、产品复盘、发布计划和用户旅程地图。

## 快速开始

### 1. 初始化知识库

```bash
python scripts/setup.py
```

### 2. 配置 Agent

**零配置，打开项目即用。**

本项目使用 [`AGENTS.md`](AGENTS.md) 作为唯一主配置文件，所有主流 AI 工具已经覆盖：

| AI 工具 | 自动加载文件 | 说明 |
|---------|-------------|------|
| **Roo Code** | `.clinerules` + `.roomodes` | 打开项目自动加载 + "📋 PM Agent" 专属模式 |
| **Cursor** | `.cursorrules` | 打开项目自动加载 |
| **Claude Code** | `CLAUDE.md` | 自动发现 |
| **GitHub Copilot** | `AGENTS.md` | 原生支持 |
| **Windsurf** | `.windsurfrules` | 打开项目自动加载 |
| **Aider** | `CONVENTIONS.md` | 自动发现 |

所有工具配置文件内容指向 [`AGENTS.md`](AGENTS.md) 获取完整指令。也有独立参考手册 [`pm-agent.md`](pm-agent.md)。

### 3. 开始使用

直接对话即可：

- "帮我写碳金融交易管理的 PRD"
- "更新产品路线图"
- "整理这些访谈笔记"
- "分析竞品 X"
- "审查本月产品指标"
- "一起头脑风暴用户留存"
- "规划下两周迭代"
- "生成 Sprint-12 的迭代计划"
- "做 Q2 产品复盘"
- "制定 v2.3 发布计划"
- "绘制新用户旅程地图"

## 工作流索引

| # | 工作流 | 说明 | Prompt | Template |
|---|--------|------|--------|----------|
| 1 | **Write Spec** | 撰写 PRD | `prompts/write-spec.md` | `templates/prd.md` |
| 2 | **Roadmap Update** | 更新路线图 | `prompts/roadmap-update.md` | `templates/roadmap.md` |
| 3 | **Stakeholder Update** | 利益相关者更新 | `prompts/stakeholder-update.md` | `templates/stakeholder-update.md` |
| 4 | **Synthesize Research** | 研究综合 | `prompts/synthesize-research.md` | `templates/research-synthesis.md` |
| 5 | **Competitive Brief** | 竞品分析 | `prompts/competitive-brief.md` | `templates/competitive-brief.md` |
| 6 | **Metrics Review** | 指标审查 | `prompts/metrics-review.md` | `templates/metrics-review.md` |
| 7 | **Brainstorm** | 头脑风暴 | `prompts/brainstorm.md` | (内联输出) |
| 8 | **Sprint Planning** | 迭代规划 | `prompts/sprint-planning.md` | `templates/sprint.md` |
| 9 | **Retrospective** | 产品复盘 | `prompts/retrospective.md` | `templates/retrospective.md` |
| 10 | **Release Planning** | 发布计划 | `prompts/release-planning.md` | `templates/release-planning.md` |
| 11 | **User Journey Map** | 用户旅程 | `prompts/user-journey-map.md` | `templates/user-journey-map.md` |

## 脚本工具

### create_doc.py — 按工作流创建文档

```bash
# 创建 PRD
python scripts/create_doc.py spec "碳金融交易管理PRD-v1.0"

# 创建迭代计划
python scripts/create_doc.py sprint "Sprint-12"

# 创建复盘
python scripts/create_doc.py retrospective "2026-Q2-复盘"

# 创建发布计划
python scripts/create_doc.py release "v2.3-发布"

# 创建用户旅程
python scripts/create_doc.py journey "新用户旅程地图"
```

### update_index.py — 更新索引和日志

```bash
# 更新 pm-wiki/index.md 和 pm-wiki/log.md
python scripts/update_index.py

# 预览更新内容（不写入）
python scripts/update_index.py --dry-run
```

### validate.py — 验证文档规范

```bash
# 验证全部文档
python scripts/validate.py

# 验证单个文件
python scripts/validate.py pm-wiki/specs/2026-05-07-xxx.md
```

## 命名规范速查

| 类型 | 命名模式 | 示例 |
|------|----------|------|
| PRD | `YYYY-MM-DD-功能名.md` | `2026-05-07-交易工作台PRD-v1.0.md` |
| Roadmap | `roadmap-YYYY-MM.md` | `roadmap-2026-05.md` |
| Updates | `YYYY-MM-DD-更新类型.md` | `2026-05-14-weekly-update.md` |
| Research | `YYYY-MM-DD-研究主题.md` | `2026-04-29-summit培训材料分析.md` |
| Competitive | `YYYY-MM-DD-竞品名.md` | `2026-05-14-competitor-x.md` |
| Metrics | `YYYY-MM-DD-指标审查.md` | `2026-05-14-metrics-review.md` |
| Ideas | `YYYY-MM-DD-主题.md` | `2026-05-14-improve-retention.md` |
| Sprint | `YYYY-MM-DD-迭代名.md` | `2026-05-14-sprint-12.md` |
| Retrospective | `YYYY-MM-DD-复盘主题.md` | `2026-05-14-sprint12-retrospective.md` |
| Release | `YYYY-MM-DD-版本发布.md` | `2026-05-14-v2.3-release.md` |
| Journey | `YYYY-MM-DD-旅程主题.md` | `2026-05-14-new-user-journey.md` |

## Frontmatter 规范

所有 Wiki 页面必须包含：

```yaml
---
title: 页面标题
type: prd|roadmap|update|research|competitive|metrics|idea|sprint|retrospective|release|journey
category: product-management
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tag1, tag2]
status: draft|review|complete
---
```

## 目录结构

```
pm-agent/
├── pm-agent.md          # Agent 系统指令
├── README.md            # 本文件
├── config.yaml          # 全局配置
├── prompts/             # 11 个工作流 Prompt
├── templates/           # 10 个输出模板（Brainstorm 无模板）
├── pm-wiki/             # 知识库（11 个子目录）
│   ├── index.md         # 自动生成的索引
│   ├── log.md           # 操作日志
│   ├── specs/           # PRD 文档
│   ├── roadmaps/        # 路线图
│   ├── research/        # 研究综合
│   ├── competitive/     # 竞品分析
│   ├── metrics/         # 指标报告
│   ├── updates/         # 利益相关者更新
│   ├── ideas/           # 头脑风暴
│   ├── sprints/         # 迭代规划
│   ├── retrospectives/  # 产品复盘
│   ├── releases/        # 发布计划
│   └── journeys/        # 用户旅程地图
├── pm-raw/              # 原始资料（用户提供）
├── tmp/                 # 临时文件
└── scripts/             # 辅助脚本
```

## 配置

全局配置在 `config.yaml` 中，包含：
- 项目信息（名称、作者、时区、日期格式）
- Frontmatter 默认值
- 11 个工作流的配置（prompt 路径、模板路径、保存目录、命名正则、frontmatter 类型）
- Wiki 目录列表
- 效率规则

## 效率规则

1. **Batch ops**: 独立文件的读写并行执行
2. **Minimal reads**: 用 Glob/Grep 检查存在性，而非 ReadFile
3. **Append-only updates**: 更新现有页面时追加链接，不重新读取完整文件
4. **Lazy index update**: 每次会话结束时更新一次 `pm-wiki/index.md`
5. **Temp files**: 使用 `tmp/` 存放临时脚本和工作文件

## 依赖

脚本工具需要 Python 3.8+ 和 PyYAML：

```bash
pip install pyyaml
```

## 常见问题

**Q: Brainstorm 为什么没有模板？**
A: 头脑风暴的输出是动态的、对话式的，不适合固定模板。输出保存为 Markdown 到 `pm-wiki/ideas/`。

**Q: 如何添加新的工作流？**
A: 1) 在 `config.yaml` 的 `workflows` 中添加配置；2) 创建 `prompts/<name>.md`；3) 创建 `templates/<name>.md`（可选）；4) 更新 `pm-agent.md` 的 Workflow Index。

**Q: 文件名不符合规范怎么办？**
A: 运行 `python scripts/validate.py` 检查具体问题。命名规范定义在 `config.yaml` 的 `workflows.*.naming_pattern` 中。
