#!/usr/bin/env python3
"""
PM Agent - 启动器

用法:
    python setup.py [command]

Commands:
    setup       初始化知识库（创建所有 wiki 目录）
    help        显示帮助

示例:
    python setup.py setup
"""

import sys
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    print("警告: 未安装 PyYAML，将使用默认目录列表")
    yaml = None


def print_banner():
    print("=" * 60)
    print("  PM Agent v2.0")
    print("  AI 产品经理助手")
    print("=" * 60)
    print()


def print_help():
    print(__doc__)
    print()
    print("使用方式:")
    print("  将 pm-agent.md 配置到 KimiCode Agent 后，直接对话即可")
    print()
    print("常用指令:")
    print("  - 帮我写 [功能] 的 PRD")
    print("  - 更新产品路线图")
    print("  - 整理这些访谈笔记")
    print("  - 分析 [竞品名]")
    print("  - 审查本月产品指标")
    print("  - 一起头脑风暴 [主题]")
    print("  - 规划下两周迭代")
    print("  - 生成 Sprint-XX 迭代计划")
    print("  - 做 Q2 产品复盘")
    print("  - 制定 vX.X 发布计划")
    print("  - 绘制新用户旅程地图")
    print()
    print("脚本工具:")
    print("  - python scripts/create_doc.py <workflow> <title>")
    print("  - python scripts/update_index.py")
    print("  - python scripts/validate.py")


def load_config():
    config_path = Path("config.yaml")
    if yaml and config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


def setup():
    print("正在初始化 PM Agent 知识库...")
    print()

    config = load_config()
    root = Path.cwd()
    wiki = root / "pm-wiki"

    # 从 config.yaml 读取目录列表，或使用默认值
    dirs = config.get("wiki_dirs", [
        "pm-wiki/specs",
        "pm-wiki/roadmaps",
        "pm-wiki/research",
        "pm-wiki/competitive",
        "pm-wiki/metrics",
        "pm-wiki/updates",
        "pm-wiki/ideas",
        "pm-wiki/sprints",
        "pm-wiki/retrospectives",
        "pm-wiki/releases",
        "pm-wiki/journeys",
    ])

    created = []
    for d in dirs:
        dir_path = root / d
        dir_path.mkdir(parents=True, exist_ok=True)
        rel = dir_path.relative_to(root)
        created.append(f"  OK  {rel}")

    for line in created:
        print(line)

    # 创建 tmp 目录
    tmp_dir = root / "tmp"
    tmp_dir.mkdir(exist_ok=True)
    print(f"  OK  tmp/")

    # 初始化 index.md（如果不存在）
    index_file = wiki / "index.md"
    if not index_file.exists():
        date_str = datetime.now().strftime("%Y-%m-%d")
        index_content = f"""---
title: PM Wiki 索引
type: index
category: product-management
updated: {date_str}
tags: [index]
status: complete
---

# PM Wiki 索引

*最后更新: {date_str}*

> 使用 `python scripts/update_index.py` 更新索引
"""
        index_file.write_text(index_content, encoding="utf-8")
        print(f"  OK  pm-wiki/index.md (初始化)")

    # 初始化 log.md（如果不存在）
    log_file = wiki / "log.md"
    if not log_file.exists():
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        log_content = f"""---
title: 操作日志
type: log
category: product-management
created: {date_str.split()[0]}
updated: {date_str.split()[0]}
tags: [log]
status: complete
---

# 操作日志

## {date_str}

- **操作**: 初始化知识库
- **说明**: PM Agent v2.0 初始化完成
"""
        log_file.write_text(log_content, encoding="utf-8")
        print(f"  OK  pm-wiki/log.md (初始化)")

    print()
    print("初始化完成!")
    print()
    print("下一步:")
    print("  1. 将 pm-agent.md 配置到 KimiCode Agent")
    print("  2. 开始对话：'帮我写 PRD'")
    print("  3. 使用脚本: python scripts/create_doc.py spec '功能名'")


def main():
    print_banner()

    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    command = sys.argv[1]

    if command == "setup":
        setup()
    elif command in ["help", "-h", "--help"]:
        print_help()
    else:
        print(f"未知命令: {command}")
        print()
        print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
