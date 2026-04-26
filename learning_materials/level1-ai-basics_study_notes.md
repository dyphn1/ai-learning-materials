# Level 1：AI 入門基礎 學習筆記
*來源檔案: level1-ai-basics.md*
*同步更新: 2026-04-26*

## 一句話理解
這份 Level 1 文件不是要用大眾科普方式重講「AI 是什麼」，而是要幫一位已有工程背景的讀者建立後續學習 AI 系統所需的最小正確心智模型。AI 是總稱，Machine Learning 是其中讓系統從資料而不是手寫規則中學習行為的方法，Deep Learning 則是用深層神經網路學習高維表示的主流路線。當今 LLM 的爆發，並不是因為語言突然變簡單，而是因為 Transformer 讓大規模並行訓練、長距離依賴建模與表示學習取得了新的平衡點。

## 必記重點
- AI：搜尋、規則、學習等方法總稱
- Machine Learning：最小化損失函數，從資料擬合參數
- Deep Learning：多層神經網路自動學表示
- Transformer：Self-Attention + MLP + positional encoding
- LLM：大規模 next-token pretraining

## 核心名詞速記
- AI：讓系統展現智慧行為
- Machine Learning：規則難以手寫時，從資料學習
- Deep Learning：特徵工程太昂貴
- Transformer：RNN/CNN 難以平行處理長序列
- LLM：通用語言理解與生成
- Embedding：需要把語意映成可計算空間

## 流程速記
1. 收集與清理語料，去重、過濾低品質內容。
2. 將文字 tokenization，轉成模型可處理的離散符號序列。
3. 以 next-token prediction 做預訓練，學會語言統計規律與表徵。
4. 視需求再做 instruction tuning、preference optimization 或 domain adaptation。
5. 在 inference 階段根據 prompt、解碼策略與系統限制生成輸出。

## 必背公式
$$
P(x) = \prod_{t=1}^{T} P(x_t \mid x_{<t})
$$

$$
\mathcal{L} = - \sum_{t=1}^{T} \log P(x_t \mid x_{<t})
$$

## 實作範例重點
### 範例片段
```python
from transformers import AutoTokenizer, pipeline


MODEL_NAME = "distilgpt2"


def main() -> None:
		tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
		generator = pipeline("text-generation", model=MODEL_NAME)

		prompt = "AI systems become useful when"
		tokens = tokenizer.encode(prompt)
		result = generator(prompt, max_new_tokens=20, do_sample=False)[0]["generated_text"]

		print(f"prompt: {prompt}")
		print(f"token_count: {len(tokens)}")
		print(f"generated: {result}")


if __name__ == "__main__":
		main()
```

### 驗證時要觀察什麼
- 第一次執行會下載模型權重，之後可離線重複測試。
- `token_count` 會顯示相同句子在模型中的 token 化結果並非等於字數。
- `generated` 會展示 next-token prediction 如何延續 prompt，而不是從零開始寫一段獨立文字。

## 自我檢查
- 練習 1：把 prompt 從一句話改成一段話，觀察 token 數量如何變化。
- 練習 2：把 `do_sample=False` 改成 `True`，觀察 deterministic 與 sampling 差異。
- 練習 3：查閱模型參數量與本機記憶體需求，理解為什麼部署策略是 AI 工程的一部分。