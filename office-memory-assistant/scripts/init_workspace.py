#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


FILES = {
    "profile/personal-profile.md": "# 个人资料\n\n- 称呼：\n- 岗位/角色：\n- 常写材料：\n",
    "profile/company-profile.md": "# 公司资料\n\n- 公司/团队名称：\n- 一句话介绍：\n- 主要客户类型：\n- 服务范围：\n- 资质/奖项/认证（需证据）：\n",
    "profile/role-and-responsibilities.md": "# 岗位职责\n\n- 主要职责：\n- 常参与项目：\n- 协作对象：\n",
    "profile/work-preferences.md": "# 工作偏好\n\n- 希望 AI 多问问题还是先给草稿：\n- 输出保守程度：\n",
    "knowledge/project-cases.md": "# 项目案例\n\n## 案例 1\n\n- 项目名称：\n- 可公开程度：公开/匿名/不可公开\n- 背景：\n- 我的职责：\n- 结果：\n- 可复用表达：\n",
    "knowledge/capabilities.md": "# 能力库\n\n- 核心能力：\n- 交付能力：\n- 技术/服务能力：\n- 证据来源：\n",
    "knowledge/reusable-paragraphs.md": "# 可复用段落\n\n",
    "knowledge/terminology.md": "# 术语表\n\n",
    "knowledge/forbidden-claims.md": "# 禁止编造和敏感边界\n\n- 禁止无证据使用：行业领先、全国第一、革命性、全链路赋能\n- 客户名称公开规则：\n- 金额公开规则：\n- 资质/奖项证明要求：\n",
    "style/writing-style.md": "# 写作风格\n\n- 总体语气：简洁、正式、少 AI 味\n- 偏好：\n",
    "style/favorite-phrases.md": "# 喜欢的表达\n\n",
    "style/disliked-phrases.md": "# 不喜欢的表达\n\n- 赋能\n- 持续优化\n- 打造闭环\n",
    "style/audience-profiles.md": "# 受众偏好\n\n## 上级\n\n## 客户\n\n## 评委\n\n## 同事\n",
    "style/leader-signals.md": "# 上级偏好\n\n记录上级平时转发的文章、短视频、讲话、截图或会议里反复强调的东西，用来判断上级最近在意什么。\n\n## 最近关注主题\n\n- \n\n## 喜欢的表达角度\n\n- \n\n## 不喜欢的表达角度\n\n- \n\n## 写材料时可借用的判断\n\n- \n",
    "knowledge/leader-shared-materials.md": "# 上级转发内容\n\n## 素材 1\n\n- 日期：\n- 类型：短视频/文章/截图/讲话/其他\n- 来源或链接：\n- 上级转发时说了什么：\n- 内容摘要：\n- 关键词：\n- 可能代表上级在意：\n- 可用于哪些材料：周报/月报/述职/方案/投标/公司介绍\n- 是否可直接引用：否\n",
    "knowledge/leader-talking-points.md": "# 上级偏好的表达和论点\n\n这些不是公司事实，不能当资质或业绩写。它们用于判断上级喜欢的角度、价值观、话术和材料重点。\n\n## 可复用角度\n\n- \n\n## 常见关键词\n\n- \n\n## 写作提醒\n\n- 上级转发的内容通常只能作为偏好和方向，不能直接当成事实证据。\n",
    "scenarios/bid-materials.md": "# 投标材料 / 公司能力说明\n\n输出：公司能力说明、相关案例、服务优势、风险提示、缺失资料清单。\n",
    "scenarios/weekly-report.md": "# 周报\n\n输出：正式版、人话版、领导友好版。\n",
    "scenarios/monthly-report.md": "# 月报 / 述职\n\n输出：月度总结、亮点包装、问题复盘、下月计划。\n",
    "scenarios/company-intro.md": "# 公司介绍\n\n输出：正式版、简洁版、商务版和不同长度版本。\n",
    "scenarios/project-summary.md": "# 项目案例包装\n\n输出：项目案例段落、STAR 结构、投标可用版、匿名版。\n",
    "scenarios/meeting-minutes.md": "# 会议纪要转材料\n\n输出：行动项、对外说明、内部汇报、风险和待确认事项。\n",
    "learning/learning-inbox.md": "# 学习收件箱\n\n<!-- pending learning items as JSON blocks -->\n",
    "learning/learning-log.md": "# 学习日志\n\n",
    "learning/correction-history.md": "# 修改历史\n\n",
    "learning/rejected-learning.md": "# 拒绝学习项\n\n",
    "outputs/.gitkeep": "",
    "templates/bid-capability.md": "# 投标公司能力说明模板\n\n## 草稿\n\n## 使用资料\n\n## 缺失信息\n\n## 风险提醒\n\n## 建议学习项\n",
    "templates/weekly-report.md": "# 周报模板\n\n## 正式版\n\n## 人话版\n\n## 领导友好版\n",
    "templates/monthly-report.md": "# 月报模板\n\n## 月度总结\n\n## 亮点包装\n\n## 问题复盘\n\n## 下月计划\n",
    "templates/company-intro.md": "# 公司介绍模板\n\n## 50 字\n\n## 150 字\n\n## 商务版\n",
    "templates/project-summary.md": "# 项目总结模板\n\n## STAR 结构\n\n## 投标可用版\n\n## 匿名版\n",
}


def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(description="Initialize OL-Memory.")
    parser.add_argument("--data-dir", default="OL-Memory")
    args = parser.parse_args()

    data_dir = Path(args.data_dir).expanduser().resolve()
    data_dir.mkdir(parents=True, exist_ok=True)
    created = []

    manifest = data_dir / "manifest.json"
    if not manifest.exists():
        manifest.write_text(json.dumps({
            "schema_version": "1.0.0",
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "profile_name": "",
            "company_name": "",
            "data_dir_name": data_dir.name,
            "supported_platforms": ["Codex", "Trae"],
            "learning_requires_confirmation": True
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        created.append(str(manifest))

    for rel, content in FILES.items():
        if write_if_missing(data_dir / rel, content):
            created.append(str(data_dir / rel))

    gitignore = data_dir.parent / ".gitignore"
    line = f"{data_dir.name}/"
    if gitignore.exists():
        existing = gitignore.read_text(encoding="utf-8", errors="ignore").splitlines()
    else:
        existing = []
    if line not in existing:
        gitignore.write_text("\n".join(existing + [line]) + "\n", encoding="utf-8")

    print(json.dumps({
        "status": "ok",
        "data_dir": str(data_dir),
        "created_count": len(created),
        "created": created,
        "next": "Run validate_memory.py, then open assets/ui or edit Markdown files."
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
