# gstreamer-python-sdk

`gi` 기반 GStreamer 를 **문자열이 아니라 데이터모델과 Enum 으로** 다루는 SDK.

```python
from gstreamer_python_sdk import Pipeline, VideoCaps, VideoFormat, Memory
from gstreamer_python_sdk.elements import VideoTestSrc, NvVidConv, NvV4l2H264Enc, H264Parse, Mp4Mux, FileSink

src = VideoTestSrc(num_buffers=90, pattern=VideoTestSrc.Pattern.BALL)
conv = NvVidConv()
enc = NvV4l2H264Enc(bitrate=4_000_000, preset_level=NvV4l2H264Enc.PresetLevel.FASTPRESET)
parse, mux, sink = H264Parse(), Mp4Mux(), FileSink(location="out.mp4")

pipeline = Pipeline(name="record")
pipeline.add(src, conv, enc, parse, mux, sink)
pipeline.link(
    src,
    VideoCaps(format=VideoFormat.I420, width=1280, height=720, framerate=30),
    conv,
    # nvvidconv 출력을 NVMM 으로 — 중간에 끼운 caps 는 capsfilter 로 자동 삽입된다
    VideoCaps(format=VideoFormat.NV12, width=1280, height=720, memory=Memory.NVMM),
    enc,
    parse,
    mux,
    sink,
)

with pipeline:
    pipeline.wait_eos()
```

gst-launch 문자열 방식도 그대로 쓸 수 있습니다: `Pipeline("videotestsrc ! fakesink")`.

## 왜

`gst-launch` 문자열은 오타·잘못된 값·존재하지 않는 프로퍼티가 실행 중에야
드러납니다. 이 SDK 는 GObject introspection 으로 **설치된 GStreamer 에서 직접**
프로퍼티 타입·범위·enum 값을 읽어 파이프라인을 만들기 전에 검증합니다.

```
videotestsrc.num_buffers: 99999999999 는 최댓값 2147483647 보다 큽니다
videotestsrc.pattern: VideoTestSrcPattern 에 nick '무지개' 이 없습니다.
    가능한 값: ball, bar, black, blink, blue, checkers-1, ... , zone-plate
videotestsrc.num_buffer: 그런 프로퍼티가 없습니다
  혹시 이것들인가요? num_buffers
```

## 요구사항

- **Jetson / JetPack** (또는 GStreamer 가 설치된 Linux)
- **Python 3.10** — 시스템 `gi` 와 같은 버전이어야 합니다 (C 확장이라 ABI 가 맞아야 함)
- **PyGObject** + **GStreamer 1.20 이상**

## 설치

### 1. 시스템 패키지

```bash
sudo apt install -y \
  gstreamer1.0-tools \
  gstreamer1.0-plugins-base \
  gstreamer1.0-plugins-good \
  gstreamer1.0-plugins-bad \
  gstreamer1.0-plugins-ugly \
  gstreamer1.0-libav \
  gstreamer1.0-nice \
  libnice10 \
  python3-gi \
  python3-gst-1.0 \
  python3.10-venv \
  v4l-utils
```

`python3-gst-1.0` 이 핵심입니다. 이 패키지가

- `gir1.2-gstreamer-1.0` (Gst typelib)
- `gir1.2-gst-plugins-base-1.0` (GstVideo / GstAudio / GstApp typelib — `VideoFormat`, `AppSink` 에 필요)
- `gir1.2-glib-2.0`

을 의존성으로 함께 끌어오고, gst-python 오버라이드(`Gst.Fraction`, `Gst.init_check` 등)도 제공합니다. 이것들을 직접 나열할 필요는 없습니다.

Jetson 의 `nvv4l2h264enc`, `nvvidconv`, `nvarguscamerasrc` 같은 하드웨어
엘리먼트는 apt 가 아니라 JetPack 의 `nvidia-l4t-gstreamer` 가 제공합니다.

### 2. 패키지 설치

`gi` 는 pip 으로 설치할 수 없는 시스템 패키지라, venv 를 만들 때 시스템
패키지가 보이도록 해야 합니다.

```bash
python3 -m venv --system-site-packages .venv
.venv/bin/pip install -e .[dev,examples]
```

설치 없이 바로 써 보려면 `PYTHONPATH=.` 로도 동작합니다.

### 3. 확인

```bash
.venv/bin/python -c "import gstreamer_python_sdk as g; print(g.diagnostics())"
.venv/bin/python examples/01_hello.py
```

## 무엇을 해 주는가

| 기능 | 설명 |
|---|---|
| **지연 초기화** | `import` 만으로는 `gi` 도 `Gst.init()` 도 부르지 않습니다. 실제로 쓰는 순간 자동 초기화 (import 44ms) |
| **gi 자동 탐색** | venv 에서 `gi` 를 못 찾으면 시스템 경로를 뒤지되, **현재 인터프리터 ABI 와 맞을 때만** 추가합니다 |
| **프로퍼티 검증** | 이름·타입·범위·enum 선택지를 실행 전에 확인. 오타는 유사 이름을 제안 |
| **Enum 자동 생성** | GObject enum/flags → 진짜 Python `IntEnum` / `IntFlag`. nick 문자열도 그대로 허용 |
| **Caps 데이터모델** | `VideoCaps` / `AudioCaps` / `IntRange` / `Options` / `Memory.NVMM` |
| **타입 스텁** | 설치된 GStreamer 를 introspect 해 `.pyi` 생성 → IDE 자동완성 + mypy |
| **버스 콜백** | `bus.on_error()`, `bus.on_state_changed()` 등. 메인루프 유무 모두 지원 |
| **안전한 종료** | `run_pipeline()` 이 Ctrl+C 에 EOS 를 보내 녹화 파일을 정상 마무리 |
| **프레임 공급** | `FrameSource` — numpy 배열을 appsrc 로. caps 기준 크기 검증 포함 |
| **RTSP 서버** | `RtspServer` — 데이터모델을 launch 문자열로 직렬화해 GstRtspServer 에 전달 |
| **그래프 보기** | `diagram()` (의존성 없음) · `to_dot()` · `save_graph()` (graphviz) |

### 동적 + 정적 하이브리드

이름 있는 클래스는 **64개**를 큐레이션했지만, 런타임은 introspection 기반이라
설치된 **1,387개 전부**를 쓸 수 있습니다.

```python
from gstreamer_python_sdk import Element
from gstreamer_python_sdk.elements import make

box = Element("videobox", top=10, bottom=10)      # 이름만 알면 바로
Compositor = make("Compositor", "compositor")     # 클래스로 승격
```

### 타입 스텁 재생성

`.pyi` 는 **생성한 머신의 GStreamer 설치 상태**를 반영합니다. 다른 머신
(x86 개발 PC ↔ Jetson)에서는 다시 만들어야 정확합니다.

```bash
.venv/bin/gst-sdk-codegen                    # 큐레이션된 것만 (기본)
.venv/bin/gst-sdk-codegen --include compositor,videobox
.venv/bin/gst-sdk-codegen --all              # 설치된 전부 (느리고 큼)
```

## 구조

```
gstreamer_python_sdk/
├── _bootstrap.py     gi 탐색 · require() · init()
├── introspect.py     ElementSpec / PropertySpec / PadSpec — 검증과 코드 생성의 단일 소스
├── enums.py          GObject enum/flags → Python Enum
├── caps.py           Caps 데이터모델
├── element.py        Element 래퍼 (프로퍼티 검증 · to_launch 직렬화)
├── elements/         큐레이션 클래스 + 생성된 __init__.pyi
├── pipeline.py       Pipeline (add / link / 상태 전이 / EOS)
├── bus.py            버스 메시지 콜백
├── mainloop.py       GLib 메인루프 · Ctrl+C 안전 종료
├── frames.py         FrameSource — appsrc 로 프레임 공급
├── rtsp.py           RtspServer
├── graph.py          diagram / to_dot / save_graph
├── codegen.py        .pyi 생성기
└── errors.py         예외 계층
```

## 예제

[examples/](examples/) 에 15개가 있습니다 — 기본 조립부터 Jetson NVENC 인코딩,
tee 분기, 동적 패드, appsink → numpy, Ctrl+C 안전 녹화, appsrc 프레임 공급,
RTSP 서버, 그래프 시각화, USB 카메라 하드웨어 디코딩 + OpenCV 표시까지.

## 검증 상태

Jetson (JetPack, GStreamer 1.20.3, Python 3.10.12, aarch64) 에서 확인했습니다.

- 예제 15개 전부 실행 통과. 06번은 실제 NVENC 하드웨어로 MP4 생성,
  15번은 실제 USB 카메라(C922)를 NVDEC 로 디코딩
- `mypy examples gstreamer_python_sdk` → 30개 파일 오류 0
- 생성된 스텁 ↔ 런타임 대조: 프로퍼티 1,103개 · enum 별칭 119개 · enum 멤버 486개 불일치 0

## 알려진 문제

**이 Jetson 에서 `nvv4l2decoder` 가 H.264 디코딩에 실패합니다** (`Stream format
not found`). rank 가 `primary+11` 로 `avdec_h264`(primary)보다 높아 `decodebin`
이 항상 선택하므로, 하드웨어 디코딩 경로가 통째로 막힙니다. `h264parse` 로
byte-stream 을 넣어 줘도 동일합니다. 우회 방법은
[examples/08_dynamic_pads.py](examples/08_dynamic_pads.py) 의 `autoplug-select`
참고. 인코딩(NVENC)과 MJPEG 디코딩(`nvv4l2decoder mjpeg=true`)은 정상입니다.

**`nvvidconv` 는 시스템 메모리 → 시스템 메모리 변환을 하지 못합니다.** caps 에는
있다고 나오지만 실제로는 `Internal data stream error` 가 납니다. 입력이 NVMM 이면
정상이므로, 카메라 경로에서는 NVMM 버퍼를 만들어 주는 디코더를 앞에 두어야 합니다
([examples/15_camera_opencv.py](examples/15_camera_opencv.py) 에 시험 결과 표가 있습니다).

## 선택적 기능과 추가 패키지

일부 기능은 이 시스템에 없는 패키지를 요구합니다. 없으면 설치 방법을 알려주고
멈출 뿐, SDK 의 나머지 기능에는 영향이 없습니다.

| 기능 | 필요한 것 | 없을 때 |
|---|---|---|
| `RtspServer` | `sudo apt install gir1.2-gst-rtsp-server-1.0 gstreamer1.0-rtsp` | 설치 안내 후 예외. `launch_string()` 으로 문자열 확인은 가능 |
| `save_graph()` | `sudo apt install graphviz` | 설치 안내 후 예외. `diagram()` / `to_dot()` 은 그대로 동작 |
| `FrameSource` 예제 | `numpy` (`python3-numpy` 또는 pip) | `FrameSource` 자체는 bytes 만으로도 동작 |
| 카메라 예제 (15번) | `opencv-python` 또는 `python3-opencv` + V4L2 카메라 | `--no-display` 로 창 없이 프레임만 처리 가능 |

## 아직 없는 것

- `appsink` → numpy 헬퍼 (`FrameSource` 의 반대편. 지금은 [09번 예제](examples/09_appsink_numpy.py) 처럼 직접 처리)
- 단위 테스트 스위트 (검증은 예제 실행으로 대체 중)
