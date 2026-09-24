# mpy-webota-demo

[mpy-webota](https://github.com/taeseokyi/mpy-webota)(MicroPython 웹 API OTA)를 쓰는 **가장 작은 예제 앱**입니다. 두 가지로 씁니다.
- 새 MicroPython 프로젝트에 mpy-webota를 붙일 때의 본보기
- mpy-webota 설치 화면의 '저장소 더하기'와 '앱 교체'를 시험하는 공개 저장소

앱은 `:80`에 한 쪽짜리 페이지(판, 가동 시간)를 띄우고 온보드 LED(GPIO2)를 깜빡일 뿐입니다. 배포, 설치, 롤백은 전부 webota(`:8266`)가 맡습니다.

## 구조
```
src/app.py              앱 — main() 이 진입점(런처가 부른다)
webota/                 mpy-webota device/ 복사본(boot.py · main.py · webota*.py · webota_ui.html)
tools/webota.py         mpy-webota 클라이언트 복사본
webota.project.json     app_id · version · map(무엇을 기기 어디로)
webota.example.json     기기 설정 /webota.json 예시
```

## 이미 mpy-webota가 설치된 기기에서
설치 화면 `http://<기기>:8266/`에서 저장소 칸에 `taeseokyi/mpy-webota-demo`를 넣고 '더하기'를 누릅니다. 목록에서 판을 고르면, 다른 앱이 돌고 있던 기기라면 **'앱 교체'**가 뜹니다. 새 앱이 90초를 버티지 못하면 원래 앱으로 자동 롤백됩니다. 원래 앱으로 돌아가려면 그 앱의 저장소를 골라 다시 '앱 교체'를 누르면 됩니다.

## 새 기기에 처음 설치 (USB 한 번)
```bash
python3 tools/webota.py --host <기기IP> token          # ~/.config/webota/<기기IP>.token
# webota.example.json 을 webota.json 으로 복사해 token · WiFi(wifi_file 또는 "wifi":{ssid,pass}) 를 채운다
mpremote fs cp webota/* src/app.py webota.json : + reset
python3 tools/webota.py --host <기기IP> status
```

## 판 올리기와 릴리스
```bash
# webota.project.json 의 version 과 src/app.py 의 VERSION 을 올리고 커밋
git tag -a v0.2.0 -m v0.2.0 && git push origin main v0.2.0
python3 tools/webota.py pack --out dist        # dist/webota-demo-v0.2.0.wpk
gh release create v0.2.0 dist/webota-demo-v0.2.0.wpk --title "v0.2.0"
```
패키지 파일 이름은 `<app_id>-v<판>….wpk` 규약을 따릅니다. 설치 화면이 이 이름으로 앱을 알아봅니다.

## 개발 중 (WSL에서 원격으로)
```bash
python3 tools/webota.py --host <기기IP> deploy        # map 대로 바뀐 파일만 → 재부팅 → 확인
python3 tools/webota.py --host <기기IP> put src/app.py /app.py   # 파일 하나(수동 변경으로 표시됨)
```
