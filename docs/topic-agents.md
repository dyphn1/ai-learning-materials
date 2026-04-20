# AI 主題分類參考文件：AI Agent 設計與框架

## 🤖 什麼是 Agent？
AI Agent 是一個能自主地接收目標、制定計畫、執行步驟、並根據結果反思來達成複雜任務的自給自足的系統。Agent 的核心是 **循環的思考-行動-觀察 (Observe-Think-Act)** 循環。

## 🔄 核心框架與流程
*   **ReAct (Reasoning and Acting):** 最基礎且重要的框架。它結構化了 Agent 的輸出，讓模型必須在每次輸出的思考步驟 (Thought) 後，明確指定採取何種行動 (Action)，並等待觀察結果 (Observation)。
    *   **流程:** Thought $\rightarrow$ Action $\rightarrow$ Observation $\rightarrow$ Thought $\rightarrow$ ... (直到達成目標)
*   **Plan-and-Execute:** Agent 首先從目標到可執行的子步驟，生成一個詳細的執行計畫（Plan）。然後，它會依序執行這些步驟，即使遇到失敗，也能在某一步驟進行回滾或調整計畫。
*   **Memory 系統:** Agent 的「記憶」分為短期 (Context Window) 和长期 (External Memory)。外部記憶 (如向量資料庫) 讓 Agent 可以在長時間的任務中記住過去的資訊。
*   **Tools/Functions Calling:** Agent 必須具備使用工具的能力 (Tool Use)。這讓模型從一個純粹的文本生成器，進化為一個可以與外部世界互動的控制器。

## 🏗️ 實作考量
1.  **安全邊界 (Safety):** 必須定義 Agent 能使用的工具的權限範圍 (如 `denyCommands`)，防止 Agent 被惡意利用執行系統危險操作。
2.  **狀態管理 (State Management):** 在複雜流程中，需要維護當前的任務狀態和已採取的行動歷史。
