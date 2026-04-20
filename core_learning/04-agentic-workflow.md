# Agentic Workflow 設計指南

## 什麼是 Agentic Workflow？

Agentic Workflow 是一種由 AI 代理人（Agent）自主規劃、執行和監控的工作流程。不同於傳統的靈活流程，Agentic Workflow 允許代理人根據環境回饋動態調整步驟，實現真正的目標導向行為。

在 OpenClaw 中，Agentic Workflow 透過以下元素實現：
- **規劃（Planning）**：代理人根據目標將任務分解為子步驟
- **工具使用（Tool Use）**：代理人呼叫外部工具（搜尋、執行程式、讀寫檔案等）來收集資訊或執行動作
- **反思（Reflection）**：代理人檢查執行結果，判斷是否達成目標或需要調整
- **記憶（Memory）**：代理人保存中間結果和學到的知識，供後續步驟使用

## 四種核心設計模式

### 1. Sequential（順序執行）
每個步驟依序完成，前一步的輸出是下一步的輸入：
```
讀取文件 → 摘要 → 翻譯 → 儲存
```
**優點**：邏輯清晰，易於除錯  
**缺點**：效率低，無法並行

### 2. Parallel（平行執行）
多個任務同時執行，最後合併結果：
```
┌→ 搜尋 Wikipedia →┐
問題 →│→ 搜尋新聞 -------│→ 整合回答
      └→ 搜尋學術論文 →--┘
```
**優點**：執行時間短，能利用多核心  
**缺點**：需要結果合併策略，可能產生衝突

### 3. Conditional（條件分支）
根據條件執行不同路徑：
```
檢查天氣
├→ 晴天 → 建議戶外活動
└→ 雨天 → 建議室內活動
```
**優點**：能適應不同情況  
**缺點**：條件判斷需準確，否则可能走錯路徑

### 4. Iterative（迭代精煉）
重複執行直到達到品質標準或次數上限：
```
草稿 → 評估 → 修改 → （如果不滿意則重複）
```
**優點**：能持續改進输出质量  
**缺點**：需明確終止条件，否则可能无限循環

## 在 OpenClaw 中實作 Agentic Workflow

### 使用內建框架
OpenClaw 提供了多種方式來建立 Agentic Workflow：

#### 1. ReAct 框架（Reasoning + Acting）
這是最基礎且重要的框架。它結構化了 Agent 的輸出，讓模型必須在每次輸出的思考步驟 (Thought) 後，明確指定採取何種行動 (Action)，並等待觀察結果 (Observation)。
```
流程: Thought → Action → Observation → Thought → ... (直到達成目標)
```

**範例提示**：
```
思考（Thought）：我需要知道今天的天氣
行動（Action）：web_search("台北今天天氣")
觀察（Observation）：搜尋結果：27°C，晴天
思考（Thought）：已取得天氣資訊，可以回答用戶
回答（Final Answer）：台北今天 27°C，晴天
```

#### 2. Plan-and-Execute
Agent 首先從目標到可執行的子步驟，生成一個詳細的執行計畫（Plan）。然後，它會依序執行這些步驟，即使遇到失敗，也能在某一步驟進行回滾或調整計畫。

#### 3. TaskFlow（持久工作流）
適合需要跨多個子任務、維護狀態、可中斷後繼續的複雜自動化。TaskFlow 提供：
- 工作流身份，使其可被追蹤和管理
- 子任務鏈結與狀態等待
- 修改檢查（Revision-checked mutations）
- 人工介入點

## 安全考量

### 1. 安全邊界 (Safety)
必須定義 Agent 能使用的工具的權限範圍（如 `denyCommands`），防止 Agent 被惡意利用執行系統危險操作。

### 2. 資料洩漏防護
Agent 在使用工具時可能無意中洩漏敏感資訊。建議：
- 對工具回傳結果進行脫敏處理
- 限制 Agent 只能存取特定目錄
- 對外部請求（如 web_search）進行域名白名單過濾

