#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INIT_SCRIPT = ROOT / "scripts" / "init_workspace.py"


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def split_items(text: str):
    return [item.strip() for item in text.replace("；", ";").replace("，", ",").split(",") if item.strip()]


def bullets(text: str):
    items = split_items(text)
    if not items and text.strip():
        items = [text.strip()]
    return "\n".join(f"- {item}" for item in items) if items else "- "


def main():
    parser = argparse.ArgumentParser(description="Write first-run OL-Memory intake answers.")
    parser.add_argument("--data-dir", default="OL-Memory")
    parser.add_argument("--name", required=True, help="Preferred name or form of address.")
    parser.add_argument("--role", required=True, help="Job role.")
    parser.add_argument("--common-docs", required=True, help="Common writing tasks, comma-separated.")
    parser.add_argument("--company-name", default="", help="Company or team name.")
    parser.add_argument("--company-intro", required=True, help="One-line company/team intro.")
    parser.add_argument("--service-scope", required=True, help="Service scope or capability list.")
    parser.add_argument("--project-case", required=True, help="One recent public/anonymous/private case.")
    parser.add_argument("--forbidden-claims", required=True, help="Facts or claims AI must not invent.")
    parser.add_argument("--writing-tone", required=True, help="Preferred writing tone.")
    parser.add_argument("--disliked-phrases", default="", help="Disliked phrases, comma-separated.")
    parser.add_argument("--leader-signals", default="", help="Optional leader-shared topic or preference signal.")
    args = parser.parse_args()

    data_dir = Path(args.data_dir).expanduser().resolve()
    init = subprocess.run(["python3", str(INIT_SCRIPT), "--data-dir", str(data_dir)], text=True, capture_output=True)
    if init.returncode != 0:
        raise SystemExit(init.stderr or init.stdout)

    write(data_dir / "profile/personal-profile.md", f"""# 个人资料

- 称呼：{args.name}
- 岗位/角色：{args.role}
- 常写材料：{args.common_docs}
""")

    write(data_dir / "profile/role-and-responsibilities.md", f"""# 岗位职责

- 主要职责：{args.role}
- 常参与项目：{args.project_case}
- 协作对象：待补充
""")

    write(data_dir / "profile/company-profile.md", f"""# 公司资料

- 公司/团队名称：{args.company_name}
- 一句话介绍：{args.company_intro}
- 主要客户类型：待补充
- 服务范围：{args.service_scope}
- 资质/奖项/认证（需证据）：待补充，未确认不得编造
""")

    write(data_dir / "knowledge/capabilities.md", f"""# 能力库

- 核心能力：{args.service_scope}
- 交付能力：待补充
- 技术/服务能力：{args.service_scope}
- 证据来源：首次启动问答，后续需要补充真实证据
""")

    write(data_dir / "knowledge/project-cases.md", f"""# 项目案例

## 首次录入案例

- 项目名称：待补充
- 可公开程度：待确认
- 背景：{args.project_case}
- 我的职责：待补充
- 结果：待补充
- 可复用表达：待补充
""")

    write(data_dir / "knowledge/forbidden-claims.md", f"""# 禁止编造和敏感边界

{bullets(args.forbidden_claims)}
- 禁止无证据使用：行业领先、全国第一、革命性、全链路赋能
- 客户名称公开规则：未确认不得公开
- 金额公开规则：未确认不得编造
- 资质/奖项证明要求：必须有证据
""")

    write(data_dir / "style/writing-style.md", f"""# 写作风格

- 总体语气：{args.writing_tone}
- 偏好：少 AI 味，优先写事实、动作、边界和下一步
""")

    write(data_dir / "style/disliked-phrases.md", f"""# 不喜欢的表达

{bullets(args.disliked_phrases)}
""")

    write(data_dir / "profile/work-preferences.md", """# 工作偏好

- 希望 AI 多问问题还是先给草稿：先给保守草稿，再列缺失信息
- 输出保守程度：不夸大，不写无证据结论
""")

    if args.leader_signals.strip():
        write(data_dir / "style/leader-signals.md", f"""# 上级偏好

记录上级平时转发的文章、短视频、讲话、截图或会议里反复强调的东西，用来判断上级最近在意什么。

## 最近关注主题

- {args.leader_signals}

## 喜欢的表达角度

- 待补充

## 不喜欢的表达角度

- 待补充

## 写材料时可借用的判断

- {args.leader_signals}
""")

    manifest_path = data_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["profile_name"] = args.name
    manifest["company_name"] = args.company_name
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "status": "ok",
        "data_dir": str(data_dir),
        "written": [
            "profile/personal-profile.md",
            "profile/role-and-responsibilities.md",
            "profile/company-profile.md",
            "knowledge/capabilities.md",
            "knowledge/project-cases.md",
            "knowledge/forbidden-claims.md",
            "style/writing-style.md",
            "style/disliked-phrases.md",
            "profile/work-preferences.md"
        ],
        "next": "Run launch_ui.py so the user can review and refine the generated profile."
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
