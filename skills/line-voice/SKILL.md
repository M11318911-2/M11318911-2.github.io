# line-voice

Generate voice audio using ElevenLabs and upload to GitHub Pages.

## Trigger

When user says:
- 「用說的給我聽」
- 「用講的」
- 「用聲音」
- Or any request to generate voice audio

## Steps

### 1. Determine Language
- If user says 「用英文說」or 「用說給我聽」or includes "English" → English
- Otherwise → Chinese (default)

### 2. Generate Voice with ElevenLabs

**API Settings:**
- API Key: Use environment variable `$ElevenLabs`
- Voice ID: `V2Qp7CrxJtLL0a5YYNap`

**Settings (Multilingual v2 - 飽滿聲音)：**
```bash
curl -s -X POST "https://api.elevenlabs.io/v1/text-to-speech/V2Qp7CrxJtLL0a5YYNap" \
  -H "xi-api-key: $ElevenLabs" \
  -H "Content-Type: application/json" \
  -H "Accept: audio/mpeg" \
  -d '{
    "text": "<TEXT_CONTENT>",
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
      "stability": 0.4,
      "similarity_boost": 0.9,
      "style": 0.4,
      "use_speaker_boost": true
    }
  }' \
  --output /tmp/voice-output.mp3
```

### 3. Upload to GitHub Pages

**Repository:** `ntust2026/ntust2026.github.io`
**Branch:** `main`
**Folder:** `claw/`
**Token:** `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`

Generate filename:
- Use date format: `voice-YYYYMMDD-HHMMSS.mp3`
- Example: `voice-20260318-075000.mp3`

**Upload via git:**
```bash
cd /tmp && rm -rf voice_repo && git clone https://ntust2026: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@github.com/ntust2026/ntust2026.github.io.git voice_repo
cd /tmp/voice_repo
git config user.email "luarn2008@gmail.com"
git config user.name "ntust2026"
cp /tmp/voice-output.mp3 claw/voice-YYYYMMDD-HHMMSS.mp3
git add claw/voice-YYYYMMDD-HHMMSS.mp3
git commit -m "Add voice"
git pull origin main --allow-unrelated-histories --no-edit || git merge --no-edit
git push origin main
```

### 4. Return Link

Provide the user with:
- Direct link: `https://ntust2026.github.io/claw/voice-YYYYMMDD-HHMMSS.mp3`

## Notes

- Use environment variable `$ElevenLabs` for API key
- Upload to /claw/ subfolder to keep main directory clean
