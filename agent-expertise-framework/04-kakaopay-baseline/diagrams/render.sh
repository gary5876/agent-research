#!/bin/sh
# system-flow.html을 PNG로 캡처한다. 브라우저로 html을 직접 열어 봐도 된다.
cd "$(dirname "$0")"
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=2 --window-size=1600,1260 \
  --screenshot="$(pwd)/system-flow.png" "file://$(pwd)/system-flow.html"
