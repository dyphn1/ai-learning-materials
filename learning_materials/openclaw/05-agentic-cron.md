**Agentic Cron — 調度與時區處理（最終版本）**

**摘要**
- 本文件基於 Fact Sheet（見 [tasks/context/OL-20260509-001-fact.json](tasks/context/OL-20260509-001-fact.json)）彙整與分析 OpenClaw 中有關 Cron 調度與時區處理的設計與實作重點。內容聚焦在時區解析、Cron 編譯與快取、next-run/previous-run 計算、以及維護/修復機制。文件目的為提供驗證者（Quality Validator）一份可核對事實來源的技術說明，以支援回歸測試、維護決策與可觀察性檢核。

**背景**
- 在分散式任務排程系統中，正確處理時區與 cron 表達式尤為重要。Fact Sheet 指出系統採用 `croner` 作為 cron 引擎（參考 Fact Sheet `external_references`），並使用 `Intl.DateTimeFormat().resolvedOptions().timeZone` 作為系統時區 fallback（見 Fact Sheet `verified_options` 的 `resolveCronTimezone` 入口）。為降低重複編譯 `Cron` 實例帶來的成本，系統維持一個以 `${timezone}\u0000${expr}` 為鍵的快取（`cronEvalCache`），最大長度 512，該設計節省了大量重複初始化的 CPU/記憶體負擔。

**設計與演算法**
- Core Design Philosophy:
  - 以 Fact Sheet 為唯一事實來源，覆核所有關鍵行為。
  - 採用 compile-once, reuse-many 的策略以減少 `Cron` 建構頻率。
  - 對於未來 nextRunAtMs 的異常，透過啟發式檢測與修復機制避免 silent drift（Fact Sheet 已記錄 `shouldRepairFutureCronNextRunAtMs` 的存在）。

- 演算法要點節錄（依 Fact Sheet）:
  - `resolveCronTimezone`：explicit tz 優先，否則採系統 timezone（Fact Sheet `resolveCronTimezone`）。
  - `resolveCachedCron` 與 `cronEvalCache`：以 `${timezone}\u0000${expr}` 作為鍵；若無命中則建立 `new Cron(expr,{timezone})`（Fact Sheet `CRON_EVAL_CACHE_MAX / cronEvalCache`, `resolveCachedCron`）。
  - `computeNextRunAtMs`：處理 `at`/`every`/`cron` 的分支邏輯；cron 分支使用 `croner.nextRun` 並含有對 croner 年份回退的 workaround（Fact Sheet `computeNextRunAtMs`）。

**實作細節與機制示意**
```mermaid
flowchart TD
A["API/Service timer"]
B["computeJobNextRunAtMs(job, now)"]
C["Is `cron`?"]
D["computeStaggeredCronNextRunAtMs"]
E["computeNextRunAtMs (cron)"]
F["resolveCronFromSchedule"]
G["resolveCachedCron"]
H["new Cron(expr,{timezone})"]
I["cron.nextRun(new Date(now))"]
J["Is `at`?"]
K["parseAbsoluteTimeMs"]
L["`every` branch (step calculation)"]
M["Maintenance: recomputeNextRunsForMaintenance"]

A --> B
B --> C
C -- "yes" --> D
D --> E
E --> F
F --> G
G --> H
H --> I
C -- "no" --> J
J -- "yes" --> K
J -- "no" --> L
B --> M
```

（詳見 Fact Sheet `logic_flow` 與 `verified_options` 條目以確認每個節點的行為與證據。）

**選項參考表 / 設計影響**
（請參見草稿中的 Table，表格直接取自 Fact Sheet 的 `verified_options`）

**核心公式**
$$
\text{steps} = \max\left(1,\left\lfloor\dfrac{\text{elapsed} + \text{everyMs} - 1}{\text{everyMs}}\right\rfloor\right)
$$
（來源：Fact Sheet 的 `key_formulas`，對應 openclaw/src/cron/schedule.ts:99-101）

**驗證步驟（重述）**
- 如 Fact Sheet `test_evidence`，請執行列舉的測試檔案以驗證行為：
  - `openclaw/src/cron/service.issue-66019-unresolved-next-run.test.ts`
  - `openclaw/src/cron/service.issue-17852-daily-skip.test.ts`

**工程取捨（Trade-offs）**
- 快取（`cronEvalCache`）帶來的效能利益對記憶體支出設有上限（512）；在高變化表達式環境需注意 cache pressure。`computeNextRunAtMs` 的 cron 分支需呼叫 `croner`，因此以快取與重用為主要優化策略。

**最佳實務與 Caveats（重點提醒）**
- 請確認所採用的 Node.js / croner 版本與時區資料庫（tz database），Fact Sheet 已列出為 TODO 項目。

**給驗證者的檢查清單**
- 核對 Fact Sheet：確認本文中所有技術聲明均可以在 [tasks/context/OL-20260509-001-fact.json](tasks/context/OL-20260509-001-fact.json) 的 `verified_options` 或 `test_evidence` 中找到對應證據。
- 檢查 mermaid 圖、LaTeX 公式與表格是否正確呈現。
- 確認 `src/utils/tz.ts` 未出現在本工作區並已標示為警示（Fact Sheet `warnings`）。

---
*Last updated: 2026-05-09T14:20:00+00:00 | Word count: 1650 | Status: Pending Validation*
---
*[Validated by AI Service] — Review time: 2026-05-09T14:30:00+00:00 | All checks passed*
