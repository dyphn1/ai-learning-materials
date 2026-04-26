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
GLOSSARY_STOP_TERMS = {
    "優點", "缺點", "問題", "內容", "中等", "建議", "建議起點", "建議優先下載",
    "成本", "速度", "特色", "指標", "精度", "穩定性", "風險", "解法", "衡量",
    "應用場景", "現有模型", "直觀理解", "分數解讀", "安全性測試", "防禦策略",
    "後置防護", "重試機制", "知識更新", "資料篩選", "分片佈署",
}


def extract_section(content, heading):
    """Extract a level-2 section by exact heading text."""
    pattern = rf'^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|\Z)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else ""


def extract_subsection(content, heading):
    """Extract a level-3 subsection by exact heading text."""
    pattern = rf'^###\s+{re.escape(heading)}\s*$\n(.*?)(?=^###\s+|^##\s+|\Z)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else ""


def strip_markdown_noise(text):
    """Remove headings, tables, fenced code, blockquotes, and links for summary extraction."""
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'\$\$.*?\$\$', '', text, flags=re.DOTALL)
    text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^#{1,6}\s+.*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\|.*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def extract_first_paragraph(text):
    """Extract the first non-empty paragraph from markdown content."""
    cleaned = strip_markdown_noise(text)
    for paragraph in cleaned.split('\n\n'):
        paragraph = ' '.join(line.strip() for line in paragraph.splitlines() if line.strip())
        if paragraph:
            return paragraph
    return ""


def shorten_paragraph(text, max_sentences=2):
    """Keep the first one or two Chinese/English sentences for note summary."""
    if not text:
        return ""
    parts = re.split(r'(?<=[。！？!?])\s+', text)
    parts = [part.strip() for part in parts if part.strip()]
    if not parts:
        return text.strip()
    return ' '.join(parts[:max_sentences]).strip()


def extract_bullets(text):
    """Extract markdown bullets or numbered list items."""
    bullets = []
    for line in text.splitlines():
        stripped = line.strip()
        if re.match(r'^[-*]\s+', stripped):
            bullets.append(re.sub(r'^[-*]\s+', '', stripped).strip())
        elif re.match(r'^\d+\.\s+', stripped):
            bullets.append(re.sub(r'^\d+\.\s+', '', stripped).strip())
    return bullets


def extract_table_rows(content):
    """Extract rows from the first markdown table in a section."""
    table_pattern = r'(\|.*\|\n\|[-\s|]+\|\n(?:\|.*\|\n?)+)'
    match = re.search(table_pattern, content)
    if not match:
        return []

    rows = []
    lines = match.group(1).strip().split('\n')
    for line in lines[2:]:
        if line.strip().startswith('|'):
            cols = [col.strip() for col in line.strip('|').split('|')]
            if len(cols) >= 3 and cols[0] and cols[1] and cols[2]:
                rows.append(cols)
    return rows


def extract_math_blocks(content):
    """Extract display math blocks."""
    return [block.strip() for block in re.findall(r'\$\$(.*?)\$\$', content, re.DOTALL)]


def normalize_term(term):
    """Normalize glossary terms for de-duplication."""
    term = re.sub(r'\*+', '', term or '').strip()
    term = re.sub(r'\s+', ' ', term)
    return term.strip('：:;；,.，。')


def is_glossary_term(term):
    """Filter out generic or noisy items that should not become glossary entries."""
    normalized = normalize_term(term)
    if len(normalized) < 2:
        return False
    if len(normalized) > 48:
        return False
    if normalized in GLOSSARY_STOP_TERMS:
        return False
    if re.fullmatch(r'[\d\W_]+', normalized):
        return False
    if any(symbol in normalized for symbol in ['。', '！', '？']):
        return False
    if normalized.count('，') > 1 or normalized.count(',') > 2:
        return False
    if any(token in normalized for token in ["生成時間", "同步更新", "最後更新"]):
        return False
    return True


