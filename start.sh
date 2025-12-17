#!/usr/bin/env bash
set -euo pipefail

LOCK_FILE="/tmp/LoadReports_job.lock"
VPN_CONFIG="myvpn9"
VPN_SESSION_ID=""

# --- 1. 定义退出清理函数 ---
cleanup() {
    if [ -n "$VPN_SESSION_ID" ]; then
        echo "Executing cleanup: Disconnecting VPN session: $VPN_SESSION_ID"
        /usr/bin/openvpn3 session-manage --session-path "$VPN_SESSION_ID" --disconnect || true
    fi
}

# --- 2. 注册 trap ---
# 无论脚本是成功退出还是因错误退出 (EXIT)，都会执行 cleanup 函数
trap cleanup EXIT

# Acquire lock (exclusive, non-blocking)
exec 200>"$LOCK_FILE"
if ! flock -n 200; then
    echo "Another instance is already running. Exit."
    exit 1
fi

/usr/bin/openvpn3 session-start --config "$VPN_CONFIG" --background
sleep 5

# Capture session id
VPN_SESSION_ID=$(
  /usr/bin/openvpn3 sessions-list | awk '/Path:/ {print $2}'
)

echo $VPN_SESSION_ID

if [ -z "$VPN_SESSION_ID" ]; then
    echo "ERROR: Could not determine VPN session ID"
    /usr/bin/openvpn3 session-manage --config myvpn9 --disconnect
    exit 1
fi

echo "VPN started with session: $VPN_SESSION_ID"

# Activate virtual environment
source venv/bin/activate

# Get yesterday date (Mac/Linux compatible)
get_yesterday() {
    if date -d "yesterday" "+%Y-%m-%d" >/dev/null 2>&1; then
        date -d "yesterday" "+%Y-%m-%d"
    else
        date -v -1d "+%Y-%m-%d"
    fi
}

current_day=$(get_yesterday)

python3 -m src.main --start "$current_day" --end "$current_day"