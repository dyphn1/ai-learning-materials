# 大型語言模型基礎 (LLM Foundations)

> 最後更新：2026-04-24
> 相關論文：[Attention Is All You Need](https://arxiv.org/abs/1706.03762), [Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context](https://arxiv.org/abs/1901.02860)

## 概覽與設計動機
大型語言模型（LLM）的崛起代表了自然語言處理領域的范式轉移。傳統統計語言模型基於 n-gram 和條件概率，而 LLM 則採用基於注意力機制的 Transformer 架構，實現了對語言結構的深度理解。LLM 的核心價值在於其**參數化知識表示**能力——將數十億個參數作為知識的載體，而非依賴外部資料庫的檢索。然而，這種設計也帶來了「知識凍結」問題：模型知識被固定在訓練時刻，無法動態更新。此外，傳統 RNN 架構的序列依賴性和長距離記憶問題，促使研究者開發了基於自注意力机制的全新架構。LLM 的設計動機正是要解決這些根本性限制，提供更具泛化性和推理能力的語言處理框架。

## 核心機制深度解析

### Transformer 架構的革命性突破
Transformer 架構徹底改變了序列處理的范式，其核心在於拋棄了循環神經網絡的序列依賴，改採用自注意力機制實現並行化處理。

#### Encoder-Decoder 結構的設計哲學
```
輸入序列 → Encoder → 上下文向量 → Decoder → 輸出序列
```

Encoder 負責將輸入序列映射到連續的向量表示，而 Decoder 則基於這些表示生成輸出序列。這種分離設計允許模型同時處理輸入和輸出的語言結構，適合翻譯等需要語言間對齊的任務。

#### Self-Attention 機制的數學基礎
Self-Attention 是 Transformer 的核心，其數學形式為：

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

其中：
- $Q$ (Query)：查詢向量，代表當前位置需要關注的內容
- $K$ (Key)：鍵向量，用於計算與查詢的相關性
- $V$ (Value)：值向量，包含實際的語義信息
- $d_k$：鍵向量的維度，用於縮放點積避免梯度消失

**直觀理解**：每個詞彙通過 Query 與所有詞彙的 Key 計算相似度，得到注意力權重，然後加權求和 Value 向量。這使得模型能夠動態決定哪個詞對當前生成最重要。

#### Multi-Head Attention 的多維度建模
單一注意力頭只能捕捉一種類型的關係，Multi-Head Attention 通過並行多個注意力頭來捕捉不同維度的語言關係：

$$
\begin{aligned}
\text{head}_i &= \text{Attention}(QW_i^Q, KW_i^K, VW_i^V) \\
\text{MultiHead}(Q, K, V) &= \text{Concat}(\text{head}_1, ..., \text{head}_h)W^O
\end{aligned}
$$

其中 $W_i^Q, W_i^K, W_i^V$ 是各頭的投影矩陣，$W^O$ 是輸出投影矩陣。每個頭專注於不同類型的關係（如句法關係、語義關係、指代關係等）。

#### Positional Encoding 的位置信息注入
由於 Self-Attention 本身不考慮詞彙順序，必須加入位置信息。Transformer 使用正弦和余弦函數生成位置編碼：

$$
PE_{(pos,2i)} = \sin\left(\frac{pos}{10000^{2i/d_{model}}}\right)
$$
$$
PE_{(pos,2i+1)} = \cos\left(\frac{pos}{10000^{2i/d_{model}}}\right)
$$

這種編碼方式具有外推性，能夠處理訓練中未見過的長序列。

### Layer Normalization 與 Residual Connection 的穩定性設計

#### Layer Normalization 的作用機制
$$
\hat{x}_i = \gamma \cdot \frac{x_i - \mu_i}{\sqrt{\sigma_i^2 + \epsilon}} + \beta
$$

其中 $\mu_i$ 和 $\sigma_i^2$ 是第 $i$ 層的均值和方差，$\gamma$ 和 $\beta$ 是可學習的參數。Layer Normalization 穩定了訓練過程，使模型對學習率選擇不那麼敏感。

#### Residual Connection 的梯度流優化
$$
x_{l+1} = \text{LayerNorm}(x_l + \text{Sublayer}(x_l))
$$

殘差連接解決了深度網絡的梯度消失問題，允許訓練數百層的網絡。

## 與前代技術的比較

| 技術 | 優點 | 限制 | 適用場景 |
|------|------|------|----------|
| **Transformer** | 並行處理、長距離依賴捕捉、可擴展性 | 計算複雜度高 O(n²)、內存需求大 | 大規模語言建模、翻譯、摘要 |
| **RNN/LSTM** | 序列處理自然、內存效率高 | 長距離依賴問題、串行處理慢 | 時序序列、實時處理 |
| **CNN** | 局部特徵捕捉、計算效率高 | 長距離依賴困難、固定感受野 | 文本分類、簡單序列任務 |
| **n-gram** | 簡單直觀、訓練快速 | 維度災難、長距離依賴缺失 | 語言建模、拼寫檢查 |

## 工程實作

### 環境設定
```bash
# PyTorch Transformer 實作環境
pip install torch transformers numpy matplotlib
pip install --upgrade transformers  # 確保使用最新版本
```

### 核心實作（完整可執行）
```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math
import numpy as np

class PositionalEncoding(nn.Module):
    """實作 Transformer 的位置編碼"""
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * 
                           (-math.log(10000.0) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        self.register_buffer('pe', pe)
    
    def forward(self, x):
        return x + self.pe[:x.size(0), :]

class MultiHeadAttention(nn.Module):
    """實作 Multi-Head Attention"""
    def __init__(self, d_model, num_heads):
        super().__init__()
        assert d_model % num_heads == 0
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
        
        self.dropout = nn.Dropout(0.1)
        
    def scaled_dot_product_attention(self, Q, K, V, mask=None):
        """縮放點積注意力"""
        attn_scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        
        if mask is not None:
            attn_scores = attn_scores.masked_fill(mask == 0, -1e9)
        
        attn_weights = F.softmax(attn_scores, dim=-1)
        attn_weights = self.dropout(attn_weights)
        
        output = torch.matmul(attn_weights, V)
        return output, attn_weights
    
    def forward(self, Q, K, V, mask=None):
        batch_size = Q.size(0)
        
        # 線性變換並分割到多個頭
        Q = self.W_q(Q).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(K).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(V).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        
        # 計算注意力
        attn_output, attn_weights = self.scaled_dot_product_attention(Q, K, V, mask)
        
        # 合併多個頭
        attn_output = attn_output.transpose(1, 2).contiguous().view(
            batch_size, -1, self.d_model)
        
        # 最終線性變換
        output = self.W_o(attn_output)
        return output, attn_weights

class TransformerEncoderLayer(nn.Module):
    """Transformer Encoder Layer"""
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super().__init__()
        self.self_attn = MultiHeadAttention(d_model, num_heads)
        self.feed_forward = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model)
        )
        
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x, mask=None):
        # Self-Attention + Residual
        attn_output, _ = self.self_attn(x, x, x, mask)
        x = self.norm1(x + self.dropout(attn_output))
        
        # Feed Forward + Residual
        ff_output = self.feed_forward(x)
        x = self.norm2(x + self.dropout(ff_output))
        
        return x

class SimpleTransformer(nn.Module):
    """簡化的 Transformer 模型"""
    def __init__(self, vocab_size, d_model, num_heads, num_layers, d_ff, max_len=5000):
        super().__init__()
        self.d_model = d_model
        
        # 詞嵌入和位置編碼
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoding = PositionalEncoding(d_model, max_len)
        
        # Encoder Layers
        self.layers = nn.ModuleList([
            TransformerEncoderLayer(d_model, num_heads, d_ff)
            for _ in range(num_layers)
        ])
        
        # 輸出層
        self.fc_out = nn.Linear(d_model, vocab_size)
        
        # 初始化參數
        self._init_weights()
        
    def _init_weights(self):
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)
                
    def forward(self, x, mask=None):
        # 詞嵌入 + 位置編碼
        x = self.embedding(x) * math.sqrt(self.d_model)
        x = self.pos_encoding(x)
        
        # 經過 Encoder Layers
        for layer in self.layers:
            x = layer(x, mask)
        
        # 輸出預測
        logits = self.fc_out(x)
        return logits

# 使用範例
def main():
    # 超參數
    vocab_size = 10000
    d_model = 512
    num_heads = 8
    num_layers = 6
    d_ff = 2048
    batch_size = 32
    seq_len = 100
    
    # 創建模型
    model = SimpleTransformer(vocab_size, d_model, num_heads, num_layers, d_ff)
    
    # 生成隨機輸入
    input_tokens = torch.randint(0, vocab_size, (batch_size, seq_len))
    
    # 前向傳播
    logits = model(input_tokens)
    
    print(f"Input shape: {input_tokens.shape}")
    print(f"Output shape: {logits.shape}")
    print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    # 演示注意力機制
    attn_layer = MultiHeadAttention(d_model, num_heads)
    query = key = value = torch.randn(batch_size, seq_len, d_model)
    attn_output, attn_weights = attn_layer(query, key, value)
    
    print(f"Attention weights shape: {attn_weights.shape}")
    print(f"Attention weights for first token: {attn_weights[0, 0, :5]}")

if __name__ == "__main__":
    main()
```

### 工程落地注意事項
- **Latency**：標準注意力機制的複雜度為 O(n²)，對長序列（>512）需要優化
- **成本**：大規模模型訓練需要分布式訓練和模型並行化策略
- **穩定性**：梯度消失/爆炸問題需要梯度裁剪和適當的初始化
- **Scaling**：隨著模型增大，需要考慮查詢/鍵/值的量化技術

## 2025-2026 最新進展

### Flash Attention 3.0 的計算優化
Flash Attention 3.0 通過 IO 感知算法和內存重用，將注意力計算的複雜度從 O(n²) 降低到 O(n log n)，在保持精度的同時大幅提升速度。

### State Space Models (SSM) 的融合
Mamba、Hybrid State Space Models 結合了 RNN 的序列建模能力和 Transformer 的並行化優勢，在長序列處理上展現出潛力。

### Ring Attention 的分布式實現
為解決長序列的內存問題，Ring Attention 將注意力計算分佈到多個設備上，實現線性內存複雜度。

### MoE (Mixture of Experts) 的規模化應用
像 Mixtral 8x7B 這樣的 MoE 模型在保持推理成本可控的同時，擴展了模型容量，提升了處理複雜任務的能力。

## 已知限制與 Open Problems

- **長序列處理**：標準 Transformer 的二次方複雜度限制了處理超長文檔的能力
- **位置信息表達**：固定位置編碼難以處理變長序列和結構化數據
- **推理效率**：自注意力機制的高計算複雜度影響實時應用
- **知識更新**：參數化知識表示導致知識凍結問題
- **能源消耗**：大規模模型的計算和內存需求巨大

## 延伸閱讀
- [Transformer 原始論文](https://arxiv.org/abs/1706.03762)
- [Attention Is All You Need 實作詳解](https://github.com/harvard-edge/cs286r_spring2020/tree/master/transformer)
- [PyTorch 官方 Transformer 教程](https://pytorch.org/tutorials/beginner/transformer_tutorial.html)
- [HuggingFace Transformers 文檔](https://huggingface.co/docs/transformers/index)

---
*此文件由 AI agent 自動生成並持續更新*

## 更新記錄
- 2026-04-24：全新撰寫，包含完整的 Transformer 架構解析、數學公式、可執行程式碼範例；加入 2025-2026 年最新進展與工程實作指南