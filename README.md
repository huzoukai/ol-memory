# OL-Memory

OL-Memory is a local-first office memory skill for Codex-style agents. It helps an agent remember confirmed workplace context, then use that context to draft practical office documents with clearer source grounding, missing-info reminders, and risk warnings.

OL means **Office Life**. The name is short, easy to say, and points to the real use case: keeping the useful parts of day-to-day work memory close at hand without turning them into a heavy database.

中文定位：**OL-Memory 是你的本地职场记忆库**。它不是自动监控工具，也不会替你编造信息；它只使用你确认录入的资料、你在聊天里补充的新信息，以及你要求它学习的文章/短视频/领导偏好信号。

## What It Helps With

- Company introductions, project summaries, proposals, tender/bid materials, weekly/monthly reports, meeting notes, review drafts, and performance summaries.
- Reusing your confirmed profile, role, company, service scope, project cases, writing style, and forbidden claims.
- Learning from day-to-day input, including leader-shared articles, short videos, internal phrasing preferences, and recurring standards.
- Producing bilingual missing-info and risk reminders, so drafts are easier to review before sending.

## Privacy Model

This repository contains the skill code only. Real user data should live outside the installed skill folder, usually in a local workspace named `OL-Memory/`.

Do not commit `OL-Memory/`, `.env`, logs, UI build folders, or exports containing private workplace information. The included `.gitignore` already excludes common local data paths.

## Install

Clone or download this repository, then copy the skill folder into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R office-memory-assistant ~/.codex/skills/office-memory-assistant
```

Restart Codex if it was already open.

## First Start

After installation, open the agent chat and say:

```text
开始启动 OL
```

English trigger:

```text
Start OL
```

The agent should not open the dashboard first. It should first ask a few required setup questions in chat, then initialize the local memory workspace and launch the page.

Required first-run questions:

1. What should OL-Memory call you, and what is your role?
2. What kinds of office documents do you write most often?
3. How would you describe your company/team and its service scope in one or two sentences?
4. What is one real project/case OL-Memory can remember? You may anonymize it.
5. What must OL-Memory avoid inventing, exaggerating, or mentioning?
6. What writing style, phrases, or leader preferences should OL-Memory follow or avoid?

After you answer, the agent initializes `OL-Memory/` and opens a local dashboard, usually at `http://127.0.0.1:<port>/`.

## Daily Use

Most daily use happens directly in the agent chat box. You can write short, natural instructions:

```text
根据 OL-Memory 帮我写一份本周工作总结。
```

```text
上级刚转发了一篇文章，重点是“客户体验”和“交付闭环”。帮我记录为学习素材，并结合这个方向改一下项目汇报。
```

```text
这句话以后不要用：“赋能业务高质量发展”。帮我记住。
```

```text
帮我根据公司介绍、我的岗位和最近项目，写一版投标用的团队能力介绍。
```

The dashboard is mainly for review, correction, and checking completeness. Chat is the main work entrance.

## If The Page Is Not Running

`127.0.0.1` is a local page. If the computer restarts, the terminal closes, or the server stops, the page will not keep running by itself.

The normal way to reopen it is to say in chat:

```text
启动 OL
```

If you need to start it manually:

```bash
python3 ~/.codex/skills/office-memory-assistant/scripts/launch_ui.py --data-dir OL-Memory --open
```

If `OL-Memory/` does not exist yet, initialize it first through the chat flow by saying `开始启动 OL`.

## Manual Initialization Fallback

The preferred path is agent-led setup. If you need a command-line fallback, use `intake_profile.py`:

```bash
python3 ~/.codex/skills/office-memory-assistant/scripts/intake_profile.py \
  --data-dir OL-Memory \
  --display-name "Your Name" \
  --role "Your Role" \
  --doc-types "weekly reports, project summaries, proposals" \
  --company-summary "Your company/team summary" \
  --project-case "One real or anonymized project case" \
  --forbidden-claims "Things the agent must not invent or mention" \
  --writing-preferences "Preferred style and disliked phrases"
```

Then launch the dashboard:

```bash
python3 ~/.codex/skills/office-memory-assistant/scripts/launch_ui.py --data-dir OL-Memory --open
```

## Output Standard

When OL-Memory drafts something, it should provide:

- The usable draft.
- Which confirmed memory it used.
- Missing information reminders in Chinese and English.
- Risk warnings in Chinese and English when claims may be unverifiable, sensitive, or overconfident.
- Suggested memory updates when the user confirms new facts.

## Developer Validation

From the repository root:

```bash
python3 office-memory-assistant/scripts/self_test.py
```

For the UI:

```bash
cd office-memory-assistant/assets/ui
npm ci
npm run build
```

For Codex skill validation, run the skill creator validator from your local Codex install if available:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py office-memory-assistant
```

## Public Release Checklist

Before publishing:

- Confirm `git status --short` does not show local memory data.
- Confirm `OL-Memory/`, logs, `.env`, `node_modules/`, and `dist/` are not tracked.
- Run the self test and UI build.
- Review `README.md` for any private company names, real people, or internal project details.
