#!/usr/bin/env python3
"""
Generate targeted deep-dive task files only for docs that fail quality gates.

The goal is to keep tasks as a small backlog of concrete doc gaps, instead of
mass-producing generic templates that duplicate the source docs.
"""

import datetime
import re
from pathlib import Path

DOCS_DIR = Path("/Users/daniel.chang/Desktop/ai/docs")
TASKS_DIR = Path("/Users/daniel.chang/Desktop/ai/tasks")

MIN_CONTENT_CHARS = 1500
AUTO_GENERATED_MARKER = "*此文件由腳本自動生成"
PAPER_PATTERN = re.compile(
    r"arxiv:\d{4}\.\d{4,5}|https?://(?:arxiv\.org/abs/|doi\.org/)",
    re.IGNORECASE,
)

def task_filename(source_name: str) -> str:
    return f"deep-{source_name}"

def strip_code_blocks(content: str) -> str:
    return re.sub(r"```.*?```", " ", content, flags=re.DOTALL)


def estimate_content_chars(content: str) -> int:
    text = strip_code_blocks(content)
    text = re.sub(r"!\[[^\]]*\]\([^\)]*\)", " ", text)
    text = re.sub(r"\[[^\]]*\]\([^\)]*\)", " ", text)
    text = re.sub(r"[#>*_`|\-]", " ", text)
    text = re.sub(r"\s+", "", text)
    return len(text)


def is_auto_generated_task(task_path: Path) -> bool:
    if not task_path.exists():
        return False
    content = task_path.read_text(encoding="utf-8")
    return AUTO_GENERATED_MARKER in content


def audit_doc(source_path: Path) -> dict:
    content = source_path.read_text(encoding="utf-8")
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else source_path.stem

    content_chars = estimate_content_chars(content)
    has_paper_ref = bool(PAPER_PATTERN.search(content))
    has_code_example = "```python" in content or "```bash" in content
    has_update_record = "## 更新記錄" in content
    has_tradeoff = "trade-off" in content.lower() or "限制" in content or "適用場景" in content
    has_term_breakdown = any(
        marker in content
        for marker in ["什麼是", "核心概念", "關鍵名詞", "術語", "概覽與設計動機"]
    )
    has_validation = any(
        marker in content
        for marker in ["驗證", "實驗", "練習", "預期觀察", "快速實驗步驟"]
    )

    missing_items = []
    if content_chars < MIN_CONTENT_CHARS:
        missing_items.append(f"主文內容估計僅 {content_chars} 字，低於 {MIN_CONTENT_CHARS} 字門檻")
    if not has_paper_ref:
        missing_items.append("缺少 arXiv / DOI / 官方技術來源引用")
    if not has_code_example:
        missing_items.append("缺少可執行範例（至少一段 python 或 bash）")
    if not has_update_record:
        missing_items.append("缺少更新記錄章節")
    if not has_tradeoff:
        missing_items.append("缺少限制、trade-off 或適用場景分析")
    if not has_term_breakdown:
        missing_items.append("缺少關鍵名詞 / 專案 / 框架的深入拆解")
    if not has_validation:
        missing_items.append("缺少最小驗證步驟或練習")

    return {
        "title": title,
        "doc_path": str(source_path),
        "content_chars": content_chars,
        "missing_items": missing_items,
        "needs_task": bool(missing_items),
    }

def build_task_content(audit: dict) -> str:
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    today = datetime.date.today().isoformat()

    lines = []
    lines.append(f"# 深度學習任務 - {audit['title']}")
    lines.append("")
    lines.append(f"> 建立日期：{today}")
    lines.append(f"> 對應 doc：{audit['doc_path']}")
    lines.append("> 狀態：待執行")
    lines.append("")
    lines.append("## 為何需要補強")
    lines.append(f"- 主文內容估計：{audit['content_chars']} 字")
    for item in audit['missing_items']:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Docs-first 執行規則")
    lines.append("- [ ] 先修改對應 doc 主文，再補 references，最後才更新 task 狀態")
    lines.append("- [ ] 不可只重寫 task 模板或只補摘要")
    lines.append("- [ ] 本任務完成的判定標準是 doc 深度提升，而不是 task 被勾選")
    lines.append("")
    lines.append("## 必達驗收標準")
    lines.append("- [ ] 至少補上 1 個 arXiv / DOI / 官方技術來源")
    lines.append("- [ ] 至少補上 1 個可執行範例（含環境設定）")
    lines.append("- [ ] 補上關鍵名詞 / 專案 / 框架的定義、核心機制、限制與替代方案")
    lines.append("- [ ] 補上 trade-off、適用場景與不適用場景")
    lines.append("- [ ] 補上更新記錄")
    lines.append("- [ ] 補上最小驗證步驟或練習")
    lines.append("")
    lines.append("## 建議研究方向")
    lines.append("- [ ] 原始論文（arXiv / DOI）")
    lines.append("- [ ] 官方文件或框架文件")
    lines.append("- [ ] 生產環境實作案例 / 工程部落格")
    lines.append("- [ ] 2025-2026 最新進展與衍生技術")
    lines.append("")
    lines.append("## 參考來源（執行後補充）")
    lines.append("- [ ] 論文：")
    lines.append("- [ ] 官方文件：")
    lines.append("- [ ] 工程部落格：")
    lines.append("")
    lines.append("*此文件由腳本自動生成，內容為 docs 缺口稽核結果*")
    lines.append(f"*生成時間：{now}*")
    return '\n'.join(lines)

def main():
    if not DOCS_DIR.exists():
        print(f"Docs directory not found: {DOCS_DIR}")
        return
    if not TASKS_DIR.exists():
        print(f"Tasks directory not found: {TASKS_DIR}")
        return

    for source_path in sorted(DOCS_DIR.glob("*.md")):
        audit = audit_doc(source_path)
        task_path = TASKS_DIR / task_filename(source_path.name)

        if not audit["needs_task"]:
            if is_auto_generated_task(task_path):
                task_path.unlink()
                print(f"Removed stale auto-generated task: {task_path.name}")
            else:
                print(f"Skip {source_path.name}: meets quality gates")
            continue

        if task_path.exists() and not is_auto_generated_task(task_path):
            print(f"Skip {task_path.name}: manual task file preserved")
            continue

        task_path.write_text(build_task_content(audit), encoding="utf-8")
        print(f"Generated targeted task: {task_path.name}")

if __name__ == "__main__":
    main()