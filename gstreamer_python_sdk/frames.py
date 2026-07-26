"""appsrc 로 프레임을 밀어 넣기.

numpy 배열이나 bytes 를 파이프라인에 직접 공급한다. caps 를 데이터모델로
못 박아 두므로 버퍼 크기가 맞는지 push 시점에 검증할 수 있다 — 크기가
어긋나면 GStreamer 깊은 곳에서 알아보기 어려운 오류가 나기 때문이다.

    src = FrameSource(VideoCaps(format=VideoFormat.RGB, width=640, height=480, framerate=30))

    pipeline = Pipeline()
    pipeline.build(src, VideoConvert(), AutoVideoSink())

    pipeline.play(timeout=0)         # ← 아래 설명 참고
    try:
        for _ in range(90):
            src.push(make_frame())   # (480, 640, 3) uint8
        src.end()                    # EOS 를 보내 정상 종료
        pipeline.wait_eos()
    finally:
        pipeline.stop()

**`with pipeline:` 를 쓰지 말 것.** appsrc 는 첫 버퍼가 들어와야 preroll 이
끝나는데, 그 버퍼는 우리가 넣어야 한다. 상태 전이가 끝나기를 기다리면
서로를 기다리다 타임아웃이 난다. `play(timeout=0)` 으로 비동기 전이를
시작해 두고 곧바로 push 를 시작하면 된다.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any

from ._bootstrap import require
from .caps import Caps, coerce_caps
from .element import Element
from .errors import GstSdkError

__all__ = ["FrameSource"]

_NS_PER_SEC = 1_000_000_000


class FrameSource(Element):
    """appsrc 래퍼. 애플리케이션이 만든 프레임을 파이프라인에 공급한다."""

    FACTORY = "appsrc"

    def __init__(
        self,
        caps: Caps | str,
        *,
        name: str | None = None,
        is_live: bool = False,
        block: bool = True,
        max_bytes: int = 0,
        **properties: Any,
    ) -> None:
        """
        Args:
            caps: 공급할 프레임의 형식. VideoCaps 를 쓰면 크기 검증이 켜진다.
            is_live: 실시간 소스처럼 동작시킬지(카메라 대체 등).
            block: 큐가 가득 차면 push 를 블로킹할지. False 면 버퍼를 버린다.
            max_bytes: 내부 큐 크기(바이트). 0 이면 GStreamer 기본값.
        """
        Gst = require("Gst")
        gst_caps = coerce_caps(caps)

        props: dict[str, Any] = {
            "caps": gst_caps,
            "is_live": is_live,
            "block": block,
            # PTS 를 직접 넣으므로 시간 기반 포맷이어야 한다.
            "format": Gst.Format.TIME,
        }
        if max_bytes:
            props["max_bytes"] = max_bytes
        props.update(properties)
        super().__init__(name=name, **props)

        object.__setattr__(self, "_caps_model", caps if isinstance(caps, Caps) else None)
        object.__setattr__(self, "_pushed", 0)
        object.__setattr__(self, "_ended", False)
        object.__setattr__(self, "_frame_bytes", _expected_bytes(gst_caps))
        object.__setattr__(self, "_frame_duration", _frame_duration(gst_caps))
        object.__setattr__(self, "_shape", _frame_shape(gst_caps, self._frame_bytes))

    # -- 정보 --------------------------------------------------------------

    @property
    def shape(self) -> tuple[int, ...] | None:
        """공급해야 할 numpy 배열 모양. 알 수 없으면 None(평면 포맷 등)."""
        return self._shape

    @property
    def frame_bytes(self) -> int | None:
        """프레임 하나의 바이트 수. caps 에서 알아낼 수 없으면 None."""
        return self._frame_bytes

    @property
    def frames_pushed(self) -> int:
        return self._pushed

    @property
    def ended(self) -> bool:
        return self._ended

    # -- 공급 --------------------------------------------------------------

    def push(
        self,
        frame: Any,
        *,
        pts: float | None = None,
        duration: float | None = None,
    ) -> None:
        """프레임 하나를 파이프라인에 넣는다.

        Args:
            frame: numpy 배열, bytes, bytearray, memoryview 등 버퍼 프로토콜을
                지원하는 것이면 무엇이든.
            pts: 표시 시각(초). 생략하면 framerate 기준으로 자동 계산한다.
            duration: 프레임 길이(초). 생략하면 framerate 에서 가져온다.

        Raises:
            GstSdkError: end() 이후에 push 했거나, 크기가 caps 와 다르거나,
                파이프라인이 버퍼를 거부했을 때.
        """
        if self._ended:
            raise GstSdkError(f"{self.name}: end() 를 부른 뒤에는 push 할 수 없습니다")

        Gst = require("Gst")
        data = _to_bytes(frame)

        expected = self._frame_bytes
        if expected is not None and len(data) != expected:
            raise GstSdkError(
                f"{self.name}: 프레임 크기가 caps 와 맞지 않습니다 — "
                f"{len(data):,} bytes 를 받았지만 {expected:,} bytes 가 필요합니다"
                + (f" (모양 {self._shape})" if self._shape else "")
            )

        buffer = Gst.Buffer.new_wrapped(data)
        step = self._frame_duration
        if duration is not None:
            buffer.duration = int(duration * _NS_PER_SEC)
        elif step is not None:
            buffer.duration = step
        if pts is not None:
            buffer.pts = int(pts * _NS_PER_SEC)
        elif step is not None:
            buffer.pts = self._pushed * step
        buffer.dts = buffer.pts

        result = self.gst.emit("push-buffer", buffer)
        if result != Gst.FlowReturn.OK:
            raise GstSdkError(
                f"{self.name}: 버퍼가 거부되었습니다 ({result.value_nick}). "
                "파이프라인이 PLAYING 상태이고 EOS 이전인지 확인하세요."
            )
        object.__setattr__(self, "_pushed", self._pushed + 1)

    def end(self) -> None:
        """EOS 를 보낸다. 멱등이며, 이후 push 는 거부된다."""
        if self._ended:
            return
        Gst = require("Gst")
        object.__setattr__(self, "_ended", True)
        result = self.gst.emit("end-of-stream")
        if result != Gst.FlowReturn.OK:
            raise GstSdkError(f"{self.name}: EOS 전송 실패 ({result.value_nick})")

    def __repr__(self) -> str:
        shape = f" shape={self._shape}" if self._shape else ""
        return f"<FrameSource {self.name!r} pushed={self._pushed}{shape}>"


# --------------------------------------------------------------------------


def _to_bytes(frame: Any) -> bytes:
    """numpy 배열 등 버퍼 프로토콜 객체 → bytes. numpy 의존성은 없다."""
    if isinstance(frame, (bytes, bytearray, memoryview)):
        return bytes(frame)
    tobytes = getattr(frame, "tobytes", None)
    if callable(tobytes):
        return tobytes()  # numpy.ndarray 는 연속 메모리로 복사해 준다
    try:
        return bytes(memoryview(frame))
    except TypeError as e:
        raise GstSdkError(
            f"프레임으로 쓸 수 없는 값입니다: {type(frame).__name__} "
            "(numpy 배열이나 bytes 를 넘기세요)"
        ) from e


def _video_info(gst_caps: Any) -> Any | None:
    """video/x-raw caps 라면 GstVideo.VideoInfo 를, 아니면 None."""
    structure = gst_caps.get_structure(0)
    if structure is None or structure.get_name() != "video/x-raw":
        return None
    try:
        GstVideo = require("GstVideo")
        return GstVideo.VideoInfo.new_from_caps(gst_caps)
    except Exception:  # noqa: BLE001 - 정보를 못 얻으면 검증만 건너뛴다
        return None


def _expected_bytes(gst_caps: Any) -> int | None:
    info = _video_info(gst_caps)
    if info is None:
        return None
    size = int(info.size)
    return size or None


def _frame_shape(gst_caps: Any, frame_bytes: int | None) -> tuple[int, ...] | None:
    """단일 평면 8비트 포맷일 때만 (h, w, c) 를 알려준다."""
    info = _video_info(gst_caps)
    if info is None or frame_bytes is None:
        return None
    width, height = int(info.width), int(info.height)
    if width <= 0 or height <= 0 or info.finfo.n_planes != 1:
        return None
    per_pixel, remainder = divmod(frame_bytes, width * height)
    if remainder or per_pixel <= 0:
        return None
    return (height, width) if per_pixel == 1 else (height, width, per_pixel)


def _frame_duration(gst_caps: Any) -> int | None:
    """caps 의 framerate 에서 프레임 하나의 길이(ns)를 구한다."""
    structure = gst_caps.get_structure(0)
    if structure is None:
        return None
    ok, numerator, denominator = structure.get_fraction("framerate")
    if not ok or numerator <= 0:
        return None
    return int(Fraction(denominator, numerator) * _NS_PER_SEC)