### 3. 無限迴圈防護
對於 Iterative 工作流，必須設定明確的終止條件（例如：最大迭代次數、品質閾值）。

## 最佳實踐

1. **從簡單開始**：先實作 Sequential 工作流，再逐步加入 Parallel 或 Conditional 元素。
2. **明確定義目標**：Agent 需要一個清晰、可衡量的目標才能有效規劃。
3. **提供充足的上下文**：在規劃階段，給予 Agent 足夠的背景資訊，以減少錯誤假设。
4. **設計良好的觀察空間**：確保 Agent 能從工具回傳結果中獲得有用的資訊。
5. **加入人工監督點**：在關鍵決策點允許人類審核或介入。
6. **記錄與除錯**：記錄每個 Thought-Action-Observation 循環，便於事後分析和改進。

## 範例：建立研究助手 Agentic Workflow

**目標**：根據用戶提供的主題，撰寫一份簡短的研究報告。

**工作流**：
1. **規劃**：將主題分解為 3-5 個子問題
2. **平行搜尋**：同時搜尋每個子問題的相關資訊
3. **整合與摘要**：將搜尋結果整合成連貫的段落
4. **反思與修改**：檢查報告是否覆蓋所有要點，必要時重新搜尋不足的部分
5. **格式化**：加入標題、參考文獻等，輸出最終報告

**實作提示**（簡化版）：
```
目標：撰寫關於「再生能源最新進展」的研究報告

步驟一：規劃子問題
思考（Thought）：我需要了解太陽能、風能、儲能和政策四個方面的最新進展
行動（Action）：write_to_file("subtopics.txt", "太陽能最新進展\\n風能最新進展\\n儲能最新進展\\n再生能源政策最新進展")
觀察（Observation）：已建立 subtopics.txt

步驟二：平行搜尋（此處簡化為順序執行，實際可透過多個子協作者實現平行）
思考（Thought）：開始搜尋太陽能最新進展
行動（Action）：web_search("2024 太陽能技術 最新進展")
觀察（Observation）：[搜尋結果]
思考（Thought）：將結果存檔並移至下一個子問題
行動（Action）：append_to_file("solar_research.md", "[搜尋結果]")
...（重複 for 風能、儲能、政策）

步驟三：整合摘要
思考（Thought）：所有子研究已完成，現在整合成報告
行動（Action）：read_file("solar_research.md") + read_file("wind_research.md") + ...
思考（Thought）：基於這些資訊撰寫報告大綱
行動（Action）：write_to_file("report_outline.md", "# 再生能源最新進展報告\\n\\n## 摘要\\n## 太陽能\\n## 風能\\n## 儲能\\n## 政策\\n## 結論")
觀察（Observation）：大綱已建立

步驟四：反思與修改
思考（Thought）：檢查大綱是否缺少重要方面，例如成本效益分析
行動（Action）：web_search("再生能源 成本效益 分析 2024")
觀察（Observation）：[結果顯示缺少此部分]
思考（Thought）：需要在報告中加入成本效益章節
行動（Action）：edit_file("report_outline.md", "## 政策", "## 成本效益\\n## 政策")

步驟五：格式化輸出
思考（Thought）：根據大綱撰寫完整報告
行動（Action）：write_to_file("final_report.md", "[完整報告內容]")
觀察（Observation）：報告已完成
回答（Final Answer）：研究報告已生成，請查看 final_report.md
```

## 參考資源
- OpenClaw AGENTS.md：關於記憶與工作流的說明
- OpenClaw TOOLS.md：記錄您的 workflow 所需的本地資訊
- 各技能的 SKILL.md：如 `web_search`, `write`, `read`, `edit` 等的具體用法
-  ReAct 論文：https://arxiv.org/abs/2210.03629
- Plan-and-Execute 論文：https://arxiv.org/abs/2305.03628