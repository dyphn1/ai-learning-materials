# 本地模型部署指南

## 學習目標
掌握使用 Ollama 在本機部署並執行 LLM 的完整流程。

---

## Ollama 使用指南

### 安裝（已完成）
```bash
brew install ollama
# 路徑：/opt/homebrew/bin/ollama
```

### 基本指令
```bash
ollama list                    # 列出已下載模型
ollama pull gemma4             # 下載模型
ollama run gemma4              # 互動式對話
ollama rm gemma4               # 刪除模型
ollama show gemma4 --modelfile # 查看模型設定
```

### API 使用
```bash
# REST API（port 11434）
curl http://localhost:11434/api/chat -d '{
  "model": "gemma4",
  "messages": [{"role": "user", "content": "你好"}]
}'
```

```python
import ollama
response = ollama.chat(model='gemma4', messages=[
    {"role": "user", "content": "你好"}
])
print(response['message']['content'])
```

---

## GGUF 量化說明

GGUF 是本地模型的主流格式，量化等級影響**精度**與**速度**的取捨：

| 量化等級 | 精度損失 | 記憶體用量 | 速度 |
|---------|---------|----------|------|
| Q8_0    | 極小    | 最大     | 較慢  |
| Q6_K    | 很小    | 較大     | 中等  |
| Q5_K_M  | 小      | 中等     | 中等  |
| **Q4_K_M** | **建議** | **中等** | **快** |
| Q3_K_M  | 中等    | 較小     | 快   |
| Q2_K    | 明顯    | 最小     | 最快  |

**建議**：日常使用 Q4_K_M 取得最佳平衡

---

## 硬體需求計算

### 記憶體估算公式
```
所需 RAM ≈ 模型參數量（B）× 量化位元數 / 8 × 1.2（overhead）
```

| 模型 | 參數量 | Q4 所需 RAM |
|------|--------|------------|
| gemma3:1b | 1B | ~1 GB |
| gemma3:4b | 4B | ~3 GB |
| gemma4:12b | 12B | ~7 GB |
| qwen3:8b | 8B | ~5 GB |
| deepseek-r1:8b | 8B | ~5 GB |
| gemma4:27b | 27B | ~16 GB |

### 你的 Mac Mini 配置
- **現有模型**：gemma4（9.6 GB），nomic-embed-text（274 MB）
- **建議優先下載**：qwen3:8b（強推理）、gemma3:4b（快速回應）

---

## openclaw 已設定的模型清單

### 本地 Ollama 模型
| 模型 | 用途 |
|------|------|
| `gemma4:latest` | 主要對話模型 |
| `gemma4:e4b` | 輕量版 |
| `nomic-embed-text:latest` | 向量 Embedding |

### OpenRouter 雲端模型（free tier）
| 模型 ID | 說明 |
|---------|------|
| `openai/gpt-oss-120b:free` | 工具呼叫能力強 |
| `nvidia/nemotron-3-super-120b:free` | 大型推理模型 |
| `google/gemma-4-26b-a4b-it:free` | Google Gemma |
| `arcee-ai/trinity-large-preview:free` | 輕量快速 |

---

*建立時間：2026-04-19*
