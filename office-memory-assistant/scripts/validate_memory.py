#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import re
from pathlib import Path

from init_workspace import FILES as DEFAULT_FILES


REQUIRED = [
    "manifest.json",
    "profile/personal-profile.md",
    "profile/company-profile.md",
    "profile/role-and-responsibilities.md",
    "profile/work-preferences.md",
    "knowledge/project-cases.md",
    "knowledge/capabilities.md",
    "knowledge/reusable-paragraphs.md",
    "knowledge/terminology.md",
    "knowledge/forbidden-claims.md",
    "knowledge/leader-shared-materials.md",
    "knowledge/leader-talking-points.md",
    "style/writing-style.md",
    "style/favorite-phrases.md",
    "style/disliked-phrases.md",
    "style/audience-profiles.md",
    "style/leader-signals.md",
    "scenarios/bid-materials.md",
    "scenarios/weekly-report.md",
    "scenarios/monthly-report.md",
    "scenarios/company-intro.md",
    "scenarios/project-summary.md",
    "scenarios/meeting-minutes.md",
    "learning/learning-inbox.md",
    "learning/learning-log.md",
    "learning/correction-history.md",
    "learning/rejected-learning.md",
]


SENSITIVE_PATTERNS = {
    "email": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "phone_cn": re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"),
    "money": re.compile(r"\d+(?:\.\d+)?\s*(万元|亿元|元|万|亿)"),
    "id_like": re.compile(r"(?<!\d)\d{15,18}(?!\d)"),
}


SENSITIVE_LABELS = {
    "email": "邮箱 / email",
    "phone_cn": "手机号 / Chinese phone number",
    "money": "金额 / money amount",
    "id_like": "疑似证件号 / ID-like number",
}


def bilingual(cn: str, en: str) -> str:
    return f"{cn} / {en}"


def normalize_text(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines())


def meaningful(text: str) -> bool:
    stripped = re.sub(r"<!--.*?-->", "", text, flags=re.S).strip()
    lines = [line.strip() for line in stripped.splitlines() if line.strip() and not line.strip().startswith("#")]
    return bool(lines)


def user_filled(rel: str, text: str) -> bool:
    if rel in DEFAULT_FILES and normalize_text(text) == normalize_text(DEFAULT_FILES[rel]):
        return False
    return meaningful(text)


def completeness(data_dir: Path):
    weights = {
        "个人身份": (15, ["profile/personal-profile.md", "profile/role-and-responsibilities.md"]),
        "公司资料": (18, ["profile/company-profile.md", "knowledge/capabilities.md"]),
        "项目案例": (17, ["knowledge/project-cases.md"]),
        "写作偏好": (15, ["style/writing-style.md", "style/disliked-phrases.md"]),
        "禁忌边界": (15, ["knowledge/forbidden-claims.md"]),
        "上级偏好": (10, ["knowledge/leader-shared-materials.md", "style/leader-signals.md"]),
        "常用场景模板": (10, ["templates/bid-capability.md", "templates/weekly-report.md", "templates/company-intro.md"]),
    }
    score = 0
    detail = {}
    for name, (weight, files) in weights.items():
        filled = sum(1 for rel in files if (data_dir / rel).exists() and user_filled(rel, (data_dir / rel).read_text(encoding="utf-8", errors="ignore")))
        part = round(weight * filled / len(files))
        score += part
        detail[name] = {"score": part, "max": weight, "files": files}
    return score, detail


def main():
    parser = argparse.ArgumentParser(description="Validate OL-Memory.")
    parser.add_argument("--data-dir", default="OL-Memory")
    args = parser.parse_args()
    data_dir = Path(args.data_dir).expanduser().resolve()

    issues = []
    warnings = []
    if not data_dir.exists():
        print(json.dumps({
            "status": "BLOCKED",
            "issues": [bilingual(f"找不到资料库目录：{data_dir}", f"Missing data directory: {data_dir}")]
        }, ensure_ascii=False, indent=2))
        return

    for rel in REQUIRED:
        path = data_dir / rel
        if not path.exists():
            issues.append(bilingual(f"缺少必需文件：{rel}", f"Missing required file: {rel}"))
        elif rel.endswith(".md") and not user_filled(rel, path.read_text(encoding="utf-8", errors="ignore")):
            warnings.append(bilingual(f"可能还没有填写实质内容：{rel}", f"Possibly empty Markdown: {rel}"))

    manifest = data_dir / "manifest.json"
    if manifest.exists():
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            if data.get("learning_requires_confirmation") is not True:
                issues.append(bilingual(
                    "manifest.learning_requires_confirmation 必须为 true",
                    "manifest.learning_requires_confirmation must be true"
                ))
            if set(data.get("supported_platforms", [])) - {"Codex", "Trae"}:
                issues.append(bilingual(
                    "目前只支持 Codex 和 Trae",
                    "Only Codex and Trae are supported platforms"
                ))
        except json.JSONDecodeError as exc:
            issues.append(bilingual(f"manifest.json 格式无效：{exc}", f"Invalid manifest.json: {exc}"))

    pending_count = 0
    inbox = data_dir / "learning/learning-inbox.md"
    if inbox.exists():
        inbox_text = inbox.read_text(encoding="utf-8", errors="ignore")
        pending_count = inbox_text.count('"status": "pending"')
        if pending_count > 20:
            warnings.append(bilingual(
                f"待确认学习项过多：{pending_count}",
                f"Too many pending learning items: {pending_count}"
            ))

    for rel in REQUIRED:
        path = data_dir / rel
        if not path.exists() or not rel.endswith(".md"):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for label, pattern in SENSITIVE_PATTERNS.items():
            if pattern.search(text):
                display = SENSITIVE_LABELS.get(label, label)
                warnings.append(bilingual(
                    f"在 {rel} 发现敏感信息模式：{display}；请确认是否允许记录并标注公开边界。",
                    f"Sensitive pattern {label} found in {rel}; ensure it is allowed and marked."
                ))

    company_names = []
    if manifest.exists():
        try:
            name = json.loads(manifest.read_text(encoding="utf-8")).get("company_name")
            if name:
                company_names.append(name)
        except json.JSONDecodeError:
            pass
    company_profile = data_dir / "profile/company-profile.md"
    if company_profile.exists():
        matches = re.findall(r"公司/团队名称：\s*(.+)", company_profile.read_text(encoding="utf-8", errors="ignore"))
        company_names.extend([m.strip() for m in matches if m.strip()])
    if len(set(company_names)) > 1:
        names = sorted(set(company_names))
        warnings.append(bilingual(
            f"可能存在不一致的公司/团队名称：{names}",
            f"Potential conflicting company names: {names}"
        ))

    score, score_detail = completeness(data_dir)
    status = "BLOCKED" if issues else ("WARNING" if warnings else "HEALTHY")
    print(json.dumps({
        "status": status,
        "data_dir": str(data_dir),
        "completeness_score": score,
        "completeness_detail": score_detail,
        "pending_learning_count": pending_count,
        "issues": issues,
        "warnings": warnings,
        "next_suggestion": suggestion(score_detail)
    }, ensure_ascii=False, indent=2))


def suggestion(detail):
    for name, value in detail.items():
        if value["score"] < value["max"]:
            return bilingual(f"建议优先补充：{name}。", f"Suggested next step: fill {name}.")
    return bilingual(
        "资料库基础完整，可以继续补充更多真实案例和表达偏好。",
        "The library is basically complete; keep adding real cases and style preferences."
    )


if __name__ == "__main__":
    main()