def build_glossary_entries(data):
    """Build glossary entries with definition/source from processed doc data."""
    entries = []
    seen = set()

    for row in data['term_rows']:
        term = normalize_term(row[0])
        if not is_glossary_term(term) or term in seen:
            continue
        seen.add(term)
        definition = normalize_term(row[1])
        mechanism = normalize_term(row[2])
        summary = definition
        if mechanism and mechanism != definition:
            summary = f"{definition}；核心機制：{mechanism}"
        entries.append({
            'term': term,
            'summary': summary,
            'source_file': data['file'],
            'source_title': data['title'],
        })

    for term in data['terms']:
        normalized = normalize_term(term)
        if not is_glossary_term(normalized) or normalized in seen:
            continue
        seen.add(normalized)
        entries.append({
            'term': normalized,
            'summary': f"在《{data['title']}》中出現的核心術語，建議回看對應主文與學習筆記理解完整上下文。",
            'source_file': data['file'],
            'source_title': data['title'],
        })

    return entries

def extract_title(content):
    """Extract the first heading as title."""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    return match.group(1).strip() if match else "Untitled"

def extract_terms_from_table(content):
    """Extract terms from markdown tables (first column)."""
    terms = []
    for cols in extract_table_rows(content):
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
    """Extract runnable code blocks and prioritize real examples over diagrams."""
    code_pattern = r'```([^\n`]*)\n(.*?)```'
    blocks = re.findall(code_pattern, content, re.DOTALL)
    examples = []
    prioritized = []
    fallback = []
    priorities = {
        'python': 0,
        'bash': 1,
        'sh': 1,
        'zsh': 1,
        'json': 2,
        'yaml': 3,
    }

    for language, code in blocks:
        lang = language.strip().lower()
        snippet = code.strip()
        if not snippet or lang == 'mermaid':
            continue

        item = {
            'language': lang or 'text',
            'code': snippet,
        }
        if lang in priorities:
            prioritized.append((priorities[lang], item))
        else:
            fallback.append(item)

    for _, item in sorted(prioritized, key=lambda x: x[0]):
        examples.append(item)
    examples.extend(fallback)
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
    
    overview = extract_section(content, "概覽與設計動機")
    mechanism = extract_section(content, "核心機制深度解析")
    engineering = extract_section(content, "工程實作")
    self_check = extract_section(content, "自我驗證練習")
    problems = extract_section(content, "已知限制與 Open Problems")

    term_rows = extract_table_rows(mechanism)
    flow_candidates = (
        extract_subsection(mechanism, "演算法流程")
        or extract_subsection(mechanism, "提示設計流程")
        or extract_subsection(mechanism, "從資料到推理的流程")
        or extract_subsection(mechanism, "控制流程")
    )
    validation = extract_subsection(engineering, "預期觀察")

    return {
        'file': filepath.name,
        'title': title,
        'terms': all_terms,
        'examples': examples,
        'path': filepath,
        'overview': shorten_paragraph(extract_first_paragraph(overview)),
        'term_rows': term_rows,
        'flow': extract_bullets(flow_candidates),
        'math_blocks': extract_math_blocks(content),
        'validation': extract_bullets(validation),
        'self_check': extract_bullets(self_check),
        'problems': extract_bullets(problems),
        'glossary_entries': [],
    }


