---
name: office-memory-assistant
description: Local office memory system for drafting workplace documents with user/company context and confirmed learning. Use when the user says "开始启动 OL", "启动 OL", "Start OL", or when Codex needs to initialize or maintain OL-Memory, legacy my-office-memory or office-memory-data, write bid materials, company capability statements, company introductions, weekly/monthly reports, performance reviews, project summaries, meeting minutes, or when the user asks AI to use personal profiles, company facts, case libraries, writing preferences, forbidden claims, or to remember corrected office-writing preferences for later use in Codex or Trae.
---

# Office Memory Assistant

Use this skill to make office writing depend on a visible local memory library instead of generic model guesses. Keep the skill installation directory free of private user data. Store user memory in the current project as `OL-Memory/` unless the user gives another path. Treat legacy `my-office-memory/` and `office-memory-data/` as supported older names.

## Core Workflow

If the user says "开始启动 OL", "启动 OL", or "Start OL", treat it as the first-run launcher command for OL-Memory. First ask the required intake questions in chat. After the user answers, write the first profile with `scripts/intake_profile.py`, then start the local UI with `scripts/launch_ui.py --data-dir <path> --open` so the user can review and refine it.

Required first-run intake questions:

1. 你希望我怎么称呼你？你的岗位/角色是什么？/ What should I call you, and what is your role?
2. 你常写哪些材料？/ What documents do you often write?
3. 你的公司/团队一句话介绍和服务范围是什么？/ What is your company/team one-liner and service scope?
4. 先给我 1 个项目案例，可以匿名。/ Give one project case; anonymous is fine.
5. 有哪些不能乱写的内容、敏感边界、喜欢/不喜欢的表达？/ What must not be invented, and what writing tone or phrases do you prefer or dislike?

1. Locate `OL-Memory/`, legacy `my-office-memory/`, legacy `office-memory-data/`, or the path the user provides in the current workspace or a parent directory.
2. If no memory library exists, collect the required intake answers and run `scripts/intake_profile.py --data-dir OL-Memory ...`, then start the UI.
3. Before drafting, read only relevant files from `profile/`, `knowledge/`, `style/`, `scenarios/`, and `templates/`.
4. Validate sensitive facts. Never invent customers, project amounts, certifications, patents, awards, team size, rankings, years, or named case details without source text.
5. Draft the requested office material.
6. Always include: draft text, used sources, missing information, external-use risks, and learning candidates.
7. Do not write long-term memory automatically. Only run learning writes after the user explicitly confirms the learning item.

## Common Commands

Initialize a memory library:

```bash
python3 ~/.codex/skills/office-memory-assistant/scripts/init_workspace.py --data-dir OL-Memory
```

Write first-run intake answers:

```bash
python3 ~/.codex/skills/office-memory-assistant/scripts/intake_profile.py --data-dir OL-Memory --name "林夏" --role "项目经理" --common-docs "周报,述职,投标材料" --company-intro "为制造业客户提供数字化服务" --service-scope "需求调研、方案设计、上线陪跑" --project-case "某园区运营看板项目，匿名可用" --forbidden-claims "客户名称、金额、资质、奖项未确认不能写" --writing-tone "正式、简洁、少 AI 味" --disliked-phrases "赋能,持续优化"
```

Compose task context before drafting:

```bash
python3 ~/.codex/skills/office-memory-assistant/scripts/compose_context.py --data-dir OL-Memory --scenario bid-materials
```

Create a pending learning item from user feedback:

```bash
python3 ~/.codex/skills/office-memory-assistant/scripts/learn_from_output.py --data-dir OL-Memory --feedback "我不喜欢持续优化和赋能"
```

Add a leader-shared article/video as a preference signal:

```bash
python3 ~/.codex/skills/office-memory-assistant/scripts/add_leader_material.py --data-dir OL-Memory --title "上级转发的文章" --summary "文章主要讲..." --leader-comment "这个思路可以学一下" --signals "上级重视结果、复盘和责任边界"
```

Accept a pending learning item after user confirmation:

```bash
python3 ~/.codex/skills/office-memory-assistant/scripts/learn_from_output.py --data-dir OL-Memory --accept learn_YYYYMMDD_HHMMSS_001
```

Validate the memory library:

```bash
python3 ~/.codex/skills/office-memory-assistant/scripts/validate_memory.py --data-dir OL-Memory
```

Export a Trae-compatible pack:

```bash
python3 ~/.codex/skills/office-memory-assistant/scripts/export_trae_pack.py --data-dir OL-Memory --out-dir trae-pack
```

Run deterministic self-tests:

```bash
python3 ~/.codex/skills/office-memory-assistant/scripts/self_test.py
```

Start the local editor UI:

```bash
python3 ~/.codex/skills/office-memory-assistant/scripts/launch_ui.py --data-dir /absolute/path/to/OL-Memory --open
```

If the local URL does not open, the local UI server is not running. Run the same `launch_ui.py` command again. User data remains in `OL-Memory/` after shutdown; only the local server needs restarting.

## Drafting Format

Every generated office document must use this shape:

```markdown
## 草稿
[正文]

## 使用资料
- path/to/file.md: relevant fact or preference

## 缺失信息
- [中文说明 / English note for missing key facts, or "暂无关键缺失 / No key gaps"]

## 风险提醒
- [中文说明 / English note for unsupported claims, sensitive details, and external-use review notes]

## 建议学习项
- type: preference | fact | case | phrase | forbidden | template | audience | correction
  content: [candidate memory]
  suggested_target_file: [relative path]
```

## Reference Routing

- Read `references/workflow.md` for generation, learning, and maintenance workflow details.
- Read `references/onboarding.md` when a user is new, needs bilingual first-run guidance, asks how to enter profile data, asks what the assistant can do, cannot open `127.0.0.1`, or asks how to restart after shutdown.
- Read `references/data-schema.md` before editing scripts or memory-library structure.
- Read `references/safety-rules.md` before drafting external-facing or claim-heavy content.
- Read `references/platform-codex.md` when using the skill inside Codex.
- Read `references/platform-trae.md` when exporting or explaining Trae usage.

## Scenario Coverage

Support at least these scenarios: bid/company capability statements, weekly reports, monthly reports or performance reviews, company introductions, project case packaging, and meeting-minutes-to-material conversion.

For missing facts, ask a short question when the fact is necessary to complete the task. If the user wants a draft immediately, mark the gap explicitly and write conservatively.

When asked "how do I start using this now?", answer with a short bilingual path: install the Skill, say `开始启动 OL`, answer the required intake questions in chat, let Codex write the starter profile and launch the UI, then use the Agent chat box for daily information and writing requests.

When the user gives leader-shared articles, short videos, screenshots, or forwarded comments, treat them as preference and attention signals. Store them in `knowledge/leader-shared-materials.md`, summarize likely leader concerns in `style/leader-signals.md`, and never treat them as verified company facts unless the user separately confirms them.
