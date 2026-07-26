"""Element 래퍼 — 프로퍼티를 파이썬 속성처럼 다룬다.

    src = Element("videotestsrc", num_buffers=100, pattern="ball")
    src.num_buffers = 50          # 범위 검증 후 설정
    src.pattern                   # <VideoTestSrcPattern.BALL: 18>

큐레이션된 엘리먼트는 이름 있는 서브클래스로 제공된다:

    from gstreamer_python_sdk.elements import VideoTestSrc
    src = VideoTestSrc(num_buffers=100, pattern=VideoTestSrc.Pattern.BALL)
"""

from __future__ import annotations

import difflib
import re
from fractions import Fraction
from pathlib import Path
from typing import Any, ClassVar, Generic, TypeVar

from ._bootstrap import ensure_initialized, require
from .caps import Caps, coerce_caps
from .enums import GstEnum, GstFlags
from .errors import LinkError, PropertyError, UnknownElementError
from .introspect import ElementSpec, PropertyKind, PropertySpec, inspect_element

__all__ = ["Element", "Prop", "launch_string"]

_R = TypeVar("_R")
_W = TypeVar("_W")


class Prop(Generic[_R, _W]):
    """읽기 타입과 쓰기 타입이 다른 프로퍼티를 표현하는 디스크립터.

    enum 프로퍼티는 읽으면 항상 Enum 멤버지만, 쓸 때는 Enum·nick 문자열·정수를
    모두 받는다. 이 비대칭을 하나의 애노테이션으로는 표현할 수 없어서 생성된
    .pyi 가 `Prop[VideoTestSrcPattern, VideoTestSrcPattern | str | int]` 형태로
    선언한다.

    런타임에는 쓰이지 않는다 — 실제 접근은 Element.__getattr__ /
    Element.__setattr__ 이 처리한다. 타입 검사기를 위한 선언용 타입이다.
    """

    def __get__(self, obj: Any, owner: type | None = None) -> _R:  # pragma: no cover
        raise NotImplementedError

    def __set__(self, obj: Any, value: _W) -> None:  # pragma: no cover
        raise NotImplementedError


