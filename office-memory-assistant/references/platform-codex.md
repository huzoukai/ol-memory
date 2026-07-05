# Codex Platform

Codex should use the local skill plus scripts.

1. Search for `OL-Memory/`, then legacy `my-office-memory/`, then legacy `office-memory-data/`, from the current workspace.
2. Initialize if missing.
3. If the user wants a visual editor or `127.0.0.1` is not running, start it with `launch_ui.py --data-dir OL-Memory --open`.
4. Use `compose_context.py` to gather relevant source files.
5. Draft with required sections.
6. Use `learn_from_output.py` only after user confirmation.
7. Run `validate_memory.py` after structural edits.

## Restarting The UI

The UI is a local server, so `http://127.0.0.1:5173/` works only while it is running. After shutdown, restart it from the project folder:

```bash
python3 ~/.codex/skills/office-memory-assistant/scripts/launch_ui.py --data-dir OL-Memory --open
```

If the user stores data somewhere else, pass the absolute data path.

Good user prompts:

- "根据 OL-Memory，写一段投标材料里的公司能力说明，正式但不要夸大。"
- "把我刚才改掉的这些表达沉淀成写作偏好。"
- "初始化办公室记忆助手资料库。"
