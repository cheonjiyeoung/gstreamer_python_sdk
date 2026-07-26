"""gi 기반 GStreamer 사용을 간편하게 해주는 SDK.

문자열 대신 데이터모델과 Enum 으로 파이프라인을 조립한다:

    from gstreamer_python_sdk import Pipeline, VideoCaps
    from gstreamer_python_sdk.elements import VideoTestSrc, VideoConvert, AutoVideoSink

    src  = VideoTestSrc(num_buffers=100, pattern=VideoTestSrc.Pattern.BALL)
    conv = VideoConvert()
    sink = AutoVideoSink(sync=False)

    pipeline = Pipeline()
    pipeline.add(src, conv, sink)
    pipeline.link(src, VideoCaps(width=640, height=480, framerate=30), conv, sink)

    with pipeline:
        pipeline.wait_eos()

이 패키지를 import 하는 것만으로는 gi 도, GStreamer 초기화도 일어나지 않는다.
GStreamer 는 실제로 쓰이는 순간 자동으로 초기화된다. 초기화 비용(플러그인
레지스트리 스캔)을 앱 시작 시점으로 앞당기려면 `init()` 을 직접 부른다.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

# 아래 모듈들은 gi 를 건드리지 않으므로 즉시 import 해도 무해하다.
from ._bootstrap import (
    diagnostics,
    ensure_initialized,
    gst_version,
    gst_version_string,
    init,
    is_initialized,
    require,
)
from .bus import Bus, Message, MessageType
from .caps import AudioCaps, Caps, Fraction, IntRange, Memory, Options, VideoCaps
from .element import Element, launch_string
from .enums import GstEnum, GstFlags, GstStrEnum
from .frames import FrameSource
from .errors import (
    GiNotFoundError,
    GstError,
    GstInitError,
    GstSdkError,
    GstTimeout,
    LinkError,
    PipelineParseError,
    PropertyError,
    StateChangeError,
    UnknownElementError,
)
from .introspect import (
    ElementSpec,
    PadSpec,
    PropertyKind,
    PropertySpec,
    inspect_element,
    list_factories,
)
from .graph import diagram, save_graph, to_dot
from .mainloop import MainLoop, run_pipeline
from .pipeline import Pipeline

__version__ = "0.4.0"

# gi typelib 이 있어야 만들 수 있는 심볼은 지연 로딩한다(PEP 562).
_LAZY = {
    "VideoFormat": ".enums",
    "AudioFormat": ".enums",
    # GstRtspServer typelib 이 있어야 import 되므로 지연 로딩한다
    "RtspServer": ".rtsp",
}

__all__ = [
    "__version__",
    # 부트스트랩
    "init",
    "ensure_initialized",
    "is_initialized",
    "require",
    "gst_version",
    "gst_version_string",
    "diagnostics",
    # 핵심 타입
    "Pipeline",
    "Element",
    "FrameSource",
    "launch_string",
    # 버스 / 메인루프
    "Bus",
    "Message",
    "MessageType",
    "MainLoop",
    "run_pipeline",
    # 그래프 / RTSP
    "diagram",
    "to_dot",
    "save_graph",
    "RtspServer",
    # caps 데이터모델
    "Caps",
    "VideoCaps",
    "AudioCaps",
    "IntRange",
    "Options",
    "Fraction",
    "Memory",
    "VideoFormat",
    "AudioFormat",
    # enum 기반 타입
    "GstEnum",
    "GstFlags",
    "GstStrEnum",
    # introspection
    "inspect_element",
    "list_factories",
    "ElementSpec",
    "PropertySpec",
    "PropertyKind",
    "PadSpec",
    # 예외
    "GstSdkError",
    "GiNotFoundError",
    "GstInitError",
    "PipelineParseError",
    "StateChangeError",
    "GstError",
    "GstTimeout",
    "UnknownElementError",
    "PropertyError",
    "LinkError",
]

if TYPE_CHECKING:  # 정적 분석기/IDE 자동완성용 (런타임에는 실행되지 않음)
    from .rtsp import RtspServer
    from .enums import AudioFormat, VideoFormat


def __getattr__(name: str):
    module_name = _LAZY.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    from importlib import import_module

    value = getattr(import_module(module_name, __name__), name)
    globals()[name] = value  # 다음 접근부터는 __getattr__ 을 타지 않는다
    return value


def __dir__() -> list[str]:
    return sorted(__all__)
