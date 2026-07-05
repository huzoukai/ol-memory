# Workflow

## A. Initialize

Run `scripts/init_workspace.py --data-dir OL-Memory` when the library is missing. The script creates Markdown source files, `manifest.json`, templates, learning files, outputs, `.gitignore`, and a completeness report.

Ask the user to add facts through the UI or by editing Markdown. Do not place private facts in the skill directory.

## B. Generate Office Material

1. Identify the scenario: `bid-materials`, `weekly-report`, `monthly-report`, `company-intro`, `project-summary`, or `meeting-minutes`.
2. Run `compose_context.py` with the scenario and optional task text.
3. Read the returned context bundle and sources.
4. Draft conservatively using only supported facts.
5. Include the required output sections from `SKILL.md`.

## C. Learn After Use

Only learn after explicit user confirmation.

When the user gives feedback or edits:

1. Classify candidates as `fact`, `preference`, `case`, `phrase`, `forbidden`, `template`, `audience`, or `correction`.
2. Create pending entries in `learning/learning-inbox.md`.
3. Ask the user to accept or reject.
4. On accept, append to the suggested target file and record `learning/learning-log.md`.
5. On reject, move the item to `learning/rejected-learning.md`.

Never auto-confirm sensitive facts such as customers, amounts, certifications, patents, awards, rankings, or personal identifiers.

## C2. Learn From Leader-Shared Materials

When the user provides an article, short video, screenshot, link, or forwarded comment from their leader:

1. Record the raw note, link, leader comment, summary, keywords, and likely signals in `knowledge/leader-shared-materials.md`.
2. Extract likely leader preferences into `style/leader-signals.md`: topics, value words, disliked angles, and writing implications.
3. Extract reusable framing into `knowledge/leader-talking-points.md`.
4. Mark all extracted items as signals, not facts. Do not use them as evidence for company capability, customer claims, awards, certifications, or performance.
5. In future drafts for leader-facing reports, monthly reviews, plans, or summaries, use these signals to choose angle and emphasis.

## D. Maintain Memory

Use the UI or Markdown files to edit data. Run `validate_memory.py` after changes. Treat `BLOCKED` validation as a stop sign before external-facing drafts.

## Required Draft Sections

Every generation must include:

- `草稿`
- `使用资料`
- `缺失信息`
- `风险提醒`
- `建议学习项`

## Small-User Bias

When the user is unsure what to provide, ask for concrete examples:

- "最近做过的 1-2 个项目是什么？"
- "哪些客户或金额不能公开？"
- "你上级最常改掉哪些词？"
- "这份材料给谁看？"
