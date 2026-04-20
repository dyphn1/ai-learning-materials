# 本地模型部署指南
*來源檔案: topic-local-models.md*

## 核心概念
- Q8_0
- Q6_K
- Q5_K_M
- **Q4_K_M**
- Q3_K_M
- Q2_K
- gemma3:1b
- gemma3:4b
- gemma4:12b
- qwen3:8b
- deepseek-r1:8b
- gemma4:27b
- `gemma4:latest`
- `gemma4:e4b`
- `nomic-embed-text:latest`
- `openai/gpt-oss-120b:free`
- `nvidia/nemotron-3-super-120b:free`
- `google/gemma-4-26b-a4b-it:free`
- `arcee-ai/trinity-large-preview:free`
- 精度
- 速度
- Q4_K_M
- 建議
- 中等
- 現有模型
- 建議優先下載

## 實作範例
### 範例 1
```
brew install ollama
# 路徑：/opt/homebrew/bin/ollama
```

### 範例 2
```
ollama list                    # 列出已下載模型
ollama pull gemma4             # 下載模型
ollama run gemma4              # 互動式對話
ollama rm gemma4               # 刪除模型
ollama show gemma4 --modelfile # 查看模型設定
```

### 範例 3
```
# REST API（port 11434）
curl http://localhost:11434/api/chat -d '{
  "model": "gemma4",
  "messages": [{"role": "user", "content": "你好"}]
}'
```

### 範例 4
```
import ollama
response = ollama.chat(model='gemma4', messages=[
    {"role": "user", "content": "你好"}
])
print(response['message']['content'])
```

### 範例 5
```
所需 RAM ≈ 模型參數量（B）× 量化位元數 / 8 × 1.2（overhead）
```


---

*生成時間: 2026-04-20 21:18:47*