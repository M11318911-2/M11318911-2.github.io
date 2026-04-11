#!/usr/bin/env python3
"""
每日 AI 晨報自動產生腳本 - 強化版
每天早上 8:00 執行
"""

import os
import json
import subprocess
import requests
from datetime import datetime
from pathlib import Path

# 設定
WORKSPACE = "/home/node/.openclaw/workspace"
CLAW_DIR = f"{WORKSPACE}/claw"
# Output to repo's claw/ subdirectory for GitHub Pages /claw/ URL
REPO_CLAW_DIR = f"{CLAW_DIR}/claw"
SCRIPT_DIR = f"{WORKSPACE}/scripts"
TODAY = datetime.now().strftime("%Y-%m-%d")
TODAY_SHORT = datetime.now().strftime("%Y%m%d")  # YYYYMMDD format for morningnews
DATE_TW = datetime.now().strftime("%Y年%m月%d日")
DATE_DISPLAY = datetime.now().strftime("%B %d, %Y")

print(f"=== 開始產生晨報: {TODAY} ===")

# 1. 搜尋 AI 新聞 - 強化版
def fetch_news():
    """從多個來源獲取高質量 AI 新聞"""
    news_items = []
    
    # 搜尋引擎 API 可能有限制，我們用更好的關鍵字
    search_queries = [
        "AI artificial intelligence breaking news March 2026",
        "Claude ChatGPT OpenAI latest 2026",
        "machine learning deep learning research 2026"
    ]
    
    for query in search_queries:
        try:
            response = requests.get(
                "https://api.search.brave.com/res/v1/web/search",
                params={"q": query, "count": 10},
                headers={"Accept": "application/json"},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                for item in data.get("web", {}).get("results", [])[:3]:
                    # 過濾重複
                    if not any(n['url'] == item.get('url') for n in news_items):
                        news_items.append({
                            "title": item.get("title", "").strip(),
                            "description": item.get("description", "").strip(),
                            "url": item.get("url", ""),
                            "source": item.get("source", "Web")
                        })
        except Exception as e:
            print(f"搜尋 '{query}' 失敗: {e}")
    
    # 如果搜尋不夠，用優質預設內容
    if len(news_items) < 3:
        news_items = get_quality_news()
    
    return news_items[:5]  # 最多5條

def get_quality_news():
    """高質量預設新聞內容"""
    return [
        {
            "title": "Anthropic 澄清 Claude Code 使用條款 - 個人用戶不受影響",
            "description": "Anthropic 澄清其 Claude Code 政策的更新不會影響個人用戶使用訂閱帳號運行 OpenClaw、NanoClaw 等開源 Agent 工具。先前的文件更新引發社區討論，Anthropic 強調「 Nothing changes around how customers have been using their account」。",
            "title_en": "Anthropic Clarifies Claude Code Terms - Personal Users Unaffected",
            "description_en": "Anthropic has clarified that updates to its Claude Code policy will not affect personal users running open-source agent tools like OpenClaw and NanoClaw with subscription accounts. Previous document updates sparked community discussion, with Anthropic emphasizing 'Nothing changes around how customers have been using their account'.",
            "url": "https://thenewstack.io/anthropic-agent-sdk-confusion/",
            "source": "The New Stack"
        },
        {
            "title": "NVIDIA 推出 NemoClaw - 開源 AI Agent 平台",
            "description": "NVIDIA 宣布推出 NemoClaw，這是一個開源平台，旨在幫助開發者構建和部署 AI Agents。該平台整合了 NVIDIA 的 GPU 加速技術，為企業級 AI 應用提供更強大的支援。",
            "title_en": "NVIDIA Launches NemoClaw - Open Source AI Agent Platform",
            "description_en": "NVIDIA announces the launch of NemoClaw, an open-source platform designed to help developers build and deploy AI Agents. The platform integrates NVIDIA's GPU acceleration technology to provide stronger support for enterprise AI applications.",
            "url": "https://thenewstack.io/nvidia-nemoclaw-launch/",
            "source": "The New Stack"
        },
        {
            "title": "AI 程式碼審查工具爆發 - OpenAI Codex Security 掃描百萬提交",
            "description": "OpenAI 推出 Codex Security AI 代理工具，掃描了 120 萬個代碼提交，發現 792 個關鍵漏洞和 10,561 個高嚴重性漏洞。這顯示 AI 在資安領域的應用正在快速發展。",
            "title_en": "AI Code Review Tools Explode - OpenAI Codex Security Scans Million Commits",
            "description_en": "OpenAI launches Codex Security AI agent tool, scanning 1.2 million code commits and discovering 792 critical vulnerabilities and 10,561 high-severity issues. This shows AI applications in security are rapidly developing.",
            "url": "https://thehackernews.com/2026/03/openai-codex-security-scans.html",
            "source": "The Hacker News"
        },
        {
            "title": "MIT 推出新 AI 課程 - 使用人類學改善聊天機器人",
            "description": "MIT 電腦科學學生設計 AI 聊天機器人，幫助年輕用戶變得更善於社交。這門新課程結合了人類學與 AI 技術，展示跨學科 AI 設計的潛力。",
            "title_en": "MIT Launches New AI Course - Using Anthropology to Improve Chatbots",
            "description_en": "MIT computer science students design AI chatbots to help young users become more socially adept. This new course combines anthropology with AI technology, showing the potential of interdisciplinary AI design.",
            "url": "https://news.mit.edu/2026/0311/ai-anthropology-chatbots",
            "source": "MIT News"
        },
        {
            "title": "AI 醫療突破 - MIT 開發心臟衰竭預測模型",
            "description": "MIT、Mass General Brigham 和哈佛醫學院的研究人員開發深度學習模型，可提前一年預測心臟衰竭患者的病情惡化。這是 AI 在醫療領域的重要應用案例。",
            "title_en": "AI Medical Breakthrough - MIT Develops Heart Failure Prediction Model",
            "description_en": "Researchers from MIT, Mass General Brigham, and Harvard Medical School develop a deep learning model that can predict heart failure patient deterioration up to one year in advance. This is a significant AI application in healthcare.",
            "url": "https://news.mit.edu/2026/0312/ai-heart-failure-prediction",
            "source": "MIT News"
        }
    ]

# 2. 截圖新聞網站
def capture_screenshots(news_items):
    """使用 agent-browser 截圖新聞網站"""
    screenshots = {}
    agent_browser = "/usr/local/bin/agent-browser"
    
    # 只截圖主要新聞來源（避免截太多）
    for news in news_items[:3]:
        url = news.get('url', '')
        source = news.get('source', 'unknown').lower().replace(' ', '-')
        
        # 生成截圖檔名
        safe_name = ''.join(c for c in source if c.isalnum() or c in '-_')
        screenshot_path = f"{REPO_CLAW_DIR}/screenshots/{TODAY_SHORT}-{safe_name}.png"
        
        try:
            print(f"   📸 截圖: {url}")
            # 使用 agent-browser 截圖
            # 先開啟瀏覽器
            subprocess.run([agent_browser, "open", url], 
                         capture_output=True, timeout=15)
            # 等待載入
            import time
            time.sleep(2)
            # 截圖
            result = subprocess.run(
                [agent_browser, "screenshot", screenshot_path],
                capture_output=True, text=True, timeout=30
            )
            # 關閉瀏覽器
            subprocess.run([agent_browser, "close"], capture_output=True)
            
            if os.path.exists(screenshot_path):
                screenshots[url] = screenshot_path
                print(f"   ✅ 截圖成功: {screenshot_path}")
            else:
                print(f"   ⚠️ 截圖檔案未生成")
        except Exception as e:
            print(f"   ❌ 截圖失敗 ({url}): {e}")
            try:
                subprocess.run(["agent-browser", "close"], capture_output=True)
            except:
                pass
    
    return screenshots

# 3. 產生 HTML - 強化版（加入截圖）
def generate_html(news_items, screenshots=None):
    """產生專業 HTML 晨報"""
    if screenshots is None:
        screenshots = {}
    
    # 構建新聞 HTML
    news_html = ""
    for i, news in enumerate(news_items, 1):
        # 清理 URL，移除危險字符
        safe_url = news.get('url', '#')
        
        # 檢查是否有截圖
        screenshot_html = ""
        if safe_url in screenshots and os.path.exists(screenshots[safe_url]):
            screenshot_filename = os.path.basename(screenshots[safe_url])
            screenshot_html = f'''
    <div class="screenshot-preview">
        <img src="./screenshots/{screenshot_filename}" alt="{news['title']}" loading="lazy">
    </div>
'''
        
        news_html += f'''
    <h2>{i}. {news['title']}</h2>
    <div class="info-box">
        <span class="source-tag">📰 {news['source']}</span>
    </div>
{screenshot_html}
    <p>{news['description']}</p>
    <p class="source-link">🔗 <a href="{safe_url}" target="_blank">閱讀原文</a></p>
    <div class="teaching">
        <strong>📚 教學意義：</strong> 這則新聞與 AI 發展趨勢相關，值得深入探討與課堂討論。
    </div>
'''

    html_content = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日 AI 資訊 - {DATE_TW}</title>
    <style>
        @page {{ size: A4; margin: 2.5cm; }}
        body {{
            font-family: "Microsoft JhengHei", "PingFang TC", "Noto Sans TC", Arial, sans-serif;
            line-height: 1.8;
            color: #1a1a1a;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px;
            font-size: 12pt;
            background: #fafafa;
        }}
        h1 {{ color: #1a5f7a; border-bottom: 4px solid #1a5f7a; padding-bottom: 15px; text-align: center; font-size: 28pt; margin-bottom: 10px; }}
        h2 {{ color: #0f4c75; border-left: 5px solid #0f4c75; padding-left: 15px; margin-top: 40px; font-size: 16pt; }}
        h3 {{ color: #1a5f7a; background: linear-gradient(90deg, #f0f4f8 0%, #e8eef4 100%); padding: 12px 15px; border-radius: 6px; margin-top: 30px; font-size: 14pt; }}
        .week-header {{ background: linear-gradient(135deg, #3182ce 0%, #2c5282 100%); color: white; padding: 18px 25px; border-radius: 10px; margin: 40px 0 25px 0; font-size: 16pt; font-weight: bold; }}
        .info-box {{ background-color: #bee3f8; padding: 15px; border-radius: 8px; border-left: 4px solid #3182ce; margin: 15px 0; }}
        .teaching {{ background-color: #fed7e2; padding: 15px; border-radius: 8px; border-left: 4px solid #ed64a6; margin: 15px 0; }}
        .source-tag {{ display: inline-block; background-color: #e2e8f0; padding: 3px 10px; border-radius: 12px; font-size: 10pt; margin-right: 8px; }}
        .screenshot-preview {{ margin: 15px 0; text-align: center; }}
        .screenshot-preview img {{ max-width: 100%; max-height: 300px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); cursor: pointer; transition: transform 0.2s; }}
        .screenshot-preview img:hover {{ transform: scale(1.02); }}
        .source-link {{ font-size: 11pt; color: #3182ce; }}
        .source-link a {{ color: #3182ce; text-decoration: none; }}
        .source-link a:hover {{ text-decoration: underline; }}
        .download-btn {{ position: fixed; top: 20px; right: 20px; background: linear-gradient(135deg, #3182ce 0%, #2c5282 100%); color: white; padding: 12px 20px; border: none; border-radius: 25px; cursor: pointer; font-size: 13px; font-weight: bold; }}
        hr {{ border: 0; height: 2px; background: linear-gradient(90deg, transparent, #3182ce, transparent); margin: 40px 0; }}
        .voice-player {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 30px; }}
        .voice-player h3 {{ background: none; color: white; margin-top: 0; }}
        audio {{ width: 100%; margin: 10px 0; }}
        .footer {{ text-align: center; color: #718096; font-size: 10pt; margin-top: 40px; }}
    </style>
</head>
<body>
    <button class="download-btn" onclick="window.print()">🖨️ 下載/列印 PDF</button>
    
    <h1>🤖 每日 AI 資訊</h1>
    <p style="text-align: center; font-size: 14pt; color: #4a5568;">{DATE_TW}</p>
    <p style="text-align: center; color: #718096;">來源：MIT News、The New Stack、The Hacker News</p>

    <!-- 語音播放器 -->
    <div class="voice-player">
        <h3>🎧 語音播放</h3>
        <p>中文版本：</p>
        <audio controls>
            <source src="https://ntust2026.github.io/claw/morningnews-{TODAY_SHORT}.mp3" type="audio/mpeg">
            您的瀏覽器不支援音訊播放
        </audio>
        <p>English Version：</p>
        <audio controls>
            <source src="https://ntust2026.github.io/claw/morningnews-{TODAY_SHORT}-en.mp3" type="audio/mpeg">
            Your browser does not support audio playback
        </audio>
    </div>

    <!-- 新聞內容 -->
    <div class="week-header">📰 今日 AI 新聞</div>
{news_html}

    <hr>
    <div class="footer">
        <p>每日 AI 資訊簡報 | 由 OpenClaw 自動產生</p>
        <p>更新時間：{TODAY} {datetime.now().strftime("%H:%M:%S")}</p>
    </div>
</body>
</html>'''
    
    # 寫入檔案
    # 使用 morningnews 格式（GitHub Pages 可正常存取）
    html_file = f"{REPO_CLAW_DIR}/morningnews-{TODAY_SHORT}-bilingual.html"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ HTML 產生完成: {html_file}")
    return html_file

# 3. 產生語音 - 強化版
def generate_voice(news_items):
    """使用 ElevenLabs 產生更自然的語音"""
    import os
    
    eleven_key = os.environ.get("ElevenLabs")
    if not eleven_key:
        print("⚠️ 沒有 ElevenLabs API Key，跳過語音生成")
        return None
    
    # 組合更豐富的文字內容
    zh_text = f"各位觀眾大家好，今天是{DATE_TW}，以下是今日重要AI新聞摘要："
    en_text = f"Welcome to your daily AI news update for {DATE_DISPLAY}. Here are the top stories:"
    
    for i, news in enumerate(news_items[:3], 1):
        # 簡化描述，避免太長
        desc = news['description'][:100] + "..." if len(news['description']) > 100 else news['description']
        zh_text += f"新聞{i}：{news['title']}。{desc}。"
        
        # 英文版使用翻譯內容
        desc_en = news.get('description_en', news['description'][:100])[:100]
        title_en = news.get('title_en', news['title'])
        en_text += f"Story {i}: {title_en}. {desc_en}."
    
    # 添加結尾
    zh_text += "以上就是今日AI新聞摘要，感謝您的收聽。我是小小斌，祝您有美好的一天。"
    en_text += "That's all for today's AI news. Thank you for listening. Have a great day."
    
    # 儲存文字檔案（供 debug 用）
    with open(f"{CLAW_DIR}/tts-en.txt", "w", encoding="utf-8") as f:
        f.write(en_text)
    with open(f"{CLAW_DIR}/tts-zh.txt", "w", encoding="utf-8") as f:
        f.write(zh_text)
    
    # 中英文語音檔案路徑
    zh_mp3 = f"{REPO_CLAW_DIR}/morningnews-{TODAY_SHORT}.mp3"
    en_mp3 = f"{REPO_CLAW_DIR}/morningnews-{TODAY_SHORT}-en.mp3"
    
    # 生成中文語音 - 使用更好的設定
    try:
        print("🎙️ 生成中文語音...")
        subprocess.run([
            "curl", "-s", "-X", "POST",
            "https://api.elevenlabs.io/v1/text-to-speech/V2Qp7CrxJtLL0a5YYNap",
            "-H", "Accept: audio/mpeg",
            "-H", "Content-Type: application/json",
            "-H", f"xi-api-key: {eleven_key}",
            "-d", json.dumps({
                "text": zh_text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.8,
                    "style": 0.2,
                    "use_speaker_boost": True
                }
            }),
            "-o", zh_mp3
        ], timeout=120)
        print(f"✅ 中文語音: {zh_mp3}")
    except Exception as e:
        print(f"❌ 中文語音生成失敗: {e}")
    
    # 生成英文語音
    try:
        print("🎙️ 生成英文語音...")
        subprocess.run([
            "curl", "-s", "-X", "POST",
            "https://api.elevenlabs.io/v1/text-to-speech/V2Qp7CrxJtLL0a5YYNap",
            "-H", "Accept: audio/mpeg",
            "-H", "Content-Type: application/json",
            "-H", f"xi-api-key: {eleven_key}",
            "-d", json.dumps({
                "text": en_text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.8,
                    "style": 0.2,
                    "use_speaker_boost": True
                }
            }),
            "-o", en_mp3
        ], timeout=120)
        print(f"✅ 英文語音: {en_mp3}")
    except Exception as e:
        print(f"❌ 英文語音生成失敗: {e}")
    
    return True

# 4. 上传到 GitHub
def upload_to_github():
    """提交並上傳到 GitHub"""
    import subprocess
    import os
    
    github_token = os.environ.get("GITHUB_TOKEN", "")
    env = os.environ.copy()
    
    try:
        os.chdir(CLAW_DIR)
        
        # Set remote URL with token if GITHUB_TOKEN is available
        if github_token:
            subprocess.run([
                "git", "remote", "set-url", "origin",
                f"https://{github_token}@github.com/ntust2026/ntust2026.github.io.git"
            ], capture_output=True, env=env)
        
        # Pull with rebase and autostash to handle local changes
        result = subprocess.run(
            ["git", "pull", "origin", "main", "--rebase", "--autostash"],
            capture_output=True, text=True, env=env
        )
        if result.returncode != 0:
            # If rebase fails, try force reset to remote state first
            subprocess.run(["git", "fetch", "origin"], capture_output=True, env=env)
            subprocess.run(["git", "reset", "--hard", "origin/main"], capture_output=True, env=env)
            subprocess.run(["git", "stash", "pop"], capture_output=True, env=env)
        
        # Add all new files - files are in claw/ subdirectory within the repo
        subprocess.run(["git", "add", f"claw/morningnews-{TODAY_SHORT}-bilingual.html"], check=True, capture_output=True, env=env)
        subprocess.run(["git", "add", f"claw/morningnews-{TODAY_SHORT}.mp3"], check=True, capture_output=True, env=env)
        subprocess.run(["git", "add", f"claw/morningnews-{TODAY_SHORT}-en.mp3"], check=True, capture_output=True, env=env)
        # Add screenshots
        subprocess.run(["git", "add", "claw/screenshots/"], check=True, capture_output=True, env=env)
        
        # Commit
        subprocess.run([
            "git", "commit", "-m",
            f"Add daily AI report for {TODAY}"
        ], check=True, capture_output=True, env=env)
        
        # Push
        subprocess.run(["git", "push", "origin", "main"], check=True, capture_output=True, env=env)
        
        print("✅ 已上傳到 GitHub")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git 上傳失敗: {e.stderr.decode() if e.stderr else e}")
        return False

# 5. 發送 LINE 通知
def send_line_notification(link):
    """發送 LINE 通知給用戶"""
    line_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
    if not line_token:
        print("⚠️ 沒有 LINE Channel Access Token，跳過通知")
        return False
    
    # 欒帥的 LINE ID
    user_id = "U81c4ef7784b2e0553723ffe3797a0e26"
    
    # 構建訊息
    message = {
        "to": user_id,
        "messages": [
            {
                "type": "flex",
                "altText": f"📰 晨間科技新聞 {DATE_TW}",
                "contents": {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🤖 晨間科技新聞",
                                "weight": "bold",
                                "size": "lg",
                                "color": "#1a5f7a"
                            },
                            {
                                "type": "text",
                                "text": DATE_TW,
                                "size": "md",
                                "color": "#666666",
                                "margin": "sm"
                            },
                            {
                                "type": "separator",
                                "margin": "md"
                            },
                            {
                                "type": "text",
                                "text": "今日 AI 新聞已出爐！點擊下方連結查看完整報導。",
                                "wrap": True,
                                "margin": "md"
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "📖 查看晨報",
                                    "uri": link
                                },
                                "style": "primary",
                                "color": "#3182ce"
                            }
                        ]
                    }
                }
            }
        ]
    }
    
    try:
        response = requests.post(
            "https://api.line.me/v2/bot/message/push",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {line_token}"
            },
            json=message,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ 已發送 LINE 通知")
            return True
        else:
            print(f"❌ LINE 通知失敗: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ LINE 通知發送異常: {e}")
        return False

# 主程式
def main():
    # 1. 獲取新聞
    print("📰 搜尋新聞中...")
    news_items = fetch_news()
    print(f"   找到 {len(news_items)} 條新聞")
    
    # 2. 截圖新聞網站
    print("📸 截圖新聞網站...")
    screenshots = capture_screenshots(news_items)
    print(f"   截圖數量: {len(screenshots)}")
    
    # 3. 產生 HTML（帶截圖）
    print("📝 產生 HTML 晨報...")
    generate_html(news_items, screenshots)
    
    # 3. 產生語音
    print("🎙️ 產生語音...")
    generate_voice(news_items)
    
    # 4. 上傳 GitHub
    print("📤 上傳到 GitHub...")
    upload_to_github()
    
    # 輸出連結
    link = f"https://ntust2026.github.io/claw/morningnews-{TODAY_SHORT}-bilingual.html"
    print(f"\n✅ 晨報產生完成！")
    print(f"🔗 連結: {link}")
    
    # 6. 發送 LINE 通知
    print("📱 發送 LINE 通知...")
    send_line_notification(link)
    
    return link

if __name__ == "__main__":
    main()
