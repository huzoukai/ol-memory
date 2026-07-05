#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
from datetime import datetime, timezone
from pathlib import Path


def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def append(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else "# 上级转发内容\n"
    path.write_text(existing.rstrip() + "\n\n" + text.rstrip() + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Add leader-shared article/video material to OL-Memory.")
    parser.add_argument("--data-dir", default="OL-Memory")
    parser.add_argument("--title", default="未命名素材")
    parser.add_argument("--type", default="文章/短视频/截图/讲话/其他")
    parser.add_argument("--source", default="")
    parser.add_argument("--leader-comment", default="")
    parser.add_argument("--summary", required=True)
    parser.add_argument("--keywords", default="")
    parser.add_argument("--signals", default="")
    parser.add_argument("--use-for", default="周报/月报/述职/方案/投标/公司介绍")
    args = parser.parse_args()

    data_dir = Path(args.data_dir).expanduser().resolve()
    date = now_iso()
    block = f"""## {args.title}

- 日期：{date}
- 类型：{args.type}
- 来源或链接：{args.source}
- 上级转发时说了什么：{args.leader_comment}
- 内容摘要：{args.summary}
- 关键词：{args.keywords}
- 可能代表上级在意：{args.signals}
- 可用于哪些材料：{args.use_for}
- 是否可直接引用：否
"""
    append(data_dir / "knowledge/leader-shared-materials.md", block)
    print(f"Added leader material to {data_dir / 'knowledge/leader-shared-materials.md'}")


if __name__ == "__main__":
    main()
