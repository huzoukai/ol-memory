# Onboarding / 新手教学

Use this guide when the user is new, when `127.0.0.1` is not running, or when they ask how to restart after shutting down the computer.

当用户第一次使用、打不开 `127.0.0.1`、或关机后不知道怎么重启时，按这份流程引导。

## First-Time Start / 第一次开始

1. Install the OL-Memory skill in Codex.
   先在 Codex 安装 OL-Memory Skill。
2. Say the startup phrase to Codex.
   对 Codex 说启动口令：

```text
开始启动 OL
```

3. Codex should ask the required intake questions in chat before opening the UI.
   Codex 应该先在聊天框自动提问，收集必填资料，再打开页面。

Required intake:

必填问答：

- preferred name and role / 称呼和岗位
- common writing tasks / 常写材料
- company or team one-liner and service scope / 公司或团队一句话介绍和服务范围
- one project case, anonymous is fine / 一个项目案例，可以匿名
- forbidden claims, sensitive boundaries, preferred and disliked wording / 不能乱写的内容、敏感边界、喜欢和不喜欢的表达

4. After the user answers, Codex writes the starter profile, then starts the local UI.
   用户回答后，Codex 写入第一版档案，再启动本地页面。

5. If manual startup is needed after data exists, use:
   如果需要手动启动，使用：

```bash
python3 ~/.codex/skills/office-memory-assistant/scripts/launch_ui.py --data-dir OL-Memory --open
```

6. Review and refine the generated starter profile in the UI.
   在页面里检查并补充自动生成的第一版档案：

- 我的档案：称呼、岗位、常写材料
- 公司资料：一句话介绍、服务范围、不能乱写的内容
- 项目案例：至少 1 个可公开或匿名案例
- 写作风格：喜欢和不喜欢的表达

7. Run validation.
   检查资料库健康状态：

```bash
python3 ~/.codex/skills/office-memory-assistant/scripts/validate_memory.py --data-dir OL-Memory
```

## How To Enter Profile Data / 前期怎么录入档案

Do not ask the user to fill every file before first value. Ask the required intake questions in the Agent chat first, then write the starter profile and let the UI be the review/edit surface.

不要要求用户一开始填满所有资料。先在 Agent 聊天框问必填问题，写出第一版档案，页面只作为检查和补充的后台：

1. `我的档案 / My Profile`
   Fill name or preferred form of address, job role, main responsibilities, and common writing tasks.
   填称呼、岗位、主要职责、经常写什么材料。
2. `公司资料 / Company`
   Fill one-line company intro, service scope, real capabilities, and facts that must not be invented.
   填公司一句话介绍、服务范围、真实能力、不能乱写的内容。
3. `项目案例 / Project Cases`
   Add 1-3 recent cases. Mark each as public, anonymous, or private.
   录入 1-3 个最近项目，并标注可公开、匿名或不可公开。
4. `写作风格 / Writing Style`
   Add preferred tone, disliked AI-sounding words, audience preferences, and reusable phrases.
   填喜欢的语气、不喜欢的 AI 味词、不同受众偏好、可复用句子。
5. `上级偏好 / Leader Signals`
   Add articles, short videos, screenshots, or comments shared by the leader. These teach the assistant what the leader values.
   录入上级转发的文章、短视频、截图或评论，用来学习上级最近在意什么。
6. `学习收件箱 / Learning Inbox`
   After each task, review pending learning items before accepting them.
   每次使用后，先审核待学习项，再确认是否沉淀。

Minimum useful profile:

最小可用档案：

- who the user is / 用户是谁
- what company or team they represent / 用户代表哪个公司或团队
- what the company actually does / 公司真实做什么
- one project case / 一个项目案例
- forbidden or sensitive claims / 禁止和敏感边界
- preferred tone / 偏好的表达风格

## Formal Daily Use / 正式使用

To open OL-Memory again, say:

再次打开 OL-Memory 时，直接说：

```text
开始启动 OL
```

Use Codex prompts like:

```text
根据 OL-Memory，帮我写一段投标材料里的公司能力说明，正式但不要夸大。
```

Daily use happens mostly in the Agent chat box. The user can paste new facts, corrections, leader-shared links or writing tasks directly into chat. Use the UI only when they want to review or edit the memory files.

日常使用主要在 Agent 聊天框里完成。用户可以直接把新信息、修改意见、上级转发链接或写作任务发到聊天框。页面主要用于检查和维护资料库。

The assistant should read relevant memory, draft with source notes, list missing facts, warn about external-use risks, and suggest learning items.

AI should help with:

它可以帮用户做：

- bid/company capability statements / 投标材料、公司能力说明
- company introductions / 公司介绍
- weekly reports / 周报
- monthly reports and performance reviews / 月报、述职
- project summaries and case packaging / 项目总结、案例包装
- meeting minutes into action/risk/report materials / 会议纪要转行动项、风险清单、汇报材料
- style cleanup and anti-AI wording / 去 AI 味、按用户风格改写
- leader-signal-aware writing based on shared videos/articles / 结合上级转发的短视频和文章调整写作角度
- learning user corrections after confirmation / 用户确认后沉淀修改偏好

## When 127.0.0.1 Is Not Running / 打不开 127.0.0.1 时

`127.0.0.1` is a local address. It only works while the UI server is running on this computer. The launcher prints the actual URL; if port `5173` is busy, it may use another port.

`127.0.0.1` 是本机地址，只有页面服务正在运行时才可用。启动器会打印实际地址；如果 `5173` 被占用，可能会使用其他端口。

If the page cannot open, run:

```bash
python3 ~/.codex/skills/office-memory-assistant/scripts/launch_ui.py --data-dir /absolute/path/to/OL-Memory --open
```

If the user is in the project folder that contains `OL-Memory`, this shorter command is enough:

```bash
python3 ~/.codex/skills/office-memory-assistant/scripts/launch_ui.py --data-dir OL-Memory --open
```

## After Shutdown Or Restart / 关机或重启后

The data remains on disk. Only the local UI server stops.

资料仍然保存在磁盘上。停止的只是本地页面服务。

After restarting the computer:

1. Open Terminal or ask Codex to run the launcher.
2. Run `launch_ui.py` with the same `--data-dir`.
3. Open the URL printed by the launcher.

1. 打开终端，或让 Codex 帮你运行启动器。
2. 用相同的 `--data-dir` 运行 `launch_ui.py`。
3. 打开启动器打印出来的 URL。

## If The User Only Wants Codex Writing / 只想让 Codex 写材料

The UI is optional after data exists. Codex can still use the Markdown library directly:

资料库存在后，UI 不是必需的。Codex 可以直接读取 Markdown 资料库：

```text
根据 /path/to/OL-Memory，帮我写周报。
```

## Minimum Viable Setup / 最小可用配置

Do not force the user to complete every field before first value. A useful first draft only needs:

- company one-line intro
- service scope or capability list
- one project case
- forbidden claims
- preferred tone

Mark all other facts as missing.
