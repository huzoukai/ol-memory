#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
from pathlib import Path


SCENARIO_FILES = {
    "bid-materials": ["profile/company-profile.md", "knowledge/capabilities.md", "knowledge/project-cases.md", "knowledge/forbidden-claims.md", "knowledge/leader-talking-points.md", "style/writing-style.md", "style/disliked-phrases.md", "style/leader-signals.md", "scenarios/bid-materials.md", "templates/bid-capability.md"],
    "weekly-report": ["profile/personal-profile.md", "profile/role-and-responsibilities.md", "knowledge/leader-shared-materials.md", "knowledge/leader-talking-points.md", "style/writing-style.md", "style/audience-profiles.md", "style/leader-signals.md", "scenarios/weekly-report.md", "templates/weekly-report.md"],
    "monthly-report": ["profile/personal-profile.md", "profile/role-and-responsibilities.md", "knowledge/leader-shared-materials.md", "knowledge/leader-talking-points.md", "style/writing-style.md", "style/leader-signals.md", "scenarios/monthly-report.md", "templates/monthly-report.md"],
    "company-intro": ["profile/company-profile.md", "knowledge/capabilities.md", "knowledge/project-cases.md", "knowledge/forbidden-claims.md", "knowledge/leader-talking-points.md", "style/writing-style.md", "scenarios/company-intro.md", "templates/company-intro.md"],
    "project-summary": ["knowledge/project-cases.md", "knowledge/leader-talking-points.md", "style/writing-style.md", "style/leader-signals.md", "scenarios/project-summary.md", "templates/project-summary.md"],
    "meeting-minutes": ["profile/personal-profile.md", "profile/role-and-responsibilities.md", "knowledge/leader-talking-points.md", "style/writing-style.md", "style/leader-signals.md", "scenarios/meeting-minutes.md"],
    "leader-learning": ["knowledge/leader-shared-materials.md", "knowledge/leader-talking-points.md", "style/leader-signals.md", "style/audience-profiles.md"],
}


def main():
    parser = argparse.ArgumentParser(description="Compose relevant memory context.")
    parser.add_argument("--data-dir", default="OL-Memory")
    parser.add_argument("--scenario", choices=sorted(SCENARIO_FILES), required=True)
    parser.add_argument("--task", default="")
    parser.add_argument("--max-chars", type=int, default=24000)
    args = parser.parse_args()

    data_dir = Path(args.data_dir).expanduser().resolve()
    sources = []
    chunks = []
    for rel in SCENARIO_FILES[args.scenario]:
        path = data_dir / rel
        if path.exists():
            text = path.read_text(encoding="utf-8", errors="ignore").strip()
            if text:
                sources.append(rel)
                chunks.append(f"\n--- SOURCE: {rel} ---\n{text}\n")

    context = "".join(chunks)
    if len(context) > args.max_chars:
        context = context[:args.max_chars] + "\n\n[TRUNCATED]\n"

    print(json.dumps({
        "status": "ok" if data_dir.exists() else "missing_data_dir",
        "data_dir": str(data_dir),
        "scenario": args.scenario,
        "task": args.task,
        "sources": sources,
        "draft_requirements": ["草稿", "使用资料", "缺失信息", "风险提醒", "建议学习项"],
        "context": context
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
