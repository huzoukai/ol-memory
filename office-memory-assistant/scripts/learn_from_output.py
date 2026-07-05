#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


TARGET_BY_TYPE = {
    "fact": "profile/company-profile.md",
    "preference": "style/writing-style.md",
    "case": "knowledge/project-cases.md",
    "phrase": "knowledge/reusable-paragraphs.md",
    "forbidden": "knowledge/forbidden-claims.md",
    "template": "templates/project-summary.md",
    "audience": "style/audience-profiles.md",
    "correction": "learning/correction-history.md",
}


def now():
    return datetime.now(timezone.utc).astimezone()


def item_id(index=1):
    return f"learn_{now().strftime('%Y%m%d_%H%M%S')}_{index:03d}"


def classify(feedback: str):
    lowered = feedback.lower()
    if any(k in feedback for k in ["不喜欢", "讨厌", "别这么写", "不要用", "不能出现"]):
        typ = "forbidden" if any(k in feedback for k in ["不能", "禁止", "不要用"]) else "preference"
    elif any(k in feedback for k in ["项目", "案例"]):
        typ = "case"
    elif any(k in feedback for k in ["上级", "客户", "评委", "同事"]):
        typ = "audience"
    elif any(k in lowered for k in ["template", "模板"]):
        typ = "template"
    else:
        typ = "correction"
    return typ


def suggest_target(typ: str, feedback: str):
    if typ in {"preference", "forbidden"} and any(k in feedback for k in ["不喜欢", "讨厌", "不要用", "不能出现", "禁用"]):
        return "style/disliked-phrases.md" if typ == "preference" else "knowledge/forbidden-claims.md"
    return TARGET_BY_TYPE[typ]


def append(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
    path.write_text(existing.rstrip() + "\n\n" + text.rstrip() + "\n", encoding="utf-8")


def load_pending(inbox: Path):
    text = inbox.read_text(encoding="utf-8", errors="ignore") if inbox.exists() else ""
    items = []
    for match in re.finditer(r"```json\n(.*?)\n```", text, re.S):
        try:
            item = json.loads(match.group(1))
            if item.get("status") == "pending":
                items.append(item)
        except json.JSONDecodeError:
            pass
    return items


def rewrite_inbox(inbox: Path, items):
    content = "# 学习收件箱\n\n<!-- pending learning items as JSON blocks -->\n"
    for item in items:
        if item.get("status") == "pending":
            content += "\n```json\n" + json.dumps(item, ensure_ascii=False, indent=2) + "\n```\n"
    inbox.write_text(content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Create, accept, or reject learning items.")
    parser.add_argument("--data-dir", default="OL-Memory")
    parser.add_argument("--feedback", help="User feedback to convert into pending learning.")
    parser.add_argument("--type", choices=sorted(TARGET_BY_TYPE), help="Override learning type.")
    parser.add_argument("--target-file", help="Override target file.")
    parser.add_argument("--source-task", default="office_memory_task")
    parser.add_argument("--accept", help="Accept pending learning id.")
    parser.add_argument("--reject", help="Reject pending learning id.")
    args = parser.parse_args()

    data_dir = Path(args.data_dir).expanduser().resolve()
    inbox = data_dir / "learning/learning-inbox.md"
    log = data_dir / "learning/learning-log.md"
    rejected = data_dir / "learning/rejected-learning.md"
    data_dir.mkdir(parents=True, exist_ok=True)

    if args.feedback:
        typ = args.type or classify(args.feedback)
        item = {
            "id": item_id(),
            "type": typ,
            "status": "pending",
            "source_task": args.source_task,
            "content": args.feedback,
            "suggested_target_file": args.target_file or suggest_target(typ, args.feedback),
            "confidence": "user_feedback",
            "created_at": now().isoformat(timespec="seconds")
        }
        append(inbox, "```json\n" + json.dumps(item, ensure_ascii=False, indent=2) + "\n```")
        print(json.dumps({"status": "pending_created", "item": item}, ensure_ascii=False, indent=2))
        return

    if args.accept or args.reject:
        action_id = args.accept or args.reject
        items = load_pending(inbox)
        kept = []
        found = None
        for item in items:
            if item.get("id") == action_id:
                found = item
            else:
                kept.append(item)
        if not found:
            print(json.dumps({"status": "not_found", "id": action_id}, ensure_ascii=False, indent=2))
            return
        if args.accept:
            found["status"] = "accepted"
            target = data_dir / found["suggested_target_file"]
            append(target, f"- {found['content']}")
            append(log, "```json\n" + json.dumps(found, ensure_ascii=False, indent=2) + "\n```")
            status = "accepted"
        else:
            found["status"] = "rejected"
            append(rejected, "```json\n" + json.dumps(found, ensure_ascii=False, indent=2) + "\n```")
            status = "rejected"
        rewrite_inbox(inbox, kept)
        print(json.dumps({"status": status, "item": found}, ensure_ascii=False, indent=2))
        return

    print(json.dumps({"status": "noop", "hint": "Use --feedback, --accept, or --reject."}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
