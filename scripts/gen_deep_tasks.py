#!/usr/bin/env python3
"""
Generate deep learning task files from the topic markdown files in docs/.
Each deep-*.md will be filled with sections based on the source file.
"""

import os
import re
from pathlib import Path

DOCS_DIR = Path("/Users/daniel.chang/Desktop/ai/docs")
TASKS_DIR = Path("/Users/daniel.chang/Desktop/ai/tasks")

# Mapping from task file to source file (if not direct)
# Actually deep-level1-ai-basics.md corresponds to level1-ai-basics.md, etc.
# So we can derive source name by removing 'deep-' prefix and maybe adjusting.
def source_filename(task_name: str) -> str:
    # task_name like "deep-level1-ai-basics.md"
    # remove 'deep-' -> "level1-ai-basics.md"
    if task_name.startswith("deep-"):
        return task_name[5:]
    return task_name

def extract_sections(content):
    """Extract some useful sections from markdown: maybe tables, bold terms, code blocks."""
    # We'll just return some placeholder content for now.
    # But we can try to extract useful bits.
    sections = {}
    # Find tables
    table_pattern = r'(\|.*\|\n\|[-\s|]+\|\n(?:\|.*\|\n)+)'
    tables = re.findall(table_pattern, content)
    sections['tables'] = tables[:2]  # limit
    
    # Find bold terms
    bold_pattern = r'\*\*([^*]+)\*\*'
    bold_terms = re.findall(bold_pattern, content)
    # filter
    common = {'和', '或', '但', '的', '了', '是', '在', '有', '這', '那', '與', '及', '等'}
    filtered = [t.strip() for t in bold_terms if len(t.strip()) > 1 and t.strip() not in common and not t.strip().isdigit()]
    sections['bold_terms'] = list(dict.fromkeys(filtered))[:20]
    
    # Find code blocks
    code_pattern = r'```[^`]*```'
    code_blocks = re.findall(code_pattern, content, re.DOTALL)
    sections['code_blocks'] = [b.strip('` \n') for b in code_blocks if b.strip('` \n')][:3]
    
    # Extract first few lines after each heading maybe.
    # We'll just return the sections.
    return sections

def generate_deep_content(source_path: Path, task_path: Path):
    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {source_path}: {e}")
        return
    
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else source_path.stem
    
    sections = extract_sections(content)
    
    # Build the deep task content
    lines = []
    lines.append(f"# 深度學習任務清單 - {source_path.stem}")
    lines.append("")
    lines.append("## 架構深度解析")
    lines.append("- [ ] 了解原理")
    lines.append("- [ ] 流程圖說明")
    lines.append("- [ ] 核心元件拆解")
    lines.append("")
    lines.append("## 實作範例")
    lines.append("- [ ] 完整可執行程式碼範例（含環境設定）")
    if sections['code_blocks']:
        lines.append("")
        lines.append("### 參考程式碼片段")
        for i, cb in enumerate(sections['code_blocks'][:2], 1):
            lines.append(f"**片段 {i}：**")
            lines.append("```")
            lines.append(cb)
            lines.append("```")
            lines.append("")
    lines.append("")
    lines.append("## 應用場景")
    lines.append("- [ ] 案例 1")
    lines.append("- [ ] 案例 2")
    lines.append("- [ ] 案例 3")
    if sections['bold_terms']:
        lines.append("")
        lines.append("### 相關概念與術語")
        for term in sections['bold_terms'][:10]:
            lines.append(f"- {term}")
    lines.append("")
    lines.append("## 擴充與進階")
    lines.append("- [ ] 進階技術")
    lines.append("- [ ] 變體")
    lines.append("- [ ] 相關論文")
    if sections['tables']:
        lines.append("")
        lines.append("### 參考表格")
        for i, table in enumerate(sections['tables'][:2], 1):
            lines.append(f"**表格 {i}：**")
            lines.append(table)
            lines.append("")
    lines.append("")
    lines.append("## 優化技巧")
    lines.append("- [ ] 常見問題與解決方案")
    lines.append("- [ ] 效能調優方法")
    lines.append("")
    lines.append("## 參考資源")
    lines.append("- [ ] 搜尋相關文章並填入 URL")
    lines.append("")
    lines.append(f"*此文件由腳本自動生成，來源：{source_path.name}*")
    lines.append(f"*生成時間：{os.popen('date +%Y-%m-%d\\ %H:%M:%S').read().strip()}*")
    
    # Write to task file
    try:
        with open(task_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print(f"Generated deep task: {task_path}")
    except Exception as e:
        print(f"Error writing {task_path}: {e}")

def main():
    if not DOCS_DIR.exists():
        print(f"Docs directory not found: {DOCS_DIR}")
        return
    if not TASKS_DIR.exists():
        print(f"Tasks directory not found: {TASKS_DIR}")
        return
    
    # Process each deep-*.md in tasks/
    for task_file in TASKS_DIR.glob("deep-*.md"):
        source_name = source_filename(task_file.name)
        source_path = DOCS_DIR / source_name
        if not source_path.exists():
            print(f"Source file not found for {task_file.name}: {source_path}")
            continue
        generate_deep_content(source_path, task_file)

if __name__ == "__main__":
    main()