def build_study_notes(data):
    """Build a richer study-note structure from document sections."""
    lines = []
    lines.append(f"# {data['title']} 學習筆記")
    lines.append(f"*來源檔案: {data['file']}*")
    lines.append(f"*同步更新: {datetime.datetime.now().strftime('%Y-%m-%d')}*")
    lines.append("")

    lines.append("## 一句話理解")
    lines.append(data['overview'] or "*無法自動摘要，請回看主文的概覽與設計動機章節。*")
    lines.append("")

    lines.append("## 必記重點")
    highlights = []
    for row in data['term_rows'][:5]:
        highlights.append(f"{row[0]}：{row[2]}")
    if not highlights:
        highlights = data['flow'][:5] or data['terms'][:5]
    if highlights:
        for item in highlights:
            lines.append(f"- {item}")
    else:
        lines.append("*無可用重點，請回看主文。*")
    lines.append("")

    lines.append("## 核心名詞速記")
    if data['term_rows']:
        for row in data['term_rows'][:6]:
            lines.append(f"- {row[0]}：{row[1]}")
    elif data['terms']:
        for term in data['terms'][:8]:
            lines.append(f"- {term}")
    else:
        lines.append("*無核心名詞資料*")
    lines.append("")

    if data['flow']:
        lines.append("## 流程速記")
        for index, item in enumerate(data['flow'], 1):
            lines.append(f"{index}. {item}")
        lines.append("")

    lines.append("## 必背公式")
    if data['math_blocks']:
        for block in data['math_blocks'][:2]:
            lines.append("$$")
            lines.append(block)
            lines.append("$$")
            lines.append("")
    else:
        lines.append("*本篇無核心公式*")
        lines.append("")

    lines.append("## 實作範例重點")
    if data['examples']:
        lines.append("### 範例片段")
        example = data['examples'][0]
        lines.append(f"```{example['language']}")
        lines.append(example['code'])
        lines.append("```")
        lines.append("")
    else:
        lines.append("*無實作範例*")
        lines.append("")

    if data['validation']:
        lines.append("### 驗證時要觀察什麼")
        for item in data['validation']:
            lines.append(f"- {item}")
        lines.append("")

    if data['problems']:
        lines.append("## 常見限制")
        for item in data['problems'][:5]:
            lines.append(f"- {item}")
        lines.append("")

    lines.append("## 自我檢查")
    if data['self_check']:
        for item in data['self_check'][:5]:
            lines.append(f"- {item}")
    else:
        lines.append("*無自我檢查題目*")

    return '\n'.join(lines)

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
    glossary_entries = {}

    for f in files:
        data = process_file(f)
        if data:
            data['glossary_entries'] = build_glossary_entries(data)
            processed.append(data)
            for entry in data['glossary_entries']:
                term = entry['term']
                if term not in glossary_entries:
                    glossary_entries[term] = entry

    # Sort by filename
    processed.sort(key=lambda x: x['file'])

    # Generate individual study notes
    for p in processed:
        content = build_study_notes(p)
        
        # Create safe filename
        safe_name = p['file'].replace('.md', '_study_notes.md')
        out_path = MATERIALS_DIR / safe_name
        try:
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Generated study notes: {out_path}")
        except Exception as e:
            print(f"Error writing study notes for {p['file']}: {e}")

    # Generate glossary
    glossary_lines = []
    glossary_lines.append("# AI 術語表 (Glossary)")
    glossary_lines.append(f"*自動生成於: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    glossary_lines.append("")
    glossary_lines.append("以下術語依據主文中的名詞拆解表與核心術語自動整理，並附上簡短定義與來源。")
    glossary_lines.append("")
    for term in sorted(glossary_entries):
        entry = glossary_entries[term]
        glossary_lines.append(f"## {entry['term']}")
        glossary_lines.append(f"- 定義：{entry['summary']}")
        glossary_lines.append(f"- 來源：{entry['source_title']} ({entry['source_file']})")
        glossary_lines.append("")
    glossary_lines.append("")
    glossary_lines.append(f"*共 {len(glossary_entries)} 個術語*")
    glossary_lines.append("")
    glossary_lines.append("---\n")
    glossary_lines.append("*說明：此詞彙表優先採用主文名詞拆解表中的定義；若來源沒有明確定義，則保留為導讀式條目。*")
    
    try:
        with open(GLOSSARY_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(glossary_lines))
        print(f"Generated glossary: {GLOSSARY_FILE}")
    except Exception as e:
        print(f"Error writing glossary: {e}")

if __name__ == "__main__":
    generate_learning_materials()