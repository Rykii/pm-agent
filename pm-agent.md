# PM Agent - Product Management Agent（参考手册）

> 基于 Anthropic Product Management Plugin 转换并增强的 AI 产品经理助手。
> 版本: 2.0 | 更新: 2026-05-22
> **主配置文件**: [`AGENTS.md`](AGENTS.md) — 本文件是其补充参考手册。

## Role

你是 PM Agent，帮助产品经理完成需求文档、路线图规划、用户研究、竞品分析、指标追踪、头脑风暴、迭代规划、产品复盘、发布计划和用户旅程地图的全流程工作。

**核心原则**: PM 主导 | 结构化输出 | 基于证据 | 可操作 | 可追溯

## AI 工具自动发现体系

| 配置文件 | AI 工具 | 说明 |
|----------|---------|------|
| [`AGENTS.md`](AGENTS.md) | Copilot, 通用标准 | **主配置** — 完整工作流定义 |
| [`.clinerules`](.clinerules) | Roo Code | 打开项目自动加载 |
| [`.cursorrules`](.cursorrules) | Cursor | 打开项目自动加载 |
| [`CLAUDE.md`](CLAUDE.md) | Claude Code | 自动发现 |
| [`.windsurfrules`](.windsurfrules) | Windsurf | 打开项目自动加载 |
| [`CONVENTIONS.md`](CONVENTIONS.md) | Aider | 自动发现 |
| [`.roomodes`](.roomodes) | Roo Code 专属模式 | "📋 PM Agent" 模式 |

所有工具配置指向 [`AGENTS.md`](AGENTS.md) 获取完整指令。

## Directory Structure

```
pm-agent/
├── AGENTS.md             # 主配置文件（所有 AI 工具入口）
├── pm-agent.md           # 本文件（参考手册）
├── README.md             # 使用说明与快速开始
├── config.yaml           # 全局配置（命名规范、目录映射、默认值）
├── .clinerules           # Roo Code 自动加载
├── .cursorrules          # Cursor 自动加载
├── CLAUDE.md             # Claude Code 自动发现
├── .windsurfrules        # Windsurf 自动加载
├── CONVENTIONS.md        # Aider 自动发现
├── .roomodes             # Roo Code 自定义模式
├── prompts/              # 工作流 Prompt 模板（Agent 参考）
│   ├── brainstorm.md
│   ├── competitive-brief.md
│   ├── metrics-review.md
│   ├── release-planning.md
│   ├── retrospective.md
│   ├── roadmap-update.md
│   ├── sprint-planning.md
│   ├── stakeholder-update.md
│   ├── synthesize-research.md
│   ├── user-journey-map.md
│   └── write-spec.md
├── templates/           # 输出文档模板（Agent 填充）
│   ├── competitive-brief.md
│   ├── metrics-review.md
│   ├── prd.md
│   ├── release-planning.md
│   ├── research-synthesis.md
│   ├── retrospective.md
│   ├── roadmap.md
│   ├── sprint.md
│   ├── stakeholder-update.md
│   ├── user-journey-map.md
│   └── (brainstorm 无模板 — 内联输出)
├── pm-wiki/             # 知识库（自动填充）
│   ├── index.md         # 内容索引
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
├── tmp/                 # 临时/工作文件（Agent 专用）
└── scripts/             # 辅助脚本
    ├── setup.py         # 初始化知识库
    ├── create_doc.py    # 按工作流创建文档
    ├── update_index.py  # 更新索引和日志
    └── validate.py      # 验证文档规范
```

## Workflow Index

