#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import shutil
from pathlib import Path


USAGE = """# Trae 使用办公室记忆助手 / Using Office Memory Assistant in Trae

1. 在 Trae 打开包含本目录的项目。
   Open the project containing this folder in Trae.
2. 先让 Trae 阅读 `TRAE_SYSTEM_PROMPT.md`。
   Ask Trae to read `TRAE_SYSTEM_PROMPT.md` first.
3. 当你要写材料时，明确说“根据 OL-Memory”。
   When drafting, explicitly say "based on OL-Memory".
4. 生成后要求 Trae 输出“使用资料、缺失信息、风险提醒、建议沉淀的学习项”。
   Require sources, missing facts, risk reminders, and learning candidates.
5. 你确认后，再让 Trae 写入对应资料文件。
   Only after confirmation should Trae write to memory files.

## 前期怎么录入档案 / Profile intake

先补最小可用档案：

Minimum useful setup:

- 我的档案：称呼、岗位、常写材料
- My Profile: name or preferred address, role, common writing tasks
- 公司资料：一句话介绍、服务范围、不能乱写内容
- Company: one-line intro, service scope, forbidden claims
- 项目案例：至少 1 个公开或匿名案例
- Project Cases: at least one public or anonymous case
- 写作风格：喜欢/不喜欢的表达
- Writing Style: preferred and disliked wording
- 上级偏好：上级转发的文章、短视频、截图、评论
- Leader Signals: articles, short videos, screenshots, and comments shared by the leader

## 能帮你做什么 / What it can do

- 投标材料、公司能力说明 / bid materials and capability statements
- 公司介绍 / company introductions
- 周报、月报、述职 / weekly reports, monthly reports, performance reviews
- 项目总结、案例包装 / project summaries and case packaging
- 会议纪要转行动项、风险清单、汇报材料 / meeting notes into actions, risks, and reports
- 去 AI 味、按你的风格改写 / remove generic AI tone and match your writing style
- 结合上级转发内容写出上级更容易接受的角度 / use leader-shared content to infer preferred angles

## 本地页面怎么打开 / Open the local UI

如果你想用可视化页面编辑资料库，在本机运行：

If you want to edit the memory library visually, run this on your computer:

```bash
python3 ~/.codex/skills/office-memory-assistant/scripts/launch_ui.py --data-dir /absolute/path/to/OL-Memory --open
```

`127.0.0.1` 只代表你自己的电脑。电脑关机或重启后，资料不会丢，但页面服务会停止；下次再运行同一条命令，并打开终端打印出来的地址即可。如果 `5173` 被占用，启动器会自动换一个端口。

`127.0.0.1` means your own computer. After shutdown or restart, the data is still there, but the UI server stops. Run the same command again and open the URL printed in Terminal. If `5173` is busy, the launcher will choose another port.
"""

SYSTEM = """你是用户的办公室记忆助手。

你必须优先读取 `OL-Memory/`。如果项目里只有旧版 `my-office-memory/` 或 `office-memory-data/`，也可以兼容读取。
你不能编造公司事实、客户名称、金额、资质、奖项、专利、团队规模或排名。
上级转发的短视频、文章、截图或评论只能作为偏好信号，不能当成公司事实。
你必须标注资料来源和缺失信息。
你必须在每次任务后提出可学习项。
未经用户确认，不要写入长期资料。
只支持 Codex 和 Trae 工作流，不要引导用户使用其他平台适配。
"""

WORKFLOW = """# Trae 工作流 / Trae Workflow

## 第一次开始 / First start

先补最小资料：个人岗位、公司一句话介绍、服务范围、1 个项目案例、禁止乱写内容、喜欢/不喜欢的表达。

Start with minimum data: role, company one-liner, service scope, one case, forbidden claims, preferred and disliked wording.

## 生成材料 / Drafting

1. 判断场景：投标材料、周报、月报、公司介绍、项目总结或会议纪要。
   Identify the scenario: bid material, weekly report, monthly report, company intro, project summary, or meeting minutes.
2. 读取相关 Markdown 文件。
   Read relevant Markdown files.
3. 如果是给上级看的内容，读取 `knowledge/leader-shared-materials.md`、`knowledge/leader-talking-points.md`、`style/leader-signals.md`。
   For leader-facing writing, read `knowledge/leader-shared-materials.md`, `knowledge/leader-talking-points.md`, and `style/leader-signals.md`.
4. 发现缺失关键事实时先问；如果用户要求先草稿，则标记缺失。
   Ask when key facts are missing; if the user wants a draft first, mark the missing facts.
5. 输出：草稿、使用资料、缺失信息、风险提醒、建议学习项。
   Output draft, sources, missing facts, risk reminders, and learning candidates.

## 上级偏好 / Leader-shared materials

When the user provides leader-shared materials, store them as signals:

- `knowledge/leader-shared-materials.md`: raw note, link, summary, leader comment, keywords
- `style/leader-signals.md`: likely leader concerns and preferred angles
- `knowledge/leader-talking-points.md`: reusable framing

Never treat leader-shared content as verified company facts unless the user confirms it separately.

## 学习沉淀 / Learning

1. 把用户反馈分成 fact、preference、case、phrase、forbidden、template、audience、correction。
   Classify feedback into fact, preference, case, phrase, forbidden, template, audience, or correction.
2. 先写入 `learning/learning-inbox.md`，状态为 pending。
   Write to `learning/learning-inbox.md` first as pending.
3. 用户确认后，再追加到建议目标文件，并写入 `learning/learning-log.md`。
   After confirmation, append to the suggested target file and write `learning/learning-log.md`.
4. 用户拒绝后，写入 `learning/rejected-learning.md`。
   If rejected, write to `learning/rejected-learning.md`.
"""


def main():
    parser = argparse.ArgumentParser(description="Export Trae-compatible pack.")
    parser.add_argument("--data-dir", default="OL-Memory")
    parser.add_argument("--out-dir", default="trae-pack")
    args = parser.parse_args()

    data_dir = Path(args.data_dir).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "TRAE_USAGE.md").write_text(USAGE, encoding="utf-8")
    (out_dir / "TRAE_SYSTEM_PROMPT.md").write_text(SYSTEM, encoding="utf-8")
    (out_dir / "TRAE_WORKFLOW.md").write_text(WORKFLOW, encoding="utf-8")

    target_data = out_dir / "OL-Memory"
    if target_data.exists():
        shutil.rmtree(target_data)
    if data_dir.exists():
        shutil.copytree(data_dir, target_data, ignore=shutil.ignore_patterns("outputs"))
    else:
        target_data.mkdir()

    print(f"Exported Trae pack: {out_dir}")


if __name__ == "__main__":
    main()
