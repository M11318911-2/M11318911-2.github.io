import requests
import os

ELEVENLABS_API_KEY = os.environ.get("ElevenLabs")
VOICE_ID = "V2Qp7CrxJtLL0a5YYNap"

ZH_TEXT = """美國晨間科技新聞，我是小小斌，現在為您播報2026年3月23日的最新科技動態。

第一則新聞，網路安全領域。美國執法部門宣布成功搗毀一個已感染全球超過300萬台設備的殭屍網絡，這是近年來規模最大的網路安全執法行動之一。專家警告，消費電子產品、小型企業設備及物聯網系統都可能成為攻擊目標。

第二則新聞，出口管制。美國檢察官起訴三名與超微電腦有關聯的人士，涉嫌透過東南亞路線將先進的輝達AI晶片非法運往中國。案情涉及使用這些晶片組裝的伺服器。此案顯示，AI運算能力已成為地緣政治資產。

第三則新聞，AI程式工具新創公司Cursor即將推出Composer 2，這是一款更高效的人工智慧模型，能處理更複雜的軟體開發任務。該公司自2023年推出以來快速成長，目前每天服務超過100萬名用戶。

第四則新聞，OpenAI宣布收購Python開發工具新創公司Astral，將其團隊整合至Codex計畫中。Codex目前已有超過200萬用戶，是年初的三倍。

第五則新聞，亞馬遜收購了瑞士機器人新創公司Rivr，該公司開發了一款能爬樓梯的四輪配送機器人，專為最後一哩配送設計。

第六則新聞，Pinterest執行長公開呼籲立法禁止16歲以下青少年使用社群媒體平台，指出這對未成年人心理健康有負面影響。

第七則新聞，Apple正式宣布將於2026年推出由人工智慧驅動的全新版本Siri，具備螢幕感知能力。

第八則新聞，美國記憶體大廠美光科技公佈季度財報，營收較去年同期暴增近2倍，公司宣布將大幅增加資本支出以滿足AI需求。

以上是今日的晨間科技新聞，我們下次再會。"""

EN_TEXT = """Good morning! I'm your tech news host, bringing you the latest technology headlines from the United States for March 23rd, 2026.

First up, cybersecurity. U.S. authorities have disrupted botnets that infected over 3 million devices worldwide, marking one of the largest recent cyber enforcement actions. Experts warn that consumer electronics and IoT systems are all potential targets.

Next, export controls. U.S. prosecutors charged three individuals tied to Super Micro Computer in an alleged scheme to divert advanced Nvidia AI chips to China through Southeast Asia. The case highlights how AI compute has become a geopolitical asset.

In AI coding news, startup Cursor is launching Composer 2, a more efficient AI model designed to handle complex software development tasks. The company has grown rapidly, now serving over 1 million daily users.

OpenAI is acquiring Astral, a Python tools startup, bringing the team into its Codex effort. Codex now has over 2 million users, triple the number from the start of the year.

Amazon has acquired Rivr, a Zurich-based robotics startup developing a stair-climbing delivery robot for last-mile logistics.

Pinterest's CEO is calling for legislation to ban social media for users under 16, citing negative mental health impacts on minors.

And Apple has announced an AI-powered Siri redesign set to debut in 2026, featuring on-screen awareness capabilities.

Finally, Micron Technology reported quarterly earnings with revenue nearly doubling year-over-year as AI demand surged, with plans to increase capital spending to over 25 billion dollars.

That's your morning tech briefing. Stay tuned for more updates."""

def generate_audio(text, filename, model):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    data = {
        "text": text,
        "model_id": model,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.2,
            "use_speaker_boost": True
        }
    }
    
    print(f"Generating {filename} with model {model}...")
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"✓ Saved: {filename} ({len(response.content)} bytes)")
        return True
    else:
        print(f"✗ Error: {response.status_code} - {response.text}")
        return False

# Generate Chinese audio
generate_audio(ZH_TEXT, "/home/node/.openclaw/workspace/morning-zh.mp3", "eleven_multilingual_v2")

# Generate English audio  
generate_audio(EN_TEXT, "/home/node/.openclaw/workspace/morning-en.mp3", "eleven_turbo_v2_5")

print("\nAudio generation complete!")
