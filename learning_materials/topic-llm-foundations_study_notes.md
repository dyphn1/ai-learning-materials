# 大型語言模型基礎 (LLM Foundations) 學習筆記
*來源檔案: topic-llm-foundations.md*
*同步更新: 2026-04-26*

## 一句話理解
大型語言模型（LLM）的崛起代表了自然語言處理領域的范式轉移。傳統統計語言模型基於 n-gram 和條件概率，而 LLM 則採用基於注意力機制的 Transformer 架構，實現了對語言結構的深度理解。LLM 的核心價值在於其**參數化知識表示**能力——將數十億個參數作為知識的載體，而非依賴外部資料庫的檢索。然而，這種設計也帶來了「知識凍結」問題：模型知識被固定在訓練時刻，無法動態更新。此外，傳統 RNN 架構的序列依賴性和長距離記憶問題，促使研究者開發了基於自注意力机制的全新架構。LLM 的設計動機正是要解決這些根本性限制，提供更具泛化性和推理能力的語言處理框架。

## 必記重點
- **Transformer**
- **RNN/LSTM**
- **CNN**
- **n-gram**
- 參數化知識表示

## 核心名詞速記
- **Transformer**
- **RNN/LSTM**
- **CNN**
- **n-gram**
- 參數化知識表示
- 直觀理解
- Transformer
- RNN/LSTM

## 必背公式
$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

$$
\begin{aligned}
\text{head}_i &= \text{Attention}(QW_i^Q, KW_i^K, VW_i^V) \\
\text{MultiHead}(Q, K, V) &= \text{Concat}(\text{head}_1, ..., \text{head}_h)W^O
\end{aligned}
$$

## 實作範例重點
### 範例片段
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

## 常見限制
- **長序列處理**：標準 Transformer 的二次方複雜度限制了處理超長文檔的能力
- **位置信息表達**：固定位置編碼難以處理變長序列和結構化數據
- **推理效率**：自注意力機制的高計算複雜度影響實時應用
- **知識更新**：參數化知識表示導致知識凍結問題
- **能源消耗**：大規模模型的計算和內存需求巨大

## 自我檢查
*無自我檢查題目*