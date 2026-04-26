# Speculative Decoding (LLM Inference Acceleration) 學習筆記
*來源檔案: topic-speculative-decoding.md*
*同步更新: 2026-04-26*

## 一句話理解
大型語言模型推理的瓶頸通常不在 FLOPs 不夠，而在 autoregressive decoding 的串行性。標準生成流程每產生一個 token，都必須再跑一次 target model，因此即使 GPU 還有剩餘算力，整體延遲仍被逐 token 的 memory movement 與 kernel launch 綁住。Speculative decoding 的設計動機，就是用一個更便宜的 draft path 預先猜出多個候選 token，再用較大的 target model 一次驗證多個位置，從而減少 target model 的完整前向次數。

## 必記重點
- Draft Model：用較小模型先猜多個 token
- Target Model：對 draft 候選做並行驗證與必要重採樣
- Verification Step：一次檢查多個候選 token，找出最長可接受前綴
- Medusa：在同一 backbone 上增加多個 decoding heads
- N-gram Speculation：直接利用上下文中的重複 token pattern 做猜測

## 核心名詞速記
- Draft Model：target model 每 token 都太貴
- Target Model：需要維持最終分布正確性
- Verification Step：草稿可能猜錯
- Medusa：維護獨立 draft model 太麻煩
- N-gram Speculation：沒有 draft 模型可用

## 流程速記
1. 使用 draft model 根據當前上下文一次提議 $k$ 個候選 token。
2. 將整段候選序列交給 target model 做一次前向傳播。
3. 逐位置比較 target model 與 draft model 對候選 token 的機率比，計算是否接受。
4. 若前綴全部通過，就一次提交這段前綴，並再向前推進多個 token。
5. 若在第 $j$ 個位置失敗，保留前 $j-1$ 個已接受 token。
6. 在失敗位置依 target-aware 修正分布重新採樣，避免最終分布被 draft bias 扭曲。
7. 重複以上步驟，直到達到停止條件。

## 必背公式
$$
\alpha_i = \min\left(1, \frac{p(d_i \mid x, d_{<i})}{q(d_i \mid x, d_{<i})}\right)
$$

$$
r(x) = \frac{\max(0, p(x) - q(x))}{\sum_y \max(0, p(y) - q(y))}
$$

## 實作範例重點
### 範例片段
```python
from __future__ import annotations


TARGET = {
    "": {"the": 0.60, "a": 0.25, "an": 0.15},
    "the": {"cat": 0.65, "dog": 0.20, "model": 0.15},
    "the cat": {"sat": 0.70, "slept": 0.20, "ran": 0.10},
}

DRAWFT = {
    "": ["the", "cat", "sat"],
    "the": ["cat", "sat"],
    "the cat": ["sat"],
}


def target_prob(context: str, token: str) -> float:
    return TARGET.get(context, {}).get(token, 0.0)


def draft_tokens(context: str, max_tokens: int) -> list[str]:
    return DRAWFT.get(context, [])[:max_tokens]


def speculative_step(context_tokens: list[str], max_draft_tokens: int = 3) -> tuple[list[str], str]:
    accepted = []
    context = " ".join(context_tokens)

    for token in draft_tokens(context, max_draft_tokens):
        current_context = " ".join(context_tokens + accepted)
        if target_prob(current_context, token) >= 0.5:
            accepted.append(token)
        else:
            break

    if accepted:
        context_tokens.extend(accepted)
        return context_tokens, f"accepted={accepted}"

    fallback = max(TARGET.get(context, {"<eos>": 1.0}), key=TARGET.get(context, {"<eos>": 1.0}).get)
    context_tokens.append(fallback)
    return context_tokens, f"fallback={fallback}"


def main() -> None:
    generated = []
    for _ in range(3):
        generated, note = speculative_step(generated)
        print(note, "->", generated)


if __name__ == "__main__":
    main()
```

### 驗證時要觀察什麼
- 第一輪應一次接受 `the`。
- 第二輪 draft 若仍命中高機率 token，會一次接受多個 token，而不是每輪只前進一個。
- 若 draft token 不符合 target 門檻，流程應回退到 fallback 採樣，而不是直接信任草稿。

## 自我檢查
- 練習 1：把範例中的 target 門檻從 `0.5` 改成更高或更低，觀察接受率如何變化。
- 練習 2：把 draft 序列故意改差，驗證 speculative decoding 何時開始失去效益。
- 練習 3：比較 standard decode、draft-target speculation、n-gram speculation 三種模式在不同輸出長度下的行為差異。