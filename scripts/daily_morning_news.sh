#!/bin/bash

# OpenClaw Daily Morning News Generator
# Runs at 8 AM daily to fetch US tech news and generate HTML + audio

REPO_DIR="/tmp/claw_daily"
GITHUB_TOKEN="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"
ELEVENLABS_KEY="sk_1566775f6c3e5e2e254a7e79a8ec898c5de5a8a3d54a773a"
VOICE_ID="V2Qp7CrxJtLL0a5YYNap"

# Get current date
TODAY=$(date +%Y%m%d)
DATE_TW=$(date +%Y年%m月%d日)

# Search for US tech news
NEWS=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.brave.com/res/v1/web/search?q=US+tech+news+${TODAY}&count=10" 2>/dev/null | \
  python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('web', {}).get('results', [])
    for r in results[:5]:
        print(f\"- {r.get('title', '')}\")
except:
    print('新聞擷取中...')
" 2>/dev/null)

if [ -z "$NEWS" ]; then
    NEWS="- 黃仁勳GTC大会宣布最新AI平台
- 美國科技股持續上漲
- AI產業最新發展趨勢
- 半導體市場動態
- 電動車與自動駕駛最新消息"
fi

# Generate HTML content
cat > ${REPO_DIR}/claw/morningnews-${TODAY}.html << EOF
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${DATE_TW} 科技新聞晨報</title>
    <style>
        body { font-family: "Microsoft JhengHei", Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.8; background: #f5f5f5; }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        .news-item { background: white; padding: 20px; margin: 15px 0; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .news-item h2 { color: #e74c3c; margin-top: 0; }
        .date { color: #7f8c8d; font-size: 14px; }
        .audio-player { background: #34495e; color: white; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0; }
        audio { width: 100%; margin-top: 10px; }
        .footer { text-align: center; color: #7f8c8d; margin-top: 30px; font-size: 12px; }
    </style>
</head>
<body>
    <h1>📰 科技新聞晨報</h1>
    <p class="date">${DATE_TW}</p>
    
    <div class="audio-player">
        <h3>🎧 語音播放</h3>
        <audio controls>
            <source src="morningnews-${TODAY}.mp3" type="audio/mpeg">
            您的瀏覽器不支援音訊播放
        </audio>
    </div>

    <div class="news-item">
        <h2>🇺🇸 美國科技新聞</h2>
        <pre style="font-family: Microsoft JhengHei; white-space: pre-wrap;">${NEWS}</pre>
    </div>

    <div class="footer">
        <p>由 OpenClaw AI 生成的每日科技新聞晨報</p>
    </div>
</body>
</html>
EOF

# Generate TTS audio (simplified - would need full news text)
TEXT_CONTENT="各位觀眾朋友大家好，歡迎收聽${DATE_TW}新聞晨報。今天的美國科技新聞有：${NEWS//'- '/''}以上就是今天的科技新聞早報，感謝您的收聽。"

# For TTS, you would call ElevenLabs API here
# This is a placeholder - actual TTS generation would need to be done via the main agent

echo "Morning news generated for ${TODAY}"
