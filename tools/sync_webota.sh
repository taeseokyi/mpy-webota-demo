#!/usr/bin/env bash
# tools/sync_webota.sh — mpy-webota(원본)의 기기 파일·클라이언트를 이 저장소로 다시 복사한다.
# webota 는 원본(github.com/taeseokyi/mpy-webota)에서 고치고 이걸 돌린다 — 여기서 고치지 않는다.
set -euo pipefail
SRC="${WEBOTA_SRC:-$HOME/work/mpy-webota}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
[ -d "$SRC/device" ] || { echo "원본이 없다: $SRC" >&2; exit 1; }
rm -f "$ROOT"/webota/*
cp "$SRC"/device/*.py "$SRC"/device/*.pem "$SRC"/device/*.html "$ROOT/webota/"
cp "$SRC/client/webota.py" "$ROOT/tools/webota.py"
echo "복사 완료 — mpy-webota $(git -C "$SRC" describe --tags --always) → webota/ · tools/webota.py"
