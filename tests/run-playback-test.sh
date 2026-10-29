#!/bin/sh
# 用真實 Chrome(headless)播放開場影片,檢查蝴蝶結只演一遍。需要 Chrome 與 python3。
# 預設用「支援 Range」的伺服器;加 norange 參數可模擬不支援 Range 的伺服器。
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; PORT=8799
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [ "$1" = norange ]; then (cd "$ROOT" && python3 -m http.server $PORT >/dev/null 2>&1 &) ; else (python3 "$ROOT/tests/rangeserver.py" "$ROOT" $PORT >/dev/null 2>&1 &); fi
sleep 1
"$CHROME" --headless=new --autoplay-policy=no-user-gesture-required --mute-audio --disable-gpu \
  --virtual-time-budget=20000 --dump-dom "http://127.0.0.1:$PORT/tests/playback-test.html" 2>/dev/null | grep -o 'RESULT [PF][A-Z]* [^<]*'
pkill -f "$PORT" 2>/dev/null; true
