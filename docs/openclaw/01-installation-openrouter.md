# OpenRouter 安裝與設定指南

## 什麼是 OpenRouter？

OpenRouter 是一個統一的介面，可以訪問多種大型語言模型（LLM），包括開源和商業模型。透過 OpenRouter，您可以使用單一 API 金鑰存取 GPT-4、Claude、Gemini 等多種模型。

## 安裝步驟

### 1. 註冊 OpenRouter 帳號
- 前往 https://openrouter.ai 註冊帳號
- 確認電子郵件並登入

### 2. 取得 API 金鑰
- 登入後前往「API Keys」頁面
- 點擊「Create Key」建立新的 API 金鑰
- 複製並安全地儲存此金鑰（僅會顯示一次）

### 3. 在 OpenClaw 中設定 OpenRouter
OpenClaw 內建支援 OpenRouter 作為模型提供者。

#### 透過環境變數設定（推薦）
在您的 shell 配置檔案（如 `~/.zshrc` 或 `~/.bashrc`）中加入：
```bash
export OPENROUTER_API_KEY="your_api_key_here"
```
然後重新載入配置：
```bash
source ~/.zshrc
```

#### 透過 OpenClaw 配置檔案
編輯 `~/.openclaw/config.yaml`（如果不存在則創建）：
```yaml
models:
  default:
    provider: openrouter
    model: openrouter/auto  # 會自動選擇最適合的模型
  openrouter:
    api_key: ${OPENROUTER_API_KEY}  # 從環境變數讀取
```

### 4. 驗證設定
在終端機中執行：
```bash
openclaw model list
```
您應該能看到可用的模型列表。

## 常用模型推薦

| 模型名稱 | 提供者 | 特色 | 適合場景 |
|----------|--------|------|----------|
| `openrouter/auto` | OpenRouter | 自動選擇 | 日常使用 |
| `openrouter/gpt-4` | OpenAI | 最強通用模型 | 複雜推理、程式碼生成 |
| `openrouter/claude-3-opus` | Anthropic | 長文本理解 | 文件分析、寫作 |
| `openrouter/gemini-pro` | Google | 多模態能力 | 圖片理解、多語言 |
| `openrouter/nvidia/nemotron-3-super` | NVIDIA | 高效推理 | 本地化部署替代方案 |

## 進階設定

### 模型參數調整
在 OpenClaw 中，您可以透過以下方式調整模型參數：
```bash
openclaw chat --temperature 0.7 --max_tokens 2000
```

### 使用特定模型
指定使用特定模型：
```bash
openclaw chat --model openrouter/gpt-4
```

### 成本監控
OpenRouter 提供使用量儀表板，您可以在網站上查看每個模型的使用成本。

## 常見問題

**Q: 如何查看我的使用量和成本？**
A: 登入 OpenRouter 網站，前往「Usage」頁面。

**Q: 遇到速率限制該怎麼辦？**
A: 您可以：
1. 升級您的 OpenRouter 方案以獲得更高的速率限制
2. 在請求間添加延遲
3. 使用較小的模型進行測試

**Q: 如何在 OpenClaw 中切換模型提供者？**
A: 修改 `config.yaml` 中的 `provider` 欄位，或使用 `--provider` 參數覆寫。

## 參考資源
- OpenRouter 文檔：https://openrouter.ai/docs
- OpenClaw 模型配置指南：參考 OpenClaw 官方文件
- API 參考：https://openrouter.ai/api