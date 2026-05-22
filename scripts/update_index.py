#!/usr/bin/env python3
"""
PM Agent - 索引更新工具

用法:
    python update_index.py

功能:
    1. 扫描 pm-wiki/ 下所有文档
    2. 按类别分组
    3. 生成/更新 pm-wiki/index.md
    4. 记录更新日志到 pm-wiki/log.md

可选参数:
    --dry-run    预览更新内容，不写入文件
"""

import sys
import re
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    print("错误: 需要 PyYAML 包。请运行: pip install pyyaml")
    sys.exit(1)


def load_config():
    config_path = Path("config.yaml")
    if not config_path.exists():
        return {}
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def parse_frontmatter(content):
    """解析 Markdown 文件的 frontmatter"""
    if not content.startswith("---"):
        return {}

    try:
        end = content.index("---", 3)
        fm_text = content[3:end].strip()
        return yaml.safe_load(fm_text) or {}
    except (ValueError, yaml.YAMLError):
        return {}


def scan_wiki():
    """扫描 pm-wiki 目录，收集所有文档信息"""
    wiki_dir = Path("pm-wiki")
    if not wiki_dir.exists():
        print("错误: pm-wiki 目录不存在")
        sys.exit(1)

    docs = {}
    for md_file in wiki_dir.rglob("*.md"):
        # 跳过 index.md 和 log.md
        if md_file.name in ("index.md", "log.md"):
            continue

        content = md_file.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(content)

        doc_type = frontmatter.get("type", "other")
        title = frontmatter.get("title", md_file.stem)
        status = frontmatter.get("status", "unknown")
        created = frontmatter.get("created", "")
        tags = frontmatter.get("tags", [])

        rel_path = md_file.relative_to(wiki_dir)
        wiki_link = f"[[{title}]]"

        if doc_type not in docs:
            docs[doc_type] = []

        docs[doc_type].append({
            "title": title,
            "path": str(rel_path),
            "status": status,
            "created": created,
            "tags": tags,
            "wiki_link": wiki_link,
        })

    # 每个类别内按创建日期排序
    for doc_type in docs:
        docs[doc_type].sort(key=lambda x: x.get("created", ""), reverse=True)

    return docs


def generate_index(docs, config):
    """生成索引 Markdown 内容"""
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        "---",
        "title: PM Wiki 索引",
        "type: index",
        "category: product-management",
        f"updated: {date_str.split()[0]}",
        "tags: [index]",
        "status: complete",
        "---",
        "",
        "# PM Wiki 索引",
        "",
        f"*最后更新: {date_str}*",
        "",
        "## 目录",
        "",
    ]

    # 类型名称映射
    type_names = {
        "prd": "📋 PRD 文档",
        "roadmap": "🗺️ 路线图",
        "update": "📢 利益相关者更新",
        "research": "🔬 研究综合",
        "competitive": "⚔️ 竞品分析",
        "metrics": "📊 指标报告",
        "idea": "💡 头脑风暴",
        "sprint": "🏃 迭代规划",
        "retrospective": "🔍 复盘",
        "release": "🚀 发布计划",
        "journey": "🛤️ 用户旅程",
    }

    # 生成目录
    for doc_type in sorted(docs.keys()):
        display_name = type_names.get(doc_type, f"📄 {doc_type}")
        count = len(docs[doc_type])
        lines.append(f"- [{display_name} ({count})](#{doc_type})")

    lines.append("")

    # 生成各分类内容
    for doc_type in sorted(docs.keys()):
        display_name = type_names.get(doc_type, f"📄 {doc_type}")
        lines.append(f"## {display_name}")
        lines.append("")

        for doc in docs[doc_type]:
            status_emoji = {
                "draft": "📝",
                "review": "👀",
                "complete": "✅",
            }.get(doc["status"], "❓")

            lines.append(f"- {status_emoji} {doc['wiki_link']} — *{doc['created']}*")

        lines.append("")

    # 添加统计
    total = sum(len(items) for items in docs.values())
    lines.append("---")
    lines.append("")
    lines.append(f"**总计文档数**: {total}")
    lines.append("")

    return "\n".join(lines)


def update_log(docs):
    """追加更新记录到 log.md"""
    log_path = Path("pm-wiki/log.md")
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    total = sum(len(items) for items in docs.values())
    type_counts = {t: len(items) for t, items in docs.items()}

    log_entry = [
        f"\n## {date_str}",
        "",
        f"- **操作**: 更新索引",
        f"- **总计文档**: {total}",
    ]

    for doc_type, count in sorted(type_counts.items()):
        log_entry.append(f"- **{doc_type}**: {count} 篇")

    log_entry.append("")

    if log_path.exists():
        content = log_path.read_text(encoding="utf-8")
        content += "\n".join(log_entry)
    else:
        content = "---\ntitle: 操作日志\ntype: log\ncategory: product-management\ncreated: "
        content += date_str.split()[0]
        content += "\nupdated: " + date_str.split()[0]
        content += "\ntags: [log]\nstatus: complete\n---\n\n# 操作日志\n"
        content += "\n".join(log_entry)

    return content


def main():
    dry_run = "--dry-run" in sys.argv

    config = load_config()
    docs = scan_wiki()

    if not docs:
        print("未在 pm-wiki/ 下找到任何文档")
        sys.exit(0)

    # 生成索引
    index_content = generate_index(docs, config)
    index_path = Path("pm-wiki/index.md")

    if dry_run:
        print("=== 索引预览 ===")
        print(index_content[:2000])
        print("\n... (预览截断)")
    else:
        index_path.write_text(index_content, encoding="utf-8")
        print(f"✅ 已更新: {index_path}")

    # 更新日志
    log_content = update_log(docs)
    log_path = Path("pm-wiki/log.md")

    if dry_run:
        print("\n=== 日志预览 ===")
        print(log_content[:1000])
    else:
        log_path.write_text(log_content, encoding="utf-8")
        print(f"✅ 已更新: {log_path}")

    # 统计输出
    print("\n📊 文档统计:")
    for doc_type, items in sorted(docs.items()):
        print(f"  {doc_type}: {len(items)} 篇")
    print(f"  总计: {sum(len(items) for items in docs.values())} 篇")


if __name__ == "__main__":
    main()
