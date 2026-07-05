# Test Prompts

## 1. 投标材料

根据资料库，帮我写一段投标文件里的公司能力说明，200 字以内，正式但不要夸大。

Expected:

- Use company profile and at least one project case.
- Avoid forbidden words: 行业领先、全链路赋能、革命性、全国第一。
- Mark missing certifications, customer names, amounts, patents, or awards.

## 2. 周报

我这周做了客户方案、整理需求、跟进开发进度。帮我写一份周报，给上级看。

Expected:

- Use user role context.
- Output formal and plain-language versions.
- Avoid empty slogans.

## 3. 学习偏好

我不喜欢“持续优化”和“赋能”，以后别这么写。

Expected:

- Create a pending learning item.
- After confirmation, append to `style/disliked-phrases.md`.

## 4. 缺失事实

帮我写我们公司有多少项专利和多少个大型客户。

Expected:

- Do not invent.
- Output missing information and ask the user to provide evidence.

## 5. Trae 使用包

在 Trae 中打开 TRAE_USAGE.md，使用同一份 OL-Memory 生成公司介绍。

Expected:

- Trae reads the same data library.
- Output includes sources, missing facts, risk reminders, and learning candidates.

## 6. 新手教学 / Onboarding

Prompt:

```text
我安装完 Skill 后，是不是只要说“开始启动 OL”？前期怎么录入档案？它能帮我做什么？
```

Expected:

- Explain first start in Chinese and English.
- Use the memorable startup phrase: `开始启动 OL`.
- Ask the required intake questions in chat before opening the UI: name/role, common docs, company intro/scope, one case, forbidden claims, style preferences.
- Explain that the UI is for review and editing after the starter profile is written.
- Explain that daily use happens in the Agent chat box; users can paste new facts, corrections, leader-shared material, or writing requests there.
- List supported office tasks.
- Explain that `127.0.0.1` requires the local UI server and can be restarted with `launch_ui.py`.

## 7. 上级偏好学习 / Leader Signals

Prompt:

```text
上级今天转发了一个短视频，说“客户要的是结果，不是我们的辛苦”。帮我记到 OL-Memory，之后写周报和述职时要参考这个偏好。
```

Expected:

- Store the material as a leader preference signal, not a company fact.
- Update or suggest updates for `knowledge/leader-shared-materials.md`, `style/leader-signals.md`, and `knowledge/leader-talking-points.md`.
- Future weekly report context includes leader-facing emphasis on result, impact, and next steps.
