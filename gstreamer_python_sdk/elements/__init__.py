"""이름 있는 엘리먼트 클래스.

클래스는 introspection 결과로부터 접근 시점에 만들어진다. 정적 자동완성은
같은 디렉터리의 `__init__.pyi` 가 담당하며, 다음 명령으로 재생성한다:

    python -m gstreamer_python_sdk.codegen

여기 없는 엘리먼트도 얼마든지 쓸 수 있다 — 1089개 전부가 동적으로 지원된다:

    from gstreamer_python_sdk import Element
    Element("compositor", background="black")
"""

from __future__ import annotations

import re
import threading
from typing import Any

from ..element import Element
from ..introspect import inspect_element

__all__ = ["Element", "CURATED", "make", "available"]

#: 이름 있는 클래스로 제공할 엘리먼트. {클래스 이름: 팩토리 이름}
#: 여기 있다고 반드시 설치되어 있는 건 아니다(Jetson 전용 nv* 등).
CURATED: dict[str, str] = {
    # --- 소스 -------------------------------------------------------------
    "VideoTestSrc": "videotestsrc",
    "AudioTestSrc": "audiotestsrc",
    "FileSrc": "filesrc",
    "V4l2Src": "v4l2src",
    "RtspSrc": "rtspsrc",
    "UdpSrc": "udpsrc",
    "SoupHttpSrc": "souphttpsrc",
    "AppSrc": "appsrc",
    "UriDecodeBin": "uridecodebin",
    "DecodeBin": "decodebin",
    "PlayBin": "playbin",
    "NvArgusCameraSrc": "nvarguscamerasrc",  # Jetson CSI 카메라
    "NvV4l2CameraSrc": "nvv4l2camerasrc",  # Jetson USB/YUV 카메라
    # --- 변환 / 필터 -------------------------------------------------------
    "CapsFilter": "capsfilter",
    "VideoConvert": "videoconvert",
    "VideoScale": "videoscale",
    "VideoRate": "videorate",
    "VideoFlip": "videoflip",
    "VideoCrop": "videocrop",
    "AudioConvert": "audioconvert",
    "AudioResample": "audioresample",
    "Queue": "queue",
    "Queue2": "queue2",
    "Tee": "tee",
    "Identity": "identity",
    "Valve": "valve",
    "NvVidConv": "nvvidconv",  # Jetson 하드웨어 변환/스케일
    "NvVideoConvert": "nvvideoconvert",  # DeepStream
    # --- 인코더 -----------------------------------------------------------
    "X264Enc": "x264enc",
    "X265Enc": "x265enc",
    "JpegEnc": "jpegenc",
    "VpxEnc": "vp8enc",
    "NvV4l2H264Enc": "nvv4l2h264enc",
    "NvV4l2H265Enc": "nvv4l2h265enc",
    "NvV4l2Vp9Enc": "nvv4l2vp9enc",
    "NvV4l2Av1Enc": "nvv4l2av1enc",
    "NvJpegEnc": "nvjpegenc",
    # --- 디코더 / 파서 -----------------------------------------------------
    "AvDecH264": "avdec_h264",
    "AvDecH265": "avdec_h265",
    "JpegDec": "jpegdec",
    "H264Parse": "h264parse",
    "H265Parse": "h265parse",
    "NvV4l2Decoder": "nvv4l2decoder",
    "NvJpegDec": "nvjpegdec",
    # --- 네트워크 / 컨테이너 -----------------------------------------------
    "RtpH264Pay": "rtph264pay",
    "RtpH264Depay": "rtph264depay",
    "RtpH265Pay": "rtph265pay",
    "RtpJitterBuffer": "rtpjitterbuffer",
    "Mp4Mux": "mp4mux",
    "QtMux": "qtmux",
    "MatroskaMux": "matroskamux",
    "MpegTsMux": "mpegtsmux",
    "FlvMux": "flvmux",
    # --- 싱크 -------------------------------------------------------------
    "FakeSink": "fakesink",
    "FileSink": "filesink",
    "AppSink": "appsink",
    "UdpSink": "udpsink",
    "AutoVideoSink": "autovideosink",
    "AutoAudioSink": "autoaudiosink",
    "XvImageSink": "xvimagesink",
    "GlImageSink": "glimagesink",
    "Nv3dSink": "nv3dsink",
    "NvEglGlesSink": "nveglglessink",
    "NvDrmVideoSink": "nvdrmvideosink",
}

_lock = threading.RLock()


def _pascal(text: str) -> str:
    return "".join(part.capitalize() for part in re.split(r"[^0-9a-zA-Z]+", text) if part)


def _nested_enums(class_name: str, spec) -> dict[str, Any]:
    """enum 프로퍼티의 Enum 을 클래스 속성으로 붙인다.

    VideoTestSrc.pattern 의 GstVideoTestSrcPattern 은 `VideoTestSrc.Pattern`
    으로 접근할 수 있게 만든다.
    """
    attrs: dict[str, Any] = {}
    for prop in spec.properties.values():
        enum_type = prop.enum_type
        if enum_type is None:
            continue
        short = enum_type.__name__
        if short.startswith(class_name) and len(short) > len(class_name):
            short = short[len(class_name) :]
        else:
            short = _pascal(prop.python_name)
        if short in attrs and attrs[short] is not enum_type:
            short = _pascal(prop.python_name)
        attrs.setdefault(short, enum_type)
        attrs.setdefault(enum_type.__name__, enum_type)
    return attrs


def make(class_name: str, factory_name: str) -> type[Element]:
    """introspection 결과로 Element 서브클래스를 만든다.

    큐레이션 목록에 없는 엘리먼트에도 쓸 수 있다:

        Compositor = make("Compositor", "compositor")
    """
    spec = inspect_element(factory_name)  # 미설치면 UnknownElementError

    doc_lines = [
        f"{factory_name} — {spec.long_name or spec.description}",
        "",
        f"klass: {spec.klass}",
        "",
        "설정 가능한 프로퍼티:",
    ]
    doc_lines += [f"    {p.describe()}" for p in spec.writable_properties]

    namespace: dict[str, Any] = {
        "FACTORY": factory_name,
        "__doc__": "\n".join(doc_lines),
        "__module__": __name__,
        "_SPEC": spec,
    }
    namespace.update(_nested_enums(class_name, spec))
    return type(class_name, (Element,), namespace)


def available() -> dict[str, str]:
    """큐레이션 목록 중 이 시스템에 실제로 설치된 것만."""
    from ..introspect import list_factories

    installed = set(list_factories())
    return {k: v for k, v in CURATED.items() if v in installed}


def __getattr__(name: str) -> Any:
    factory_name = CURATED.get(name)
    if factory_name is None:
        raise AttributeError(
            f"'{name}' 은 큐레이션 목록에 없습니다. "
            f"Element(\"<팩토리이름>\") 으로 직접 쓰거나 "
            f"elements.make(\"{name}\", \"<팩토리이름>\") 로 클래스를 만드세요."
        )
    with _lock:
        cls = globals().get(name)
        if cls is None:
            cls = make(name, factory_name)
            globals()[name] = cls
    return cls


def __dir__() -> list[str]:
    return sorted({*__all__, *CURATED})
