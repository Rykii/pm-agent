#!/usr/bin/env python3
"""
PM Agent - 启动器

用法:
    python start.py [command]

Commands:
    setup       初始化知识库
    help        显示帮助

Examples:
    python start.py setup
"""

import sys
from pathlib import Path
from datetime import datetime

def print_banner():
    print("=" * 60)
    print("  PM Agent")
    print("  AI 产品经理助手")
    print("=" * 60)
    print()

def print_help():
    print(__doc__)
    print()
    print("使用方式:")
    print("  将 agents.md 配置到 KimiCode Agent 后，直接对话即可")
    print()
    print("常用指令:")
    print("  - 帮我写 [功能] 的 PRD")
    print("  - 更新产品路线图")
    print("  - 整理这些访谈笔记")
    print("  - 分析 [竞品名]")
    print("  - 审查本月产品指标")
    print("  - 一起头脑风暴 [主题]")
    print("  - 规划下两周迭代")

def setup():
    print("正在初始化 PM Agent 知识库...")
    
    root = Path.cwd()
    wiki = root / "wiki"
    
    dirs = [
        wiki / "specs",
        wiki / "roadmaps",
        wiki / "research",
        wiki / "competitive",
        wiki / "metrics",
        wiki / "updates",
        wiki / "ideas",
        wiki / "sprints",
    ]
    
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"  OK {d.relative_to(root)}")
    
    # 更新 index.md 中的日期占位符
    index_file = wiki / "index.md"
    if index_file.exists():
        content = index_file.read_text(encoding="utf-8")
        content = content.replace("{{date}}", datetime.now().strftime("%Y-%m-%d"))
        index_file.write_text(content, encoding="utf-8")
    
    log_file = wiki / "log.md"
    if log_file.exists():
        content = log_file.read_text(encoding="utf-8")
        content = content.replace("{{date}}", datetime.now().strftime("%Y-%m-%d %H:%M"))
        log_file.write_text(content, encoding="utf-8")
    
    print("\n初始化完成!")
    print("\n下一步:")
    print("  1. 将 agents.md 配置到 KimiCode Agent")
    print("  2. 开始对话：'帮我写 PRD'")

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
