# mpy-webota-demo — mpy-webota 를 쓰는 가장 작은 앱.
#
# 런처(main.py, webota)가 `import app; app.main()` 으로 부른다. 앱은 할 일만 하면 된다:
#   - :80 에 한 쪽짜리 페이지(판·가동 시간)를 띄우고
#   - 온보드 LED 가 있으면 천천히 깜빡인다.
# 원격 배포·패키지 설치·롤백은 전부 webota(:8266)가 맡는다.
import socket
import time
import _thread

VERSION = "0.1.1"
LED_PIN = 2               # 보드마다 다르다 — 없으면 조용히 건너뛴다

_t0 = time.time()


def _page():
    up = int(time.time() - _t0)
    return ("<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width'>"
            "<title>webota demo</title><body style='font:16px system-ui;padding:16px'>"
            "<h1>mpy-webota-demo v%s</h1><p>가동 %d초</p>"
            "<p>설치 화면: <a href='' onclick=\"location.port=8266;return false\">:8266</a></p>"
            % (VERSION, up))


def _web():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 80))
    s.listen(2)
    while True:
        c, _ = s.accept()
        try:
            c.settimeout(5)
            c.recv(512)
            body = _page().encode()
            c.send(b"HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n"
                   b"Content-Length: %d\r\n\r\n" % len(body))
            c.send(body)
        except OSError:
            pass
        finally:
            c.close()


def main():
    print("[demo] v%s 시작" % VERSION)
    try:
        _thread.start_new_thread(_web, ())
    except Exception as e:
        print("[demo] 웹 실패: %r" % e)
    led = None
    try:
        from machine import Pin
        led = Pin(LED_PIN, Pin.OUT)
    except Exception:
        pass
    on = False
    while True:
        if led is not None:
            on = not on
            led.value(on)
        time.sleep(1)
