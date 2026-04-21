# 深度學習任務清單 - topic-evaluation

## 架構深度解析
- [ ] 了解原理
- [ ] 流程圖說明
- [ ] 核心元件拆解

## 實作範例
- [ ] 完整可執行程式碼範例（含環境設定）

### 參考程式碼片段
**片段 1：**
```
bash
pip install lm-eval

# 評測本地 Ollama 模型
lm_eval --model local-completions \
  --model_args base_url=http://localhost:11434/v1,model=gemma4 \
  --tasks mmlu \
  --num_fewshot 5
```

**片段 2：**
```
python
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


## 應用場景
- [ ] 案例 1
- [ ] 案例 2
- [ ] 案例 3

### 相關概念與術語
- 內容
- 衡量
- 分數解讀
- 指標
- 自動評測與回歸測試
- 應用場景

## 擴充與進階
- [ ] 進階技術
- [ ] 變體
- [ ] 相關論文

## 優化技巧
- [ ] 常見問題與解決方案
- [ ] 效能調優方法

## 參考資源
- [ ] 搜尋相關文章並填入 URL

*此文件由腳本自動生成，來源：topic-evaluation.md*
*生成時間：2026-04-21 20:06:43*