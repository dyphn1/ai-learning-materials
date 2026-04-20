#!/usr/bin/env python3
"""
AI Learning Materials Generator
Generates study notes and glossary from markdown files in /Users/daniel.chang/Desktop/ai/docs/
"""

import os
import re
import datetime
from pathlib import Path

DOCS_DIR = Path("/Users/daniel.chang/Desktop/ai/docs")
MATERIALS_DIR = Path("/Users/daniel.chang/Desktop/ai/learning_materials")
GLOSSARY_FILE = MATERIALS_DIR / "AI_Glossary.md"

def extract_title(content):
    """Extract the first heading as title."""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    return match.group(1).strip() if match else "Untitled"

def extract_terms_from_table(content):
    """Extract terms from markdown tables (first column)."""
    terms = []
    table_pattern = r'(\|.*\|\n\|[-\s|]+\|\n(?:\|.*\|\n)+)'
    tables = re.findall(table_pattern, content)
    for table in tables:
        lines = table.strip().split('\n')
        for line in lines[2:]:
            if line.strip().startswith('|'):
                cols = [col.strip() for col in line.strip('|').split('|')]
                if cols:
                    terms.append(cols[0])
    return terms

def extract_terms_from_bold(content):
    """Extract terms from bold markdown."""
    bold_pattern = r'\*\*([^*]+)\*\*'
    terms = re.findall(bold_pattern, content)
    filtered = []
    common = {'和', '或', '但', '的', '了', '是', '在', '有', '這', '那', '與', '及', '等'}
    for term in terms:
        term = term.strip()
        if len(term) > 1 and term not in common and not term.isdigit():
            filtered.append(term)
    return filtered

def extract_examples(content):
    """Extract code blocks as examples."""
    code_pattern = r'```[^`]*```'
    blocks = re.findall(code_pattern, content, re.DOTALL)
    examples = []
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) > 2:
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
    all_terms = list(dict.fromkeys(terms_from_table + terms_from_bold))
    examples = extract_examples(content)
    
    return {
        'file': filepath.name,
        'title': title,
        'terms': all_terms,
        'examples': examples,
        'path': filepath
    }

def generate_learning_materials():
    """Generate learning materials for each file and a glossary."""
    if not DOCS_DIR.exists():
        print(f"Docs directory not found: {DOCS_DIR}")
        return

    MATERIALS_DIR.mkdir(exist_ok=True)
    
    files = list(DOCS_DIR.glob("*.md"))
    if not files:
        print(f"No markdown files found in {DOCS_DIR}")
        return

    processed = []
    all_terms_set = set()

    for f in files:
        data = process_file(f)
        if data:
            processed.append(data)
            all_terms_set.update(data['terms'])

    # Sort by filename
    processed.sort(key=lambda x: x['file'])

    # Generate individual study notes
    for p in processed:
        lines = []
        lines.append(f"# {p['title']}")
        lines.append(f"*來源檔案: {p['file']}*")
        lines.append("")
        lines.append("## 核心概念")
        if p['terms']:
            for term in p['terms']:
                lines.append(f"- {term}")
        else:
            lines.append("*無核心概念資料*")
        lines.append("")
        lines.append("## 實作範例")
        if p['examples']:
            for i, example in enumerate(p['examples'], 1):
                lines.append(f"### 範例 {i}")
                lines.append("```")
                lines.append(example)
                lines.append("```")
                lines.append("")
        else:
            lines.append("*無實作範例*")
        lines.append("")
        lines.append("---\n")
        lines.append(f"*生成時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        # Create safe filename
        safe_name = p['file'].replace('.md', '_study_notes.md')
        out_path = MATERIALS_DIR / safe_name
        try:
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            print(f"Generated study notes: {out_path}")
        except Exception as e:
            print(f"Error writing study notes for {p['file']}: {e}")

    # Generate glossary
    glossary_lines = []
    glossary_lines.append("# AI 術語表 (Glossary)")
    glossary_lines.append(f"*自動生成於: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    glossary_lines.append("")
    glossary_lines.append("以下是從所有學習文件中提取的核心術語列表：")
    glossary_lines.append("")
    sorted_terms = sorted(list(all_terms_set))
    for term in sorted_terms:
        glossary_lines.append(f"- {term}")
    glossary_lines.append("")
    glossary_lines.append(f"*共 {len(sorted_terms)} 個術語*")
    glossary_lines.append("")
    glossary_lines.append("---\n")
    glossary_lines.append("*說明：此詞彙表僅列出術語，詳細定義請參考對應的學習筆記。*")
    
    try:
        with open(GLOSSARY_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(glossary_lines))
        print(f"Generated glossary: {GLOSSARY_FILE}")
    except Exception as e:
        print(f"Error writing glossary: {e}")

if __name__ == "__main__":
    generate_learning_materials()