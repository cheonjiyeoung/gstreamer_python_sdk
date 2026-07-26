# 예제

## 준비

`gi` 는 pip 으로 설치할 수 없는 시스템 패키지라, venv 를 만들 때 시스템
패키지가 보이도록 해야 합니다.

```bash
python3 -m venv --system-site-packages .venv
.venv/bin/pip install -e .[examples]      # 09번의 numpy 까지
.venv/bin/python examples/01_hello.py
```

설치 없이 한 번만 돌려보려면 `PYTHONPATH` 로도 됩니다.

```bash
PYTHONPATH=. python3 examples/01_hello.py
```

## 목록

| 예제 | 내용 |
|---|---|
| [01_hello.py](01_hello.py) | 가장 단순한 파이프라인. `add()` / `link()` / `with` 블록 |
| [02_enums_and_properties.py](02_enums_and_properties.py) | 프로퍼티를 속성처럼, 설정값을 Enum 으로. 검증 실패 메시지 |
| [03_caps.py](03_caps.py) | `VideoCaps` / `AudioCaps` / `IntRange` / `Options` / `Memory.NVMM` |
| [04_introspect.py](04_introspect.py) | 엘리먼트 탐색. 큐레이션 밖 엘리먼트 사용법 |
| [05_encode_file.py](05_encode_file.py) | 소프트웨어(x264enc) 인코딩 → MP4 |
| [06_jetson_hw_encode.py](06_jetson_hw_encode.py) | Jetson NVENC 인코딩. NVMM 메모리 caps |
| [07_tee_branch.py](07_tee_branch.py) | `tee` 로 분기. 요청(request) 패드 |
| [08_dynamic_pads.py](08_dynamic_pads.py) | `decodebin` 의 `pad-added`, `autoplug-select` 로 디코더 선택 제어 |
| [09_appsink_numpy.py](09_appsink_numpy.py) | `appsink` 로 프레임을 numpy 배열로 꺼내기 |
| [10_bus_callbacks.py](10_bus_callbacks.py) | 버스 메시지를 콜백으로. 메인루프 없이 `bus.run()` 으로 펌프 |
| [11_mainloop_recording.py](11_mainloop_recording.py) | GLib 메인루프 녹화. **Ctrl+C 로 파일을 안전하게 마무리** |
| [12_appsrc_frames.py](12_appsrc_frames.py) | numpy 로 만든 프레임을 `FrameSource`(appsrc) 로 공급 |
| [13_rtsp_server.py](13_rtsp_server.py) | RTSP 서버. `--dry-run` 으로 launch 문자열만 확인 가능 |
| [14_graph.py](14_graph.py) | `diagram()` / `to_dot()` / `save_graph()` 로 파이프라인 보기 |
| [15_camera_opencv.py](15_camera_opencv.py) | **USB 카메라 → NVDEC 하드웨어 디코딩 → appsink → OpenCV imshow** |

## 이 시스템에서 확인된 것

전부 Jetson (JetPack, GStreamer 1.20.3, Python 3.10.12) 에서 실행하여 통과했습니다.
06번은 실제로 NVENC 하드웨어를 사용해 MP4 를 만듭니다.

13번과 14번은 이 시스템에 없는 패키지를 요구하는 부분이 있습니다 —
13번은 `gir1.2-gst-rtsp-server-1.0`(서버 구동), 14번은 `graphviz`(PNG 렌더링).
둘 다 없으면 설치 안내를 출력하고 나머지는 정상 동작합니다.
15번은 Logitech C922(`/dev/video0`)로 확인했습니다.

### 15번 — Jetson 에서 카메라 하드웨어 가속 경로 찾기

이 Jetson 에서 실제로 시험해 본 결과입니다.

| 경로 | 결과 |
|---|---|
| `v4l2src ! image/jpeg ! nvv4l2decoder mjpeg=true ! nvvidconv ! BGRx` | **동작** — 이걸 씁니다 |
| `v4l2src ! image/jpeg ! nvjpegdec ! fakesink` | 동작 (단독으로는) |
| `... ! nvjpegdec ! nvvidconv ! BGRx` | 실패 — 협상 오류 |
| `v4l2src ! video/x-raw,YUY2 ! nvvidconv ! BGRx` | 실패 — nvvidconv 는 시스템→시스템 변환을 못 함 |
| `... YUY2 ! nvvidconv ! NVMM,NV12 ! nvvidconv ! BGRx` | 실패 |

즉 **카메라를 MJPEG 로 받아 `nvv4l2decoder mjpeg=true` 로 디코딩**하는 것이
유일하게 동작하는 하드웨어 경로입니다. (`nvv4l2decoder` 는 H.264 는 실패하지만
MJPEG 는 정상입니다 — 08번 항목 참고.)

720p 300 프레임 실측: 하드웨어 27.9 fps / CPU 2.87초, 소프트웨어 23.7 fps / CPU 3.77초.
소프트웨어 경로는 30fps 를 따라가지 못합니다.

### 11번 — Ctrl+C 로 왜 안전해지는가

녹화 중 프로세스가 그냥 죽으면 mp4mux 가 moov atom 을 쓰지 못해 파일이
재생 불가능해집니다. 실제로 측정한 결과입니다.

| 종료 방법 | 결과 |
|---|---|
| `kill -9` (EOS 없음) | **0 bytes, 재생 불가** |
| `kill -INT` (`run_pipeline` 의 graceful EOS) | 66,543 bytes, `Duration 0:00:03.76` 정상 |

`run_pipeline()` 은 SIGINT/SIGTERM 을 받으면 즉시 죽지 않고 EOS 를 보내
mux 가 헤더를 쓸 때까지 기다립니다. 한 번 더 누르면 즉시 중단합니다.

### 08번 — Jetson 하드웨어 디코더 주의

이 Jetson 에서는 `nvv4l2decoder`(rank primary+11)가 `avdec_h264`(primary)보다
우선순위가 높아 `decodebin` 이 항상 선택하는데, 정작 H.264 디코딩에 실패합니다
(`Stream format not found`). `h264parse` 로 byte-stream 을 넣어줘도 마찬가지입니다.
08번은 `autoplug-select` 시그널로 그 팩토리를 건너뛰게 해서 우회합니다.
하드웨어 디코딩이 정상인 환경이라면 `SKIP_DECODERS` 를 비우면 됩니다.

## 타입 검사

예제와 SDK 모두 mypy 를 통과합니다. 설정은 `pyproject.toml` 의 `[tool.mypy]` 에 있습니다.

```bash
.venv/bin/pip install -e .[dev]
.venv/bin/mypy examples gstreamer_python_sdk
```

02번의 두 줄에는 `# type: ignore` 가 붙어 있는데, 일부러 넣은 잘못된 코드를
mypy 가 정확히 잡아내기 때문입니다. 오타와 타입 불일치는 실행 전에 mypy 가,
범위 초과와 잘못된 enum nick 값은 실행 시점에 SDK 가 잡습니다.

IDE 자동완성이 이상하면 스텁을 다시 만드세요 — 스텁은 **생성한 머신의
GStreamer 설치 상태**를 반영합니다.

```bash
.venv/bin/gst-sdk-codegen          # 또는 python -m gstreamer_python_sdk.codegen
```
