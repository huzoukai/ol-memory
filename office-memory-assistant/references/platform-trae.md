# Trae Platform

Trae compatibility must not rely on Codex-only tools. Export a `trae-pack/` containing:

```text
trae-pack/
├── TRAE_USAGE.md
├── TRAE_SYSTEM_PROMPT.md
├── TRAE_WORKFLOW.md
└── OL-Memory/
```

The Trae workflow:

1. Open the project containing `trae-pack/`.
2. Ask Trae to read `TRAE_SYSTEM_PROMPT.md`.
3. Ask for output "根据 OL-Memory".
4. Require source list, missing facts, risk reminders, and learning candidates.
5. Confirm learning before writing to memory files.

## Startup Boundary

Trae can use the exported Markdown data without the UI. If the user wants the visual editor, start the Codex skill UI separately:

```bash
python3 ~/.codex/skills/office-memory-assistant/scripts/launch_ui.py --data-dir /absolute/path/to/OL-Memory --open
```

After shutdown, run the same command again.

Do not add adapters for platforms other than Codex and Trae.
