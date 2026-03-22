#!/bin/bash

# 每日 AI 晨報自動產生腳本
# 執行時間：每天 8:00

cd /home/node/.openclaw/workspace

# 獲取今天的日期
TODAY=$(date +%Y-%m-%d)

echo "=== 開始產生晨報: $TODAY ==="

# 執行 Python 腳本產生晨報
python3 /home/node/.openclaw/workspace/scripts/generate_morning_report.py

echo "=== 晨報產生完成 ==="