class Element:
    """Gst.Element 래퍼.

    서브클래스는 `FACTORY` 클래스 속성으로 팩토리 이름을 고정한다.
    """

    FACTORY: ClassVar[str] = ""

    def __init__(
        self,
        factory_name: str | None = None,
        /,
        *,
        name: str | None = None,
        **properties: Any,
    ) -> None:
        factory = factory_name or type(self).FACTORY
        if not factory:
            raise ValueError("factory_name 을 지정하거나 FACTORY 를 가진 서브클래스를 쓰세요")

        ensure_initialized()
        Gst = require("Gst")

        spec = inspect_element(factory)
        gst_element = Gst.ElementFactory.make(factory, name)
        if gst_element is None:
            raise UnknownElementError(factory, detail="인스턴스 생성 실패")

        object.__setattr__(self, "_spec", spec)
        object.__setattr__(self, "_gst", gst_element)
        object.__setattr__(self, "_explicit_name", name is not None)

        if properties:
            self.set(**properties)

    # -- 생성 -------------------------------------------------------------

    @classmethod
    def wrap(cls, gst_element) -> "Element":
        """이미 존재하는 Gst.Element 를 감싼다(파이프라인 순회 결과 등)."""
        factory = gst_element.get_factory()
        spec = inspect_element(factory.get_name()) if factory else ElementSpec("<unknown>")
        obj = object.__new__(cls)
        object.__setattr__(obj, "_spec", spec)
        object.__setattr__(obj, "_gst", gst_element)
        object.__setattr__(obj, "_explicit_name", None)  # 알 수 없음 → 추측한다
        return obj

    # -- 기본 정보 ---------------------------------------------------------

    @property
    def gst(self):
        """감싸고 있는 Gst.Element. SDK 가 못 덮는 기능은 여기로 내려간다."""
        return self._gst

    @property
    def spec(self) -> ElementSpec:
        """이 엘리먼트의 introspection 결과."""
        return self._spec

    @property
    def name(self) -> str:
        return self._gst.get_name()

    @property
    def factory_name(self) -> str:
        return self._spec.factory_name

    # -- 프로퍼티 ----------------------------------------------------------

    def _lookup(self, python_name: str) -> PropertySpec:
        spec = self._spec.get(python_name)
        if spec is None:
            candidates = list(self._spec.properties)
            raise PropertyError(
                self.factory_name,
                python_name,
                "그런 프로퍼티가 없습니다",
                difflib.get_close_matches(python_name, candidates, n=4, cutoff=0.5),
            )
        return spec

    def _coerce(self, spec: PropertySpec, value: Any) -> Any:
        """Python 값 → GObject 가 받을 수 있는 값. 범위/선택지 검증 포함."""
        if value is None:
            return None

        if spec.enum_type is not None:
            try:
                member = spec.enum_type.coerce(value)
            except (ValueError, TypeError) as e:
                raise PropertyError(self.factory_name, spec.python_name, str(e)) from e
            return int(member)

        if spec.kind is PropertyKind.CAPS:
            return coerce_caps(value)

        if spec.kind is PropertyKind.FRACTION:
            Gst = require("Gst")
            if isinstance(value, Fraction):
                return Gst.Fraction(value.numerator, value.denominator)
            if isinstance(value, tuple) and len(value) == 2:
                return Gst.Fraction(*value)
            if isinstance(value, int):
                return Gst.Fraction(value, 1)
            return value

        if spec.kind is PropertyKind.STRING:
            if isinstance(value, Path):
                return str(value)
            if not isinstance(value, str):
                raise PropertyError(
                    self.factory_name,
                    spec.python_name,
                    f"문자열이 필요한데 {type(value).__name__} 을 받았습니다",
                )
            return value

        if spec.kind is PropertyKind.BOOL:
            if not isinstance(value, (bool, int)):
                raise PropertyError(
                    self.factory_name,
                    spec.python_name,
                    f"bool 이 필요한데 {type(value).__name__} 을 받았습니다",
                )
            return bool(value)

        if spec.kind in (PropertyKind.INT, PropertyKind.FLOAT):
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise PropertyError(
                    self.factory_name,
                    spec.python_name,
                    f"숫자가 필요한데 {type(value).__name__} 을 받았습니다",
                )
            if spec.kind is PropertyKind.INT:
                if isinstance(value, float) and not value.is_integer():
                    raise PropertyError(
                        self.factory_name, spec.python_name, f"정수가 필요합니다: {value}"
                    )
                value = int(value)
            if spec.minimum is not None and value < spec.minimum:
                raise PropertyError(
                    self.factory_name,
                    spec.python_name,
                    f"{value} 는 최솟값 {spec.minimum} 보다 작습니다",
                )
            if spec.maximum is not None and value > spec.maximum:
                raise PropertyError(
                    self.factory_name,
                    spec.python_name,
                    f"{value} 는 최댓값 {spec.maximum} 보다 큽니다",
                )
            return value

        return value

    def set(self, **properties: Any) -> "Element":
        """여러 프로퍼티를 한 번에 설정한다. self 를 반환."""
        for python_name, value in properties.items():
            spec = self._lookup(python_name)
            if not spec.writable:
                raise PropertyError(self.factory_name, python_name, "읽기 전용 프로퍼티입니다")
            self._gst.set_property(spec.name, self._coerce(spec, value))
        return self

    def get(self, python_name: str) -> Any:
        """프로퍼티 값을 읽는다. enum 은 생성된 Python Enum 으로 돌려준다."""
        spec = self._lookup(python_name)
        if not spec.readable:
            raise PropertyError(self.factory_name, python_name, "쓰기 전용 프로퍼티입니다")
        value = self._gst.get_property(spec.name)
        if spec.enum_type is not None and value is not None:
            try:
                return spec.enum_type(int(value))
            except (ValueError, TypeError):
                return value
        if spec.kind is PropertyKind.CAPS and value is not None:
            return Caps.from_gst(value)
        return value

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_"):
            object.__setattr__(self, name, value)
            return
        self.set(**{name: value})

    def __getattr__(self, name: str) -> Any:
        # 내부 속성과 dunder 는 정상 경로로 처리되어야 한다(재귀 방지).
        if name.startswith("_"):
            raise AttributeError(name)
        return self.get(name)

    def __dir__(self) -> list[str]:
        return sorted({*super().__dir__(), *self._spec.properties})

    def values(self) -> dict[str, Any]:
        """읽을 수 있는 스칼라 프로퍼티들의 현재 값. 디버깅용."""
        out: dict[str, Any] = {}
        for spec in self._spec.properties.values():
            if not spec.readable or spec.kind in (PropertyKind.OBJECT, PropertyKind.OTHER):
                continue
            try:
                out[spec.python_name] = self.get(spec.python_name)
            except Exception:  # noqa: BLE001 - 값 조회 실패는 무시
                pass
        return out

    def describe(self) -> str:
        """이 엘리먼트가 받는 모든 프로퍼티를 사람이 읽을 형태로."""
        return self._spec.describe()

    def to_launch(self, *, include_defaults: bool = False) -> str:
        """gst-launch-1.0 문법으로 직렬화한다.

        디버깅에도 쓰지만, 문자열 launch 만 받는 API(대표적으로
        GstRtspServer 의 `set_launch()`)에 데이터모델을 넘기기 위한 다리다.

            VideoTestSrc(num_buffers=100, pattern="ball").to_launch()
            # 'videotestsrc num-buffers=100 pattern=ball'

        Args:
            include_defaults: 기본값과 같은 프로퍼티도 전부 적을지.
        """
        parts = [self.factory_name]

        # 자동 생성 이름은 적지 않는다. GStreamer 의 자동 이름이 항상 팩토리
        # 이름으로 시작하지는 않으므로(nvvidconv → 'nvvconv1'), 생성 시 이름을
        # 직접 줬는지를 기억해 두고 그것을 우선 믿는다.
        explicit = self._explicit_name
        if explicit is None:
            explicit = not re.fullmatch(rf"{re.escape(self.factory_name)}\d*", self.name)
        if explicit:
            parts.append(f"name={_launch_value(self.name)}")

        skip = {PropertyKind.OBJECT, PropertyKind.OTHER, PropertyKind.STRUCTURE}
        for spec in self._spec.properties.values():
            if not spec.writable or spec.kind in skip:
                continue
            try:
                value = self.get(spec.python_name)
            except Exception:  # noqa: BLE001 - 읽을 수 없는 프로퍼티는 건너뛴다
                continue
            if value is None:
                continue
            if not include_defaults and _equal_to_default(value, spec.default):
                continue
            parts.append(f"{spec.name}={_launch_value(value)}")

        return " ".join(parts)

    # -- 연결 / 패드 -------------------------------------------------------

    def link(self, other: "Element") -> "Element":
        """이 엘리먼트의 src 패드를 other 의 sink 패드에 연결하고 other 를 반환."""
        if not self._gst.link(other._gst):
            raise LinkError(self.name, other.name, _link_hint(self, other))
        return other

    def link_filtered(self, other: "Element", caps: Caps | str) -> "Element":
        """caps 를 강제하며 연결한다(capsfilter 없이 링크에 직접 caps 지정)."""
        if not self._gst.link_filtered(other._gst, coerce_caps(caps)):
            raise LinkError(self.name, other.name, f"caps 제약: {caps}")
        return other

    def pad(self, name: str = "src"):
        """정적 패드를 가져온다."""
        p = self._gst.get_static_pad(name)
        if p is None:
            available = [t.name for t in self._spec.pads]
            raise LinkError(self.name, name, f"'{name}' 패드가 없습니다. 템플릿: {available}")
        return p

    def request_pad(self, template: str):
        """tee 의 'src_%u' 처럼 요청형 패드를 새로 만든다."""
        p = self._gst.request_pad_simple(template) if hasattr(
            self._gst, "request_pad_simple"
        ) else self._gst.get_request_pad(template)
        if p is None:
            raise LinkError(self.name, template, "요청 패드를 만들 수 없습니다")
        return p

    def on(self, signal: str, handler) -> int:
        """시그널 연결. decodebin 의 'pad-added' 등.

            decode.on("pad-added", lambda el, pad: pad.link(sink.pad("sink")))
        """
        return self._gst.connect(signal, handler)

    # -- 기타 --------------------------------------------------------------

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.name!r} ({self.factory_name})>"


