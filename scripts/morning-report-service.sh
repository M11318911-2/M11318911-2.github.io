#!/bin/bash

# 晨報定時服務 (使用 sleep 輪詢)
# 每分鐘檢查是否應該產生晨報

SCRIPT_DIR="/home/node/.openclaw/workspace/scripts"
LOG_DIR="/home/node/.openclaw/workspace/logs"
REPORT_SCRIPT="$SCRIPT_DIR/daily-morning-report.sh"

mkdir -p "$LOG_DIR"

echo "🌅 晨報定時服務啟動 (每天 8:00)"
echo "Log: $LOG_DIR/morning-service.log"

while true; do
    CURRENT_HOUR=$(date +%H)
    CURRENT_MIN=$(date +%M)
    
    # 每天 8:00 執行
    if [ "$CURRENT_HOUR" = "08" ] && [ "$CURRENT_MIN" = "00" ]; then
        echo "$(date): ⏰ 開始產生晨報..." >> "$LOG_DIR/morning-service.log"
        
        # 執行晨報腳本
        bash "$REPORT_SCRIPT" >> "$LOG_DIR/morning-report.log" 2>&1
        
        TODAY=$(date +%Y-%m-%d)
        LINK="https://ntust2026.github.io/claw/daily-ai-$TODAY.html"
        
        echo "$(date): ✅ 晨報產生完成 - $LINK" >> "$LOG_DIR/morning-service.log"
        
        # 發送連結給用戶 (透過 OpenClaw 訊息)
        # 這裡記錄下載連結，供後續發送
        echo "$LINK" > "$LOG_DIR/latest-report-link.txt"
        
        # 等待 60 秒避免重複執行
        sleep 60
    fi
    
    # 每 60 秒檢查一次
    sleep 60
done
