"""Document output writer."""

import logging
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from src.config import MODULE_DEFINITIONS, Settings

logger = logging.getLogger(__name__)

TEMPLATE_DIR = Path(__file__).parent.parent / "templates"


def write_module_doc(
    module_key: str,
    content: str,
    settings: Settings,
    accuracy_score: int = -1,
):
    """Write a module document to the output directory."""
    module_def = MODULE_DEFINITIONS[module_key]
    output_path = settings.output_path

    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("module_doc.md.j2")

    rendered = template.render(
        module_title=module_def["title"],
        content=content,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        accuracy_score=accuracy_score if accuracy_score >= 0 else "未验证",
    )

    filename = f"{module_def['id']}.md"
    filepath = output_path / filename
    filepath.write_text(rendered, encoding="utf-8")
    logger.info("Wrote documentation to %s", filepath)
    return filepath


def write_index(settings: Settings, generated_modules: list[str]):
    """Write an index file listing all generated documents."""
    output_path = settings.output_path
    lines = [
        "# Custom Dashboard 知识库文档索引",
        "",
        "> 本知识库由 document-automation 工具自动生成",
        f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 文档列表",
        "",
    ]

    for key in generated_modules:
        if key in MODULE_DEFINITIONS:
            mod = MODULE_DEFINITIONS[key]
            lines.append(f"- [{mod['title']}]({mod['id']}.md) - {mod['description']}")

    lines.extend([
        "",
        "## 数据源",
        "",
        "- 后端代码: `Pacvue/custom-dashboard` (Java/Spring Boot)",
        "- 前端代码: `Pacvue/CustomDashboard-modules-web` (Vue)",
        "- 技术评审: Confluence (35+ 篇)",
        "- PRD 文档: Confluence (19 篇)",
        "- 设计稿: Figma `Custom-Dashboard-Report`",
        "",
    ])

    index_path = output_path / "README.md"
    index_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Wrote index to %s", index_path)
