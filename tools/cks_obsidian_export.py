#!/usr/bin/env python3
"""Производный экспорт CKS в Obsidian.

Этот модуль не создаёт второй Knowledge Runtime (рабочий контур знаний),
а использует существующий tools/cks_knowledge_runtime.py как источник
нормализованных объектов и представлений.

Obsidian здесь является визуальным слоем. Он не является SSOT (единым
источником истины), не принимает решения и не изменяет Canon (канон).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from cks_knowledge_runtime import KnowledgeRuntime, STATUS_RU


PIPELINE_COLUMNS = {
    "raw": 0,
    "captured": 0,
    "normalized": 1,
    "deduplicated": 1,
    "clustered": 2,
    "researched": 2,
    "understood": 2,
    "connected": 2,
    "validated": 2,
    "knowledge": 3,
    "evolving": 3,
    "disputed": 3,
    "canonical": 4,
    "superseded": 5,
    "archived": 5,
    "rejected": 5,
    "draft": 0,
    "review": 2,
    "active": 3,
}


def _slug(value: str) -> str:
    text = re.sub(r"[^0-9A-Za-zА-Яа-яЁё._-]+", "_", str(value).strip())
    return text.strip("_") or "объект"


def _note_link(object_id: str) -> str:
    return f"[[{object_id}]]"


class ObsidianExport:
    """Строит производную Obsidian-проекцию из существующего KnowledgeRuntime."""

    def __init__(self, runtime: KnowledgeRuntime) -> None:
        self.runtime = runtime

    def _write_text(self, root: Path, relative: str, text: str, written: list[str]) -> None:
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text.rstrip() + "\n", encoding="utf-8")
        written.append(relative.replace("\\", "/"))

    def _index_note(self, title: str, value: str, object_ids: list[str], kind: str) -> str:
        lines = [
            "---",
            'cks_authority: "derived_view_only"',
            f'cks_view_kind: "{kind}"',
            "---",
            "",
            f"# {title}: {value}",
            "",
            "> Производная навигационная заметка CKS. Не является источником истины.",
            "",
            f"Объектов: **{len(object_ids)}**",
            "",
        ]
        lines.extend(f"- {_note_link(object_id)}" for object_id in sorted(object_ids))
        return "\n".join(lines)

    def _navigation_block(self, record: dict[str, Any]) -> str:
        lines = ["", "## Навигация CKS", ""]
        for cluster in record.get("clusters", []):
            lines.append(f"- Кластер: [[Кластеры/{_slug(cluster)}|{cluster}]]")
        for tag in record.get("tags", []):
            lines.append(f"- Тег: [[Теги/{_slug(tag)}|{tag}]]")
        for project in record.get("projects", []):
            lines.append(f"- Проект-проекция: [[Проекты/{_slug(project)}|{project}]]")
        status = str(record.get("status") or "raw")
        lines.append(f"- Статус: [[Статусы/{_slug(status)}|{STATUS_RU.get(status, status)}]]")
        lines.extend([
            "",
            "> Навигация является производной. Изменения в Obsidian не меняют Canon автоматически.",
            "",
        ])
        return "\n".join(lines)

    def _canvas(self) -> dict[str, Any]:
        nodes: list[dict[str, Any]] = []
        edges: list[dict[str, Any]] = []
        node_ids: dict[str, str] = {}
        rows: dict[int, int] = defaultdict(int)

        for index, (object_id, record) in enumerate(sorted(self.runtime.records.items())):
            status = str(record.get("status") or "raw")
            column = PIPELINE_COLUMNS.get(status, 2)
            row = rows[column]
            rows[column] += 1
            canvas_id = f"n{index}"
            node_ids[object_id] = canvas_id
            nodes.append({
                "id": canvas_id,
                "type": "file",
                "file": f"Знания/{_slug(object_id)}.md",
                "x": column * 520,
                "y": row * 300,
                "width": 420,
                "height": 220,
            })

        edge_number = 0
        seen: set[tuple[str, str, str]] = set()
        for source_id, record in sorted(self.runtime.records.items()):
            for target_id, relation_type in self.runtime.relation_targets(record):
                if target_id not in node_ids:
                    continue
                key = (source_id, target_id, relation_type)
                if key in seen:
                    continue
                seen.add(key)
                edges.append({
                    "id": f"e{edge_number}",
                    "fromNode": node_ids[source_id],
                    "toNode": node_ids[target_id],
                    "fromSide": "right",
                    "toSide": "left",
                    "label": relation_type,
                })
                edge_number += 1

            for evidence in record.get("evidence", []):
                target_id = evidence if isinstance(evidence, str) else evidence.get("id") or evidence.get("reference")
                if not target_id or target_id not in node_ids:
                    continue
                key = (source_id, str(target_id), "доказательство")
                if key in seen:
                    continue
                seen.add(key)
                edges.append({
                    "id": f"e{edge_number}",
                    "fromNode": node_ids[source_id],
                    "toNode": node_ids[str(target_id)],
                    "fromSide": "right",
                    "toSide": "left",
                    "label": "доказательство",
                })
                edge_number += 1

        return {"nodes": nodes, "edges": edges}

    def export(self, vault_root: str | Path) -> dict[str, Any]:
        root = Path(vault_root)
        root.mkdir(parents=True, exist_ok=True)
        written: list[str] = []

        for directory in ("Знания", "Кластеры", "Теги", "Проекты", "Статусы", "Карты"):
            (root / directory).mkdir(parents=True, exist_ok=True)

        for object_id, record in sorted(self.runtime.records.items()):
            markdown = self.runtime.obsidian_markdown(record)
            markdown += self._navigation_block(record)
            self._write_text(root, f"Знания/{_slug(object_id)}.md", markdown, written)

        views = self.runtime.dynamic_views()
        for cluster, object_ids in views.get("по_кластерам", {}).items():
            self._write_text(
                root,
                f"Кластеры/{_slug(cluster)}.md",
                self._index_note("Кластер", cluster, object_ids, "cluster"),
                written,
            )
        for tag, object_ids in views.get("по_тегам", {}).items():
            self._write_text(
                root,
                f"Теги/{_slug(tag)}.md",
                self._index_note("Тег", tag, object_ids, "tag"),
                written,
            )
        for project, object_ids in views.get("по_проектам", {}).items():
            self._write_text(
                root,
                f"Проекты/{_slug(project)}.md",
                self._index_note("Проект-проекция", project, object_ids, "project_view"),
                written,
            )
        for status, object_ids in views.get("по_статусам", {}).items():
            self._write_text(
                root,
                f"Статусы/{_slug(status)}.md",
                self._index_note("Статус", STATUS_RU.get(status, status), object_ids, "status"),
                written,
            )

        overview = [
            "# CKS — визуальная база знаний",
            "",
            "> Эта папка может быть открыта в Obsidian как Vault (хранилище заметок).",
            "> Все файлы здесь являются производными представлениями. SSOT остаётся в объектах CKS.",
            "",
            "## Представления",
            "",
            "- [[Карты/CKS_Граф.canvas|Граф знаний]]",
            "- [[Кластеры]]",
            "- [[Теги]]",
            "- [[Проекты]]",
            "- [[Статусы]]",
            "",
            "## Путь от материала к знанию",
            "",
        ]
        for stage, payload in views.get("путь_материал_в_знание", {}).items():
            overview.append(f"- **{stage}**: {payload['count']}")
        overview.extend(["", "## Все объекты", ""])
        overview.extend(f"- {_note_link(object_id)}" for object_id in sorted(self.runtime.records))
        self._write_text(root, "CKS_Обзор.md", "\n".join(overview), written)

        for title, folder, key in (
            ("Кластеры", "Кластеры", "по_кластерам"),
            ("Теги", "Теги", "по_тегам"),
            ("Проекты", "Проекты", "по_проектам"),
            ("Статусы", "Статусы", "по_статусам"),
        ):
            lines = [f"# {title}", "", "> Производный индекс CKS.", ""]
            for value in sorted(views.get(key, {})):
                lines.append(f"- [[{folder}/{_slug(value)}|{value}]]")
            self._write_text(root, f"{title}.md", "\n".join(lines), written)

        canvas = self._canvas()
        canvas_path = root / "Карты" / "CKS_Граф.canvas"
        canvas_path.write_text(json.dumps(canvas, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written.append("Карты/CKS_Граф.canvas")

        guide = """# Obsidian + CKS\n\nОткройте эту папку в Obsidian как Vault (хранилище заметок).\n\nCKS использует:\n\n- Markdown-заметки объектов знаний;\n- YAML frontmatter (метаданные в начале заметки);\n- Wiki-ссылки `[[...]]`;\n- индексы кластеров, тегов, статусов и проектов-проекций;\n- Canvas `Карты/CKS_Граф.canvas` для графического обзора.\n\nПравило: Obsidian — только представление. Редактирование производных файлов не должно автоматически менять SSOT или Canon.\n"""
        self._write_text(root, "OBSIDIAN_CKS_README.md", guide, written)

        return {
            "status": "PASS",
            "authority": "derived_view_only",
            "objects": len(self.runtime.records),
            "written": written,
            "canvas": {
                "nodes": len(canvas["nodes"]),
                "edges": len(canvas["edges"]),
                "path": "Карты/CKS_Граф.canvas",
            },
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="CKS: экспорт визуальной базы в Obsidian")
    parser.add_argument("input", help="JSON-массив объектов CKS")
    parser.add_argument("vault", help="Каталог Obsidian Vault; может находиться прямо в Git-репозитории")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise SystemExit("Вход должен быть JSON-массивом объектов")

    runtime = KnowledgeRuntime()
    validation = runtime.ingest(payload)
    if validation["status"] == "FAIL":
        print(json.dumps({"validation": validation}, ensure_ascii=False, indent=2))
        return 1

    result = ObsidianExport(runtime).export(args.vault)
    print(json.dumps({"validation": validation, "obsidian": result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
