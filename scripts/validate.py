#!/usr/bin/env python3
"""
PM Agent - 文档验证工具

用法:
    python validate.py [path]

参数:
    path    要验证的文件或目录（默认: pm-wiki/）

功能:
    1. 检查文件名是否符合命名规范
    2. 检查 frontmatter 是否完整
    3. 检查 wikilinks 是否指向存在的文件
    4. 输出验证报告

退出码:
    0 - 无问题
    1 - 发现问题
"""

import sys
import re
from pathlib import Path

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
        return None, "缺少 frontmatter"

    try:
        end = content.index("---", 3)
        fm_text = content[3:end].strip()
        return yaml.safe_load(fm_text) or {}, None
    except ValueError:
        return None, "frontmatter 格式错误（未找到结束标记）"
    except yaml.YAMLError as e:
        return None, f"frontmatter YAML 解析错误: {e}"


def validate_filename(filename, config):
    """验证文件名是否符合命名规范"""
    # 排除特殊文件
    if filename in ("index.md", "log.md", "README.md"):
        return []

    errors = []
    workflows = config.get("workflows", {})

    matched = False
    for key, wf in workflows.items():
        pattern = wf.get("naming_pattern", "")
        if pattern and re.match(pattern, filename):
            matched = True
            break

    if not matched:
        errors.append(f"文件名不符合任何命名规范: {filename}")

    return errors


def validate_frontmatter(frontmatter, filepath):
    """验证 frontmatter 字段是否完整"""
    errors = []
    required_fields = ["title", "type", "category", "created", "updated", "tags", "status"]

    for field in required_fields:
        if field not in frontmatter:
            errors.append(f"缺少 frontmatter 字段: {field}")

    if "type" in frontmatter:
        valid_types = [
            "prd", "roadmap", "update", "research", "competitive",
            "metrics", "idea", "sprint", "retrospective", "release",
            "journey", "index", "log"
        ]
        if frontmatter["type"] not in valid_types:
            errors.append(f"无效的 type: {frontmatter['type']}")

    if "status" in frontmatter:
        valid_statuses = ["draft", "review", "complete"]
        if frontmatter["status"] not in valid_statuses:
            errors.append(f"无效的 status: {frontmatter['status']}")

    if "created" in frontmatter:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(frontmatter["created"])):
            errors.append(f"created 格式错误: {frontmatter['created']} (应为 YYYY-MM-DD)")

    if "updated" in frontmatter:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(frontmatter["updated"])):
            errors.append(f"updated 格式错误: {frontmatter['updated']} (应为 YYYY-MM-DD)")

    return errors


def extract_wikilinks(content):
    """提取内容中的 wikilinks"""
    # 匹配 [[页面名]] 和 [[页面名|显示文本]]
    pattern = r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]'
    return re.findall(pattern, content)


def validate_wikilinks(content, wiki_dir, current_file):
    """验证 wikilinks 是否指向存在的文件"""
    errors = []
    links = extract_wikilinks(content)

    # 收集所有文档标题
    existing_titles = set()
    for md_file in wiki_dir.rglob("*.md"):
        if md_file.name in ("index.md", "log.md"):
            continue
        fm_content = md_file.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(fm_content)
        if fm and "title" in fm:
            existing_titles.add(fm["title"])

    for link in links:
        if link not in existing_titles:
            errors.append(f"wikilink 指向不存在的页面: [[{link}]]")

    return errors


def validate_file(filepath, config, wiki_dir):
    """验证单个文件"""
    errors = []

    # 文件名验证
    filename_errors = validate_filename(filepath.name, config)
    errors.extend(filename_errors)

    # 读取内容
    content = filepath.read_text(encoding="utf-8")

    # Frontmatter 验证
    frontmatter, fm_error = parse_frontmatter(content)
    if fm_error:
        errors.append(fm_error)
    else:
        fm_errors = validate_frontmatter(frontmatter, filepath)
        errors.extend(fm_errors)

    # Wikilink 验证（排除日志文件）
    if filepath.name != "log.md":
        link_errors = validate_wikilinks(content, wiki_dir, filepath)
        errors.extend(link_errors)

    return errors


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "pm-wiki"
    target_path = Path(target)

    if not target_path.exists():
        print(f"错误: 路径不存在: {target}")
        sys.exit(1)

    config = load_config()
    wiki_dir = Path("pm-wiki")

    all_errors = {}
    total_files = 0
    total_errors = 0

    if target_path.is_file():
        files = [target_path]
    else:
        files = list(target_path.rglob("*.md"))

    for filepath in files:
        if filepath.name in ("index.md",):
            continue

        errors = validate_file(filepath, config, wiki_dir)
        total_files += 1

        if errors:
            all_errors[str(filepath)] = errors
            total_errors += len(errors)

    # 输出报告
    print("=" * 60)
    print("PM Agent 文档验证报告")
    print("=" * 60)
    print(f"验证文件数: {total_files}")
    print(f"问题总数: {total_errors}")
    print()

    if all_errors:
        for filepath, errors in all_errors.items():
            print(f"\n📄 {filepath}")
            for error in errors:
                print(f"   ❌ {error}")
    else:
        print("\n✅ 所有文件均符合规范！")

    print()
    print("=" * 60)

    if total_errors > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