def launch_string(*items: "Element | Caps | str") -> str:
    """엘리먼트와 caps 를 ' ! ' 로 이어 gst-launch 문자열을 만든다.

        launch_string(VideoTestSrc(is_live=True), VideoCaps(width=640), X264Enc())
        # 'videotestsrc is-live=true ! video/x-raw, width=640 ! x264enc'

    capsfilter 엘리먼트는 `capsfilter caps="..."` 대신 caps 만 적어 읽기 쉽게
    만든다 — gst-launch 문법에서 둘은 같은 뜻이다.
    """
    parts: list[str] = []
    for item in items:
        if isinstance(item, Caps):
            parts.append(item.to_string())
        elif isinstance(item, str):
            parts.append(item)
        elif isinstance(item, Element):
            if item.factory_name == "capsfilter":
                caps = item.get("caps")
                parts.append(caps.to_string() if caps is not None else item.to_launch())
            else:
                parts.append(item.to_launch())
        else:
            raise TypeError(f"launch 문자열로 만들 수 없는 값: {item!r}")
    return " ! ".join(parts)


def _equal_to_default(value: Any, default: Any) -> bool:
    """현재 값이 기본값과 같은지. enum 은 정수로 비교한다."""
    if default is None:
        return False
    try:
        if isinstance(value, (GstEnum, GstFlags)) or isinstance(default, (GstEnum, GstFlags)):
            return int(value) == int(default)
        return bool(value == default)
    except (TypeError, ValueError):
        return False


