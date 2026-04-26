# AI 模型評測框架指南 學習筆記
*來源檔案: topic-evaluation.md*
*同步更新: 2026-04-26*

## 一句話理解
*無法自動摘要，請回看主文的概覽與設計動機章節。*

## 必記重點
- 內容
- 衡量
- 分數解讀
- 指標
- 自動評測與回歸測試

## 核心名詞速記
- 內容
- 衡量
- 分數解讀
- 指標
- 自動評測與回歸測試
- 應用場景

## 必背公式
*本篇無核心公式*

## 實作範例重點
### 範例片段
```python
import ollama

test_cases = [
    {"prompt": "2 + 2 = ?", "expected": "4"},
    {"prompt": "台灣首都是哪裡？", "expected": "台北"},
]

for case in test_cases:
    resp = ollama.chat(model='gemma4', messages=[{"role":"user","content":case["prompt"]}])
    answer = resp['message']['content']
    passed = case["expected"] in answer
    print(f"{'✅' if passed else '❌'} {case['prompt'][:20]}...")
```

## 自我檢查
*無自我檢查題目*