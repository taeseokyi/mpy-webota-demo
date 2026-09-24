# mpy-webota-demo

[mpy-webota](https://github.com/taeseokyi/mpy-webota)를 쓰는 **가장 작은 예제 앱**입니다. mpy-webota는 MicroPython용 서명 패키지 설치 모듈입니다. 이 저장소는 두 가지로 씁니다.
- 새 MicroPython 프로젝트에 mpy-webota를 붙일 때의 본보기
- mpy-webota 설치 화면의 설치, 앱 교체, GitHub 확인을 시험하는 공개 저장소

앱은 `:80`에 한 쪽짜리 페이지(판, 가동 시간)를 띄우고 온보드 LED(GPIO2)를 깜빡일 뿐입니다. 설치, 롤백, WiFi는 전부 webota(`:8266`)가 맡습니다.

## 구조
```
src/app.py              앱 — main() 이 진입점(런처가 부른다)
webota/                 mpy-webota device/ 복사본(boot.py · main.py · webota*.py · CA · 설치 화면)
tools/webota.py         mpy-webota 클라이언트 복사본
tools/sync_webota.sh    위 두 복사본을 원본에서 다시 가져온다(여기서 고치지 않는다)
webota.project.json     app_id · version · map · data/settings 선언 · device(기기 설정의 원천)
```

## 보안 (mpy-webota 1.x)
- 기기는 **서명된 패키지만** 설치합니다. 믿는 공개키는 `webota.project.json`의 `device.pkg_keys`(`3a1f670f18a68b14`)이고, USB로만 심습니다.
- 기기를 바꾸는 작업(설치, 정리, 공유기 쪽 WiFi 변경)은 **매번 GitHub 승인**을 받습니다. 허용 계정은 `device.github_auth.owners`입니다.
- 서명 없는 옛 판(v0.x)은 1.x 기기에 설치되지 않습니다.

## 내 기기에 설치 (USB 한 번)
```bash
git clone https://github.com/taeseokyi/mpy-webota-demo && cd mpy-webota-demo
pip install mpremote
python3 tools/webota.py usb-install --port COM5 --github-owner <내 GitHub 계정>
```
- webota와 기기 설정만 올라갑니다. 기기 설정에는 이 저장소의 공개키, 출처, 새로 만든 내 기기 토큰, GitHub 확인이 들어갑니다. **앱은 올리지 않습니다.**
- `--github-owner`: 설치와 정리를 승인할 **내** GitHub 계정입니다. 빼면 저장소 작성자(`taeseokyi`)만 승인할 수 있습니다. `--no-github-auth`를 주면 GitHub 확인 없이 기기 토큰만 씁니다.
- 기기가 설정용 AP(`webota-demo-setup` / `webota1234`)를 올립니다. 휴대폰으로 붙어 `http://192.168.4.1:8266/`에서 WiFi를 정합니다.
- 공유기에 붙은 뒤 `http://<기기>:8266/`에서 토큰 칸에 내 토큰을 넣고 '저장'합니다. 토큰은 `~/.config/webota/…token`에 있습니다. 그다음 판을 골라 '설치'하면 GitHub 확인 창이 뜨고, 승인하면 설치됩니다. 첫 설치가 이 앱을 받아들입니다.

## 다른 앱이 돌고 있는 mpy-webota 기기에서
출처는 USB로 정한 것만 쓰므로, 이 저장소의 판을 설치하려면 이 저장소에서 `usb-install`을 한 번 합니다(위와 같음). 그 기기는 이 저장소의 공개키를 믿게 됩니다.

## 판 올리기와 릴리스 (저장소 작성자)
```bash
# webota.project.json 의 version 과 src/app.py 의 VERSION 을 올리고 커밋
git tag -a v1.0.1 -m v1.0.1 && git push origin main v1.0.1
python3 tools/webota.py pack --out dist        # 서명 암호를 묻는다 → dist/webota-demo-v1.0.1.wpk
gh release create v1.0.1 dist/webota-demo-v1.0.1.wpk --title "v1.0.1"
```
- 패키지 파일 이름은 `<app_id>-v<판>….wpk` 규약을 따릅니다. 설치 화면이 이 이름으로 앱을 알아봅니다.
- 서명 키는 `python3 tools/webota.py signing-key init`으로 한 번 만들고, 공개키는 `signing-key publish`로 `webota.project.json`에 넣습니다.
- webota를 새 판으로 바꾸려면 `./tools/sync_webota.sh`를 돌리고 판을 올립니다.
