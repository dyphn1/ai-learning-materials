# AI 主題分類參考文件：大型語言模型基礎 (LLM Foundations)

## 📚 核心概念
*   **Transformer 架構:** 基於 Self-Attention 機制，徹底改變 NLP 領域。其 Encoder-Decoder 結構允許模型并行處理序列數據。
*   **Self-Attention 機制:** 這是 Transformer 的核心。它允許模型計算序列中每個詞彙與其他所有詞彙之間的「關聯度」（Attention Score），從而決定在生成下一個詞時，哪些前面的詞更重要。這使模型能夠捕捉長距離依賴關係。

## 🛠 實作要點
*   **位置編碼 (Positional Encoding):** 因為 Attention 本身不考慮詞彙的順序，所以需要加入 Positional Encoding 來告訴模型每個詞彙在序列中的位置。
*   **實務應用:** LLM 的大部分成功都源於其對 Transformer 結構的掌握和高效應用。
