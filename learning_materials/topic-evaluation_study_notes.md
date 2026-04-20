# AI 模型評測框架指南
*來源檔案: topic-evaluation.md*

## 核心概念
- 內容
- 衡量
- 分數解讀
- 指標
- 自動評測與回歸測試
- 應用場景

## 實作範例
### 範例 1
```
pip install lm-eval

# 評測本地 Ollama 模型
lm_eval --model local-completions \
  --model_args base_url=http://localhost:11434/v1,model=gemma4 \
  --tasks mmlu \
  --num_fewshot 5
```

### 範例 2
```
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


---

*生成時間: 2026-04-20 21:18:47*