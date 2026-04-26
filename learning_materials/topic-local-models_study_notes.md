# 本地模型部署指南 學習筆記
*來源檔案: topic-local-models.md*
*同步更新: 2026-04-26*

## 一句話理解
*無法自動摘要，請回看主文的概覽與設計動機章節。*

## 必記重點
- Q8_0
- Q6_K
- Q5_K_M
- **Q4_K_M**
- Q3_K_M

## 核心名詞速記
- Q8_0
- Q6_K
- Q5_K_M
- **Q4_K_M**
- Q3_K_M
- Q2_K
- 精度
- 速度

## 必背公式
*本篇無核心公式*

## 實作範例重點
### 範例片段
```python
import ollama
response = ollama.chat(model='gemma4', messages=[
    {"role": "user", "content": "你好"}
])
print(response['message']['content'])
```

## 自我檢查
*無自我檢查題目*