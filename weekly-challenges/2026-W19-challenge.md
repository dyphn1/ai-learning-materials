# 每週進階挑戰 - 第 19 週 (2026)

*週期: 2026-05-04 ~ 2026-05-10*  
*主題: Agentic Pipeline 診斷與修復*

## 挑戰: 分析並修復 Agentic Pipeline 失敗

本週 agentic pipeline 出現系統性失敗（logs/pipeline.log 中可見連續 28 次 ERROR）。  
你的任務是進行根本原因分析，並產出一份完整的診斷報告。

### 背景

檢查 `logs/pipeline.log`，你會看到從 2026-05-10 到 2026-05-12 的每次執行都失敗了。  
失敗有三種模式：
1. 每次都呼叫 `quality-validator` 但沒有 completed 任務可驗證
2. `pipeline lock exists` 錯誤
3. `Orchestrator finished but no active task card exists`

### 實作要求

1. **診斷階段**：解析 `logs/pipeline.log` 的最近 28 次失敗，找出根本原因
2. **報告**：撰寫 `docs/pipeline-diagnosis-W19.md`，包含：
   - 失敗摘要（失敗次數、失敗模式分類）
   - 根本原因分析（至少 3 個）
   - 修復方案（具體到程式碼層面）
   - 預防措施（如何避免下次發生）
3. **修復**：在 `scripts/agentic_pipeline.py` 中實作修復
4. **驗證**：執行 `python3 scripts/agentic_pipeline.py --normalize-only` 確認 pipeline 可以啟動

### 驗收標準

- [ ] `docs/pipeline-diagnosis-W19.md` 存在且有結構化內容
- [ ] 根本原因章節列出至少 3 個原因
- [ ] `scripts/agentic_pipeline.py` 語法正確（`python3 -m py_compile` 通過）
- [ ] `logs/pipeline.log` 中沒有殘留的 pipeline lock 錯誤（重置後）

### 參考

實際修復已於 2026-05-13 完成，見 `tasks/20260513T000000+0800_pipeline-fix.md`。  
本題作為學習回顧：獨立分析並重新推導修復方案。
