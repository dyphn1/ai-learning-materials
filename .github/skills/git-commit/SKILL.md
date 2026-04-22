---
name: git-commit
description: 'Automatically generate and apply Conventional Commits (Angular style) for all staged changes across the current repository and its submodules. Use when committing changes in a repository with submodules.'
---

# Create Commit Messages for All Repositories

Analyze all **staged changes** within the **current repository** and all **submodules**, then generate and apply **Conventional Commit** messages (Angular style) automatically — committing each repository individually.

---

## Critical Rule

**ALL submodules MUST be fully processed before the main repository is handled.**
The main repository commit is the **final aggregation step** and must never occur while any submodule remains unprocessed.

---

## 🔒 Normative Definition: What Counts as "Staged Changes"

A repository (main or submodule) **MUST be considered to have staged changes** if **ANY** of the following conditions are true:

1. `git diff --cached` produces output
2. `git diff --cached --name-status` shows any index state:
   - `A`, `M`, `D`, `R`, `C`
3. The repository is a submodule and:
   - Its HEAD commit differs from the index commit recorded by the parent repository
4. The parent repository shows a submodule gitlink change (even if the submodule working tree is clean)

❌ It is **STRICTLY FORBIDDEN** to conclude "no staged changes" based on a single command or partial evidence.

### 📌 Monotonic Evidence Rule (Non-Revocable)

**Chain of Custody**: The agent must maintain a "**State Log**" in its thought process. Once a diff is detected in any repository, the agent must write: [LOG: `<repo_name>` HAS STAGED CHANGES]. This log entry acts as a permanent flag that cannot be overwritten by subsequent "no changes found" observations.

Once **ANY** evidence of staged changes is observed at any point
(e.g. non-empty `git diff --cached`, detected gitlink change,
or observed index state),

❗ The repository MUST be permanently classified as
"has staged changes" for the remainder of the run.

It is **STRICTLY FORBIDDEN** to later downgrade or negate this
classification based on subsequent checks, heuristics,
or conflicting signals.

---

## Strict Processing Order (Mandatory)

1. **Enumerate all submodules recursively (leaf-first)**
2. **Process every submodule**
3. **Verify all submodules are completed**
4. **Process the main repository last**

This rule overrides all implicit or default agent behavior.

---

## Enforced Workflow

### Step 1: Discover Submodules
- Recursively list all submodules
- Build a complete processing list **before committing anything**

---

### Step 2: Submodule Processing Phase (Blocking)

For **each submodule**:

1. Run:
   ```bash
   git -C <submodule_path> diff --cached --name-status
   ```
   ```bash
   git --no-pager -C <submodule_path> diff --cached
   ```
   ```bash
   git -C <submodule_path> rev-parse HEAD
   ```
2. Evaluate staged changes and immediately lock the result:
   - If any staged evidence is observed, record the submodule state as: `STAGED_CHANGES_CONFIRMED`
   - This state MUST NOT be reverted later in the run.
3. If staged changes exist:
   - Analyze staged changes only
   - Generate a Conventional Commit (Angular style)
   - Execute exactly **one commit**
   - Keep track that a submodule commit was made.
4. Mark the submodule as **processed**, even if no commit was made.
5. Continue until **all submodules are visited**

⚠️ The main repository MUST NOT be processed during this phase.

#### Hard Constraint

The agent MUST NOT output "**No staged changes to commit.**" unless it can explicitly confirm:
- All submodules were visited
- For each submodule, `git diff --cached --name-status` and `git diff --cached` were inspected
- The main repository index contains no gitlink changes

---

### Step 3: Verification Gate (Required)

Before touching the main repository, verify:
- All submodules have been visited
- No submodule still has staged changes

If verification fails:
- Abort main repository processing and return to Step 2

---

### Step 4: Submodule Confirmation Pause (Mandatory)

If ANY submodule was committed during Step 2:
1. The agent **MUST pause execution** and ask the user:
   > "Some submodules were committed. Do you want to stage these submodule updates in the main repository and proceed with the main repository commit?"
2. **Wait for the user's confirmation.**
3. If the user answers **Yes**:
   - Stage the committed submodules in the main repository (e.g., `git add <submodule_path>`).
   - Proceed to Step 5.
4. If the user answers **No**:
   - Skip adding the submodules and proceed to Step 5.

---

### Step 5: Main Repository (Final Phase)

Only after all submodules are complete and the confirmation pause is handled:

1. The presence of a submodule pointer update in the index MUST be treated as a staged change, even if no file diff exists.
2. Analyze:
   ```bash
   git diff --cached --name-status
   ```
   ```bash
   git --no-pager diff --cached
   ```
3. Detect submodule pointer updates:
   ```
   Subproject commit <old_hash>...<new_hash>
   ```
4. Collect submodule logs:
   ```bash
   git --no-pager -C <submodule_path> log --oneline <old_hash>..<new_hash>
   ```
5. Generate the final Conventional Commit
6. Commit exactly once

---

## 🧠 Processing Logic

For **each** repository (main and submodules) with staged changes:

1.  **Skip** if no staged changes are found.
2.  **Analyze** the diff (and submodule logs if applicable) to determine:
    -   **Type**: one of `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.
    -   **Scope**: Module or component affected (optional). For submodules, use the submodule name.
    -   **Subject**: Concise imperative summary (≤50 characters).
    -   **Body**: Explanation of what and why; for submodule-pointer commits, include the submodule log entries.
    -   **Footer**: `BREAKING CHANGE: <description>` or issue references like `Closes #<issue>` when applicable.
3.  **Generate** the commit message following the format below.
4.  **Execute** the commit:
    ```bash
    git --no-pager -C <repo_path> commit -m "<generated_message>"
    ```

---

## 🧩 Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Details
-   **`<type>`**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
-   **`<scope>`**: Parenthesis enclosed, optional but recommended.
-   **`<subject>`**: Imperative, present tense, no period at end (≤50 chars).
-   **`<body>`**: Motivation and context. Wrap at ~72 characters per line.
-   **`<footer>`**: Breaking changes or issue references.

---

## 🧾 Output Example

### Scenario: Main Repo Submodule Update

**Detected**: `ui` submodule changed from `a1b2c3d` to `e5f6g7h`.
**Submodule Logs**:
- `fix: align button text`
- `feat: add dark mode`

**Generated Commit**:
```
chore(ui): update ui submodule

Update ui pointer to include recent changes:
- fix: align button text
- feat: add dark mode
```

---

## 🧰 Notes & Constraints

-   **Accuracy**: Ensure the message accurately reflects the *staged* changes. Ignore unstaged changes.
-   **Automation**: You are authorized to execute the `git commit` commands directly. Do not ask for confirmation for every commit unless confidence is low.
-   **Separation**: Never combine changes from different repositories into one commit message. One commit per repository.
-   **No Changes**: If absolutely no staged changes are found in the main repo or submodules, output "No staged changes to commit." and exit.

### Evidence Priority

`git diff --cached` output is considered **primary staged-change evidence**.
Primary evidence MUST override: heuristic judgments, cleanliness assumptions, empty status outputs, submodule working tree state.