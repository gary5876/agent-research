#!/bin/sh
# 이 폴더의 흐름도 html을 PNG로 캡처한다. 사용: ./render.sh superpowers-flow [높이]
cd "$(dirname "$0")"
N="${1:-superpowers-flow}"; H="${2:-1400}"
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=2 --window-size=1600,$H \
  --screenshot="$(pwd)/$N.png" "file://$(pwd)/$N.html"
