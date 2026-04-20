# Level 1：AI 入門基礎

## 學習目標
了解 AI / Machine Learning 的基本概念與術語，能夠理解 LLM 的運作方式。

---

## 核心概念

### 什麼是 AI / ML / Deep Learning？

- **AI（人工智慧）**：讓機器模擬人類智慧的廣義領域
- **Machine Learning（ML）**：從資料中學習規則，不需明確程式化
- **Deep Learning**：使用多層神經網路的 ML 子集，尤其擅長非結構化資料（圖像、文字）

### 什麼是 LLM（大型語言模型）？

- 以 Transformer 架構為基礎，在大量文字資料上訓練
- 透過「預測下一個 token」學習語言規律
- 代表模型：GPT 系列、Gemma、Llama、Qwen、DeepSeek

### 重要術語

| 術語 | 說明 |
|------|------|
| Token | LLM 處理的最小單位（約 0.75 個英文字） |
| Context Window | 模型一次能處理的最大 token 數 |
| Temperature | 控制輸出的隨機性（0=確定, 1=創意） |
| Inference | 用已訓練好的模型進行預測 |
| Fine-tuning | 在特定資料上繼續訓練模型 |
| Embedding | 將文字轉換為向量（數字陣列）以表達語意 |

---

## 參考資源（Desktop/ai/docs/ 內）

- `Beginners-Guide-to-Artificial-Intelligence.pdf`
- `Student-Guide-Module-1-Fundamentals-of-AI.pdf`
- `ED673750.pdf`

---

## 學習路徑建議

1. 閱讀上方 PDF 基礎概念
2. 在本機用 Ollama 跑 `gemma4` 模型，感受 LLM 互動
3. 嘗試修改 temperature 觀察輸出差異
4. 進入 Level 2：Prompt Engineering

---

*建立時間：2026-04-19*