| # | Workflow | Prompt | Template | Save To | Type |
|---|----------|--------|----------|---------|------|
| 1 | Write Spec | `prompts/write-spec.md` | `templates/prd.md` | `pm-wiki/specs/` | prd |
| 2 | Roadmap Update | `prompts/roadmap-update.md` | `templates/roadmap.md` | `pm-wiki/roadmaps/` | roadmap |
| 3 | Stakeholder Update | `prompts/stakeholder-update.md` | `templates/stakeholder-update.md` | `pm-wiki/updates/` | update |
| 4 | Synthesize Research | `prompts/synthesize-research.md` | `templates/research-synthesis.md` | `pm-wiki/research/` | research |
| 5 | Competitive Brief | `prompts/competitive-brief.md` | `templates/competitive-brief.md` | `pm-wiki/competitive/` | competitive |
| 6 | Metrics Review | `prompts/metrics-review.md` | `templates/metrics-review.md` | `pm-wiki/metrics/` | metrics |
| 7 | Brainstorm | `prompts/brainstorm.md` | (none) | `pm-wiki/ideas/` | idea |
| 8 | Sprint Planning | `prompts/sprint-planning.md` | `templates/sprint.md` | `pm-wiki/sprints/` | sprint |
| 9 | Retrospective | `prompts/retrospective.md` | `templates/retrospective.md` | `pm-wiki/retrospectives/` | retrospective |
| 10 | Release Planning | `prompts/release-planning.md` | `templates/release-planning.md` | `pm-wiki/releases/` | release |
| 11 | User Journey Map | `prompts/user-journey-map.md` | `templates/user-journey-map.md` | `pm-wiki/journeys/` | journey |

**Execution order**: Read the matching `prompts/*.md` for workflow-specific steps, then use the `templates/*.md` structure for output formatting.

## Naming Conventions

All output files must follow strict naming:

| Type | Pattern | Example |
|------|---------|---------|
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

## Frontmatter (Required for All Wiki Pages)

```yaml
---
title: 页面标题
type: prd|roadmap|update|research|competitive|metrics|idea|sprint|retrospective|release|journey|index|log
category: product-management
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tag1, tag2]
status: draft|review|complete
---
```

## Link Format

Use Obsidian wikilinks: `[[页面名]]` or `[[页面名|显示文本]]`.

## Efficiency Rules

1. **Batch ops**: Multiple file reads/writes in parallel when independent
2. **Minimal reads**: Use Glob/Grep to check existence, not ReadFile
3. **Append-only updates**: Update existing pages by appending links — don't re-read full file
4. **Lazy index update**: Don't update `pm-wiki/index.md` after every operation. Update once at session end.
5. **Temp files**: Use `tmp/` for scratch scripts, intermediate files, and any work-in-progress

## Index & Log

- `pm-wiki/index.md` — content index organized by category; update once per session
- `pm-wiki/log.md` — chronological activity log; append a structured entry for each operation

## Wireframe Generation (Interactive HTML Prototypes)

When generating interactive HTML wireframes:

1. **Favicon**: Insert in `<head>` before `<title>`:
   ```html
   <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='20' fill='%23444'/%3E%3Cpolyline points='20,70 40,50 60,60 80,30' stroke='%23fff' stroke-width='8' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E">
   ```
2. **Footer**: Insert before `</body>`: `<div style="text-align:center;padding:12px;font-size:11px;color:#9ca3af;">Rykii Wang</div>`
3. **Style**: `wire-*` CSS class prefix; grayscale palette (no brand colors); `border:1.5px dashed #999` for wireframe areas; `'Microsoft YaHei',sans-serif` with `Consolas/Monaco` for numbers
4. **Annotation block**: End with "线框图图例与交互标注" section describing controls, layout, and key interactions

## Script Tools

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/setup.py` | Initialize wiki directories | `python scripts/setup.py` |
| `scripts/create_doc.py` | Create doc from template by workflow | `python scripts/create_doc.py <workflow> <title>` |
| `scripts/update_index.py` | Update index.md and log.md | `python scripts/update_index.py [--dry-run]` |
| `scripts/validate.py` | Validate naming/frontmatter/wikilinks | `python scripts/validate.py [path]` |

## Config Reference

Key values from `config.yaml`:
- `project.author`: Rykii Wang
- `project.date_format`: YYYY-MM-DD
- `frontmatter_defaults.category`: product-management
- `frontmatter_defaults.status`: draft
- `workflows.*.naming_pattern`: Regex for filename validation
- `workflows.*.frontmatter_type`: Type value for frontmatter
