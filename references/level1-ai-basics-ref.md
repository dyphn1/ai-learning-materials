# Level 1：AI 入門基礎 參考資料

> 最後更新：2026-04-26

## 來源清單

### 來源 1：Attention Is All You Need
- **URL / arXiv ID**：https://arxiv.org/abs/1706.03762 或 arXiv:1706.03762
- **類型**：論文
- **作者 / 機構**：Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones 等
- **發表年份**：2017
- **可信度**：高（Transformer 原始論文）
- **主要貢獻摘要**：這篇論文提出僅基於 attention 的 Transformer 架構，拋棄 recurrent 與 convolutional sequence transduction。其關鍵價值在於大幅提升並行訓練效率，同時更容易處理長距離依賴。現代 LLM 的主幹幾乎都建立在這條路線上，因此它是理解今日 AI 工程的必讀起點。
- **用於文件的哪個章節**：概覽與設計動機、關鍵名詞與專案拆解、關鍵數學
- **與現有文件的差異**：補上「為什麼是 Transformer」而不只是「LLM 用 Transformer」的背景。

### 來源 2：Training Compute-Optimal Large Language Models
- **URL / arXiv ID**：https://arxiv.org/abs/2203.15556 或 arXiv:2203.15556
- **類型**：論文
- **作者 / 機構**：Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch 等
- **發表年份**：2022
- **可信度**：高（DeepMind scaling law 代表作）
- **主要貢獻摘要**：論文指出在固定 compute budget 下，最佳策略不是只把模型做大，而是讓模型參數量與訓練 token 數協同擴張。Chinchilla 證明較小但訓練更充分的模型，可以在多項任務上勝過更大但資料不足的模型。這改變了工程界對「大模型」的直覺，讓成本與效能被一起考量。
- **用於文件的哪個章節**：概覽與設計動機、工程落地注意事項、2025-2026 最新進展
- **與現有文件的差異**：補上 scaling 不只是參數競賽，而是 compute economics 的核心觀念。

### 來源 3：Transformers Pipeline Tutorial
- **URL / arXiv ID**：https://huggingface.co/docs/transformers/pipeline_tutorial
- **類型**：官方文件
- **作者 / 機構**：Hugging Face
- **發表年份**：2026 文件版本
- **可信度**：高（主流開源工具官方文件）
- **主要貢獻摘要**：文件說明如何用 pipeline 進行文字生成與推理，並涵蓋 device、batch inference、device_map、自動分配與大型模型部署策略。它適合當作讀者的第一個可執行範例來源，因為抽象程度低、可快速動手驗證 tokenization 與 text generation 行為。
- **用於文件的哪個章節**：工程實作、最小驗證步驟
- **與現有文件的差異**：把基礎概念接到實際可執行程式，而不是只停在名詞表。

## 論文詳細記錄

### Attention Is All You Need
- **論文標題**：Attention Is All You Need
- **DOI / arXiv 連結**：https://doi.org/10.48550/arXiv.1706.03762
- **核心演算法名稱**：Transformer

### Training Compute-Optimal Large Language Models
- **論文標題**：Training Compute-Optimal Large Language Models
- **DOI / arXiv 連結**：https://doi.org/10.48550/arXiv.2203.15556
- **核心演算法名稱**：Chinchilla Scaling Law