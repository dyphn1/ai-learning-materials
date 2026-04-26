# Level 2：RAG 入門指南 學習筆記
*來源檔案: level2-rag-basics.md*
*同步更新: 2026-04-26*

## 一句話理解
*無法自動摘要，請回看主文的概覽與設計動機章節。*

## 必記重點
- 固定大小
- 句子切分
- 語意切分
- 重疊切分
- 問題

## 核心名詞速記
- 固定大小
- 句子切分
- 語意切分
- 重疊切分
- 問題
- 解法
- 建議起點
- LangChain

## 必背公式
*本篇無核心公式*

## 實作範例重點
### 範例片段
```python
# 使用 nomic-embed-text（已安裝）
import ollama
response = ollama.embeddings(model='nomic-embed-text', prompt='你好')
vector = response['embedding']  # 長度 768 的浮點陣列
```

## 自我檢查
*無自我檢查題目*