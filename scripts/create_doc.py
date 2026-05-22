#!/usr/bin/env python3
"""
PM Agent - 文档创建工具

用法:
    python create_doc.py <workflow> <title>

参数:
    workflow   工作流类型: spec, roadmap, update, research, competitive,
                         metrics, idea, sprint, retrospective,
                         release, journey
    title      文档标题（支持中文）

示例:
    python create_doc.py spec "碳金融交易管理PRD-v1.0"
    python create_doc.py sprint "Sprint-12"
    python create_doc.py retrospective "2026-Q2-复盘"

功能:
    1. 根据工作流类型自动选择模板
    2. 按命名规范生成文件名
    3. 填充 frontmatter
    4. 保存到正确的知识库目录
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
        print("错误: 未找到 config.yaml，请确保在 pm-agent 根目录运行")
        sys.exit(1)
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def slugify(title):
    """将标题转换为文件名安全的字符串"""
    # 保留中文，只移除危险字符
    safe = re.sub(r'[<>"/\\|?*]', '', title)
    safe = safe.strip()
    return safe


def generate_filename(workflow_key, title, date_str):
    """按命名规范生成文件名"""
    workflow_map = {
        "spec": ("specs", f"{date_str}-{slugify(title)}.md"),
        "roadmap": ("roadmaps", f"roadmap-{date_str[:7]}.md"),
        "update": ("updates", f"{date_str}-{slugify(title)}.md"),
        "research": ("research", f"{date_str}-{slugify(title)}.md"),
        "competitive": ("competitive", f"{date_str}-{slugify(title)}.md"),
        "metrics": ("metrics", f"{date_str}-{slugify(title)}.md"),
        "idea": ("ideas", f"{date_str}-{slugify(title)}.md"),
        "sprint": ("sprints", f"{date_str}-{slugify(title)}.md"),
        "retrospective": ("retrospectives", f"{date_str}-{slugify(title)}.md"),
        "release": ("releases", f"{date_str}-{slugify(title)}.md"),
        "journey": ("journeys", f"{date_str}-{slugify(title)}.md"),
    }
    return workflow_map.get(workflow_key, (None, None))


def fill_frontmatter(template_content, title, date_str, config):
    """填充 frontmatter 和模板变量"""
    defaults = config.get("frontmatter_defaults", {})

    # 替换 frontmatter 中的占位符
    content = template_content.replace("{{title}}", title)
    content = content.replace("{{date}}", date_str)

    # 替换其他常见占位符
    content = content.replace("{{timeframe}}", "")
    content = content.replace("{{scope}}", "")
    content = content.replace("{{context}}", "")
    content = content.replace("{{competitor_1}}", "竞品 A")
    content = content.replace("{{competitor_2}}", "竞品 B")
    content = content.replace("{{user_type_1}}", "用户类型 1")
    content = content.replace("{{user_type_2}}", "用户类型 2")
    content = content.replace("{{metric_1}}", "指标 1")
    content = content.replace("{{metric_2}}", "指标 2")
    content = content.replace("{{highlight_1}}", "亮点 1")
    content = content.replace("{{concern_1}}", "关注 1")
    content = content.replace("{{project_1}}", "项目 1")
    content = content.replace("{{project_2}}", "项目 2")
    content = content.replace("{{project_3}}", "项目 3")
    content = content.replace("{{project_4}}", "项目 4")
    content = content.replace("{{persona_1}}", "用户画像 1")
    content = content.replace("{{persona_2}}", "用户画像 2")
    content = content.replace("{{team}}", "")
    content = content.replace("{{version}}", "")
    content = content.replace("{{release_date}}", "")
    content = content.replace("{{persona}}", "")
    content = content.replace("{{theme}}", "")
    content = content.replace("{{start_date}}", date_str)
    content = content.replace("{{end_date}}", "")
    content = content.replace("{{team_size}}", "")

    return content


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    workflow_key = sys.argv[1]
    title = sys.argv[2]

    config = load_config()
    date_str = datetime.now().strftime(config.get("project", {}).get("date_format", "%Y-%m-%d"))

    # 查找工作流配置
    workflows = config.get("workflows", {})
    workflow_config = None
    for key, wf in workflows.items():
        wf_type = wf.get("frontmatter_type", "")
        if wf_type == workflow_key or key.replace("-", "") == workflow_key.replace("-", ""):
            workflow_config = wf
            break

    # 支持简写映射
    alias_map = {
        "spec": "write-spec",
        "roadmap": "roadmap-update",
        "update": "stakeholder-update",
        "research": "synthesize-research",
        "competitive": "competitive-brief",
        "metrics": "metrics-review",
        "idea": "brainstorm",
        "sprint": "sprint-planning",
        "retrospective": "retrospective",
        "release": "release-planning",
        "journey": "user-journey-map",
    }

    if workflow_config is None:
        mapped = alias_map.get(workflow_key)
        if mapped and mapped in workflows:
            workflow_config = workflows[mapped]

    if workflow_config is None:
        print(f"错误: 未知工作流 '{workflow_key}'")
        print(f"可用工作流: {', '.join(alias_map.keys())}")
        sys.exit(1)

    template_path = workflow_config.get("template")
    if not template_path:
        print(f"工作流 '{workflow_key}' 无模板（如 brainstorm），跳过创建")
        sys.exit(0)

    # 读取模板
    template_file = Path(template_path)
    if not template_file.exists():
        print(f"错误: 模板文件不存在: {template_path}")
        sys.exit(1)

    template_content = template_file.read_text(encoding="utf-8")

    # 填充内容
    content = fill_frontmatter(template_content, title, date_str, config)

    # 确定保存路径
    subdir, filename = generate_filename(workflow_key, title, date_str)
    if subdir is None:
        print(f"错误: 无法为工作流 '{workflow_key}' 生成文件名")
        sys.exit(1)

    save_dir = Path("pm-wiki") / subdir
    save_dir.mkdir(parents=True, exist_ok=True)
    save_path = save_dir / filename

    # 检查文件是否已存在
    if save_path.exists():
        print(f"警告: 文件已存在: {save_path}")
        overwrite = input("是否覆盖? (y/N): ").strip().lower()
        if overwrite != "y":
            print("已取消")
            sys.exit(0)

    # 保存文件
    save_path.write_text(content, encoding="utf-8")
    print(f"✅ 已创建: {save_path}")
    print(f"   工作流: {workflow_key}")
    print(f"   标题: {title}")
    print(f"   日期: {date_str}")

    # 提示后续操作
    print(f"\n下一步:")
    print(f"  1. 编辑文档: {save_path}")
    print(f"  2. 运行 'python scripts/update_index.py' 更新索引")
    print(f"  3. 运行 'python scripts/validate.py' 检查规范")


if __name__ == "__main__":
    main()