def _launch_value(value: Any) -> str:
    """Python 값 → gst-launch 프로퍼티 값 표기."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (GstEnum, GstFlags)):
        return value.nick
    if isinstance(value, Caps):
        return _quote(value.to_string())
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    return _quote(text) if not text or re.search(r"[\s,;!\"'()=\[\]{}]", text) else text


def _quote(text: str) -> str:
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _link_hint(src: "Element", sink: "Element") -> str:
    """연결 실패 시 원인을 좁혀준다 — 패드 부재인지 caps 협상 실패인지."""
    lines = []
    missing = False
    for element, direction in ((src, "src"), (sink, "sink")):
        caps = [p.caps for p in element._spec.pads if p.direction == direction]
        if not caps:
            lines.append(f"  {element.factory_name} 에는 {direction} 패드가 없습니다")
            missing = True
            continue
        text = caps[0]
        if len(text) > 160:
            text = text[:157] + "..."
        lines.append(f"  {element.factory_name} {direction} 패드: {text}")

    if missing:
        lines.append("  → 연결 방향이 뒤바뀌지 않았는지 확인하세요 (source → sink 순서).")
    else:
        lines.append(
            "  → caps 가 겹치지 않습니다. videoconvert/videoscale/audioconvert "
            "(Jetson 은 nvvidconv) 를 사이에 넣어보세요."
        )
    return "\n".join(lines)
