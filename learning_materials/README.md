# AI 學習材料

此目錄包含從 `/Users/daniel.chang/Desktop/ai/docs/` 中的 Markdown 文件自動生成的學習材料。

## 目錄結構

- `AI_Glossary.md`：完整的 AI 術語表，包含所有文件中提取的核心術語。
- `*_study_notes.md`：每個原始 Markdown 文件對應的學習筆記，包含：
  - 核心概念（來自表格第一欄及 **粗體** 標記）
  - 實作範例（程式碼區塊摘錄）

## 檔案列表

| 學習筆記 | 對應原始檔案 |
|----------|--------------|
| level1-ai-basics_study_notes.md | level1-ai-basics.md |
| level2-prompt-engineering_study_notes.md | level2-prompt-engineering.md |
| level2-rag-basics_study_notes.md | level2-rag-basics.md |
| level3-agent-design_study_notes.md | level3-agent-design.md |
| topic-agentic-workflow_study_notes.md | topic-agentic-workflow.md |
| topic-agents_study_notes.md | topic-agents.md |
| topic-evaluation_study_notes.md | topic-evaluation.md |
| topic-llm-foundations_study_notes.md | topic-llm-foundations.md |
| topic-local-models_study_notes.md | topic-local-models.md |
| topic-multi-agent_study_notes.md | topic-multi-agent.md |
| topic-prompt-engineering_study_notes.md | topic-prompt-engineering.md |
| topic-rag_study_notes.md | topic-rag.md |

## 使用方式

1. 先閱讀 `AI_Glossary.md` 了解所有核心術語。
2. 依照興趣或學習順序閱讀對應的 `_study_notes.md` 文件。
3. 每個筆記中都包含實作範例，可直接參考或在本機環境中執行。

## 自動更新

這些材料是由腳本自動生成的。若原始文件有更新，可重新執行以下腳本來更新學習材料：

```bash
cd /Users/daniel.chang/Desktop/ai/scripts
python3 gen_learning_materials.py
```

亦可設定 cron 定時更新（參考 `/Users/daniel.chang/Desktop/ai/scripts/update_roadmap.sh` 的範例）。

---
*自動生成於: $(date)*