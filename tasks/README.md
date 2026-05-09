# Tasks Directory

`tasks/` 是 agentic workflow 的狀態機資料區，不再放大型 prompt。

## Runtime State

- `backlog.json`：待派發任務總表。
- `active/`：正在處理或已研究完成、等待撰寫的任務卡。
- `context/`：Fact Sheet 與 review note。
- `completed/`：已撰寫完成、等待 Quality Validator 的任務卡。
- `archived/`：通過驗證的任務卡。
- `stale/`：狀態整理時保留下來的舊副本，不參與 workflow。

## Planning Specs

- `specs/`：舊 deep-task 規格與補強清單，作為 backlog 或人工規劃參考。

實際 workflow 入口是：

```bash
cd /Users/daniel.chang/Desktop/ai && /usr/bin/env python3 scripts/agentic_pipeline.py
```
