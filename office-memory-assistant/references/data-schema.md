# Data Schema

Canonical user data lives in `OL-Memory/`. Legacy `my-office-memory/` and `office-memory-data/` are still accepted when an older project already uses them.

```text
OL-Memory/
├── manifest.json
├── profile/
├── knowledge/
├── style/
├── scenarios/
├── learning/
├── outputs/
└── templates/
```

## Manifest

`manifest.json` stores:

- `schema_version`
- `created_at`
- `updated_at`
- `profile_name`
- `company_name`
- `data_dir_name`
- `supported_platforms`: only `Codex` and `Trae`
- `learning_requires_confirmation`: must be `true`

## Required Markdown Files

Profile:

- `profile/personal-profile.md`
- `profile/company-profile.md`
- `profile/role-and-responsibilities.md`
- `profile/work-preferences.md`

Knowledge:

- `knowledge/project-cases.md`
- `knowledge/capabilities.md`
- `knowledge/reusable-paragraphs.md`
- `knowledge/terminology.md`
- `knowledge/forbidden-claims.md`
- `knowledge/leader-shared-materials.md`
- `knowledge/leader-talking-points.md`

Style:

- `style/writing-style.md`
- `style/favorite-phrases.md`
- `style/disliked-phrases.md`
- `style/audience-profiles.md`
- `style/leader-signals.md`

Scenarios:

- `scenarios/bid-materials.md`
- `scenarios/weekly-report.md`
- `scenarios/monthly-report.md`
- `scenarios/company-intro.md`
- `scenarios/project-summary.md`
- `scenarios/meeting-minutes.md`

Learning:

- `learning/learning-inbox.md`
- `learning/learning-log.md`
- `learning/correction-history.md`
- `learning/rejected-learning.md`

Templates:

- `templates/bid-capability.md`
- `templates/weekly-report.md`
- `templates/monthly-report.md`
- `templates/company-intro.md`
- `templates/project-summary.md`

## Learning Item

```json
{
  "id": "learn_20260703_100000_001",
  "type": "preference",
  "status": "pending",
  "source_task": "bid_capability_draft",
  "content": "用户不喜欢'赋能'、'持续优化'这类 AI 味表达。",
  "suggested_target_file": "style/disliked-phrases.md",
  "confidence": "user_feedback",
  "created_at": "2026-07-03T10:00:00+08:00"
}
```

Allowed statuses: `pending`, `accepted`, `rejected`, `superseded`.
