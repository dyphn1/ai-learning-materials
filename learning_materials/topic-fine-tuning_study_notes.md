# Fine-tuning 與 Post-Training (LLM Adaptation) 學習筆記
*來源檔案: topic-fine-tuning.md*
*同步更新: 2026-04-26*

## 一句話理解
預訓練模型已經學到廣泛的語言分布，但這不代表它可以直接滿足特定產品、特定領域或特定行為邊界。Fine-tuning 與 post-training 的設計動機，就是把「會說話的基礎模型」轉成「在特定目標上可控、可部署、可維護的模型」。當任務需要領域語彙、企業內部格式、工具協作習慣、偏好對齊或安全風格時，只靠 prompt 往往不夠穩定，因為每次請求都要重複提供規則，且模型的內部表示並沒有真正被更新。

## 必記重點
- Full Fine-tuning：更新所有可訓練權重
- LoRA：將權重更新表示成低秩矩陣分解 $BA$
- QLoRA：在 4-bit quantized backbone 上訓練 LoRA adapters
- PEFT：抽象 LoRA、IA3、Prefix Tuning 等方法的配置與載入
- SFT：用 supervised pairs 直接最小化 language modeling loss

## 核心名詞速記
- Full Fine-tuning：需要全面改寫模型行為
- LoRA：full FT 太貴
- QLoRA：LoRA 仍受限於 GPU 記憶體
- PEFT：需要統一管理多種參數高效方法
- SFT：先讓模型學會目標格式與任務風格
- DPO：RLHF pipeline 太重

## 流程速記
1. 定義 adaptation 目標，是 domain adaptation、instruction following、preference alignment 還是 safety tuning。
2. 決定資料型態，是 supervised pairs、ranked preference pairs，或混合資料。
3. 選擇參數更新策略：full FT、LoRA、QLoRA 或其他 PEFT 方法。
4. 準備 tokenizer、padding、packing 與訓練資料格式，避免資料管線先破壞目標行為。
5. 以訓練損失或 preference objective 進行更新，並記錄 trainable params、顯存與吞吐。
6. 用 task metrics、judge model、人類評測或 regression set 檢查收益與副作用。
7. 決定部署方式：merge adapter、動態載入 adapter，或保留對齊階段與基礎模型分離。

## 必背公式
$$
W' = W + \Delta W, \quad \Delta W = \frac{\alpha}{r} BA
$$

$$
\mathcal{L}_{DPO} = - \mathbb{E}\left[\log \sigma\left(\beta \log \frac{\pi_\theta(y_w \mid x)}{\pi_{ref}(y_w \mid x)} - \beta \log \frac{\pi_\theta(y_l \mid x)}{\pi_{ref}(y_l \mid x)}\right)\right]
$$

## 實作範例重點
### 範例片段
```python
from datasets import Dataset
from peft import LoraConfig, TaskType, get_peft_model
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)


MODEL_NAME = "sshleifer/tiny-gpt2"


def build_dataset(tokenizer):
    rows = {
        "text": [
            "### Instruction: Summarize adapter tuning. ### Response: Adapters reduce trainable parameters.",
            "### Instruction: Explain QLoRA. ### Response: QLoRA trains LoRA adapters on a 4-bit frozen backbone.",
            "### Instruction: What does DPO optimize? ### Response: DPO directly optimizes preference pairs without PPO.",
        ]
    }
    dataset = Dataset.from_dict(rows)

    def tokenize(batch):
        return tokenizer(batch["text"], truncation=True, padding="max_length", max_length=96)

    return dataset.map(tokenize, batched=True, remove_columns=["text"])


def print_trainable_ratio(model):
    trainable = sum(param.numel() for param in model.parameters() if param.requires_grad)
    total = sum(param.numel() for param in model.parameters())
    print(f"trainable_params={trainable}")
    print(f"total_params={total}")
    print(f"ratio={trainable / total:.4%}")


def main():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=8,
        lora_alpha=16,
        lora_dropout=0.05,
        target_modules=["c_attn"],
    )
    model = get_peft_model(model, lora_config)
    print_trainable_ratio(model)

    tokenized_dataset = build_dataset(tokenizer)
    collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
    args = TrainingArguments(
        output_dir="./tmp-ft-output",
        per_device_train_batch_size=2,
        num_train_epochs=1,
        logging_steps=1,
        save_strategy="no",
        report_to=[],
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized_dataset,
        data_collator=collator,
    )
    trainer.train()

    prompt = "### Instruction: Explain LoRA in one sentence. ### Response:"
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(**inputs, max_new_tokens=24)
    print(tokenizer.decode(output[0], skip_special_tokens=True))


if __name__ == "__main__":
    main()
```

### 驗證時要觀察什麼
- `trainable_params` 應遠小於 `total_params`，證明只更新 adapter 而非全模型。
- 訓練能在極小模型上完成 1 個 epoch，驗證資料管線、LoRA 注入與生成流程都可運作。
- 若 `target_modules` 不匹配模型結構，最常見錯誤會出現在 adapter 注入階段。

## 自我檢查
- 練習 1：把 LoRA 的 `r` 從 `8` 改成 `4` 與 `16`，觀察 trainable params 與輸出差異。
- 練習 2：改用不同的小模型測試 `target_modules`，理解 adapter 注入與模型結構的耦合。
- 練習 3：比較 prompt-only、LoRA SFT、DPO 三種路線分別解決的是哪一層問題。