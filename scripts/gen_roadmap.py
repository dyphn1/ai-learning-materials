#!/usr/bin/env python3
"""
AI Learning Roadmap Generator
Scans markdown files in /Users/daniel.chang/Desktop/ai/docs/ and generates a learning roadmap.
"""

import os
import re
import datetime
from pathlib import Path

DOCS_DIR = Path("/Users/daniel.chang/Desktop/ai/docs")
OUTPUT_FILE = Path("/Users/daniel.chang/Desktop/ai/learning_roadmap.md")

def extract_title(content):
    """Extract the first heading as title."""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    return match.group(1).strip() if match else "Untitled"

def extract_terms_from_table(content):
    """Extract terms from markdown tables (first column)."""
    terms = []
    # Find table blocks
    table_pattern = r'(\|.*\|\n\|[-\s|]+\|\n(?:\|.*\|\n)+)'
    tables = re.findall(table_pattern, content)
    for table in tables:
        lines = table.strip().split('\n')
        # Skip header and separator
        for line in lines[2:]:
            if line.strip().startswith('|'):
                cols = [col.strip() for col in line.strip('|').split('|')]
                if cols:
                    terms.append(cols[0])  # First column as term
    return terms

def extract_terms_from_bold(content):
    """Extract terms from bold markdown."""
    # Find **term** patterns
    bold_pattern = r'\*\*([^*]+)\*\*'
    terms = re.findall(bold_pattern, content)
    # Filter out very short terms and common words
    filtered = []
    common = {'和', '或', '但', '的', '了', '是', '在', '有', '這', '那', '與', '及', '等'}
    for term in terms:
        term = term.strip()
        if len(term) > 1 and term not in common and not term.isdigit():
            filtered.append(term)
    return filtered

def extract_examples(content):
    """Extract code blocks as examples."""
    # Find code blocks (fenced with ```)
    code_pattern = r'```[^`]*```'
    blocks = re.findall(code_pattern, content, re.DOTALL)
    examples = []
    for block in blocks:
        # Remove the fences
        lines = block.strip().split('\n')
        if len(lines) > 2:  # Has content beyond fences
            code = '\n'.join(lines[1:-1]).strip()
            if code:
                examples.append(code)
    return examples

def process_file(filepath):
    """Process a single markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

    title = extract_title(content)
    terms_from_table = extract_terms_from_table(content)
    terms_from_bold = extract_terms_from_bold(content)
    
    # Combine and deduplicate
    all_terms = list(dict.fromkeys(terms_from_table + terms_from_bold))
    
    examples = extract_examples(content)
    
    return {
        'file': filepath.name,
        'title': title,
        'terms': all_terms,
        'examples': examples,
        'path': filepath
    }

def generate_roadmap():
    """Generate the learning roadmap markdown."""
    if not DOCS_DIR.exists():
        print(f"Docs directory not found: {DOCS_DIR}")
        return

    files = list(DOCS_DIR.glob("*.md"))
    if not files:
        print(f"No markdown files found in {DOCS_DIR}")
        return

    processed = []
    for f in files:
        data = process_file(f)
        if data:
            processed.append(data)

    # Sort by filename for consistent ordering
    processed.sort(key=lambda x: x['file'])

    # Generate markdown
    lines = []
    lines.append("# AI 學習路線拓樸 (Learning Roadmap Topology)")
    lines.append(f"*自動生成於: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    lines.append("")
    lines.append("## 總覽")
    lines.append("")
    lines.append("| 文件 | 主題 | 核心概念數量 |")
    lines.append("|------|------|--------------|")
    for p in processed:
        lines.append(f"| {p['file']} | {p['title']} | {len(p['terms'])} |")
    lines.append("")
    lines.append("## 詳細學習路線")
    lines.append("")
    
    for p in processed:
        lines.append(f"### {p['title']} (`{p['file']}`)")
        lines.append("")
        if p['terms']:
            lines.append("**核心概念與術語：**")
            for term in p['terms']:
                lines.append(f"- {term}")
            lines.append("")
        if p['examples']:
            lines.append("**實作範例摘錄：**")
            for i, example in enumerate(p['examples'][:2], 1):  # Limit to first 2 examples
                lines.append(f"```\n{example}\n```")
                lines.append("")
            if len(p['examples']) > 2:
                lines.append(f"*... 及另外 {len(p['examples'])-2} 個範例 ...*")
                lines.append("")
        lines.append("---\n")

    # Write output
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print(f"Roadmap generated: {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error writing roadmap: {e}")

if __name__ == "__main__":
    generate_roadmap()