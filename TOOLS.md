# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### GitHub

- Username: ntust2026
- Token: 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

### TTS (ElevenLabs)

- API Key: <your-api-key>
- Voice ID (中文/英文): V2Qp7CrxJtLL0a5YYNap
- 說明：
  - 「用說的給我聽」→ 中文
  - 「用英文說給我聽」→ 英文
```

### agent-browser (Vercel Labs)

- 安裝：`npm install -g agent-browser`
- 版本：0.21.4
- 執行：`agent-browser open <url>` → 操作 → `agent-browser close`
- 截圖：`agent-browser screenshot [--full] [--annotate] [path]`
- 快速測試：用 `agent-browser open example.com` 確認可用


## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
