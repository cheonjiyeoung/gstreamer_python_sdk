"""Caps 데이터모델.

`"video/x-raw,format=NV12,width=1920,height=1080,framerate=30/1"` 같은 문자열
대신 타입이 있는 객체로 다룬다.

    VideoCaps(format=VideoFormat.NV12, width=1920, height=1080, framerate=30)
    VideoCaps(width=1920, height=1080, memory=Memory.NVMM)   # Jetson NVMM
    AudioCaps(format=AudioFormat.S16LE, rate=48000, channels=2)

값 종류:
    IntRange(1, 60)         → [ 1, 60 ]
    Options("au", "nal")    → { au, nal }
    Fraction(30000, 1001)   → 30000/1001
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Iterable, Mapping

from ._bootstrap import require
from .enums import GstEnum, GstStrEnum, Memory

__all__ = [
    "Caps",
    "VideoCaps",
    "AudioCaps",
    "IntRange",
    "Options",
    "Fraction",
    "Memory",
]


@dataclass(frozen=True)
class IntRange:
    """caps 의 `[ min, max ]` 값."""

    minimum: int
    maximum: int

    def __str__(self) -> str:
        return f"[ {self.minimum}, {self.maximum} ]"


@dataclass(frozen=True)
class Options:
    """caps 의 `{ a, b, c }` 값(택일 목록)."""

    values: tuple[Any, ...]

    def __init__(self, *values: Any) -> None:
        object.__setattr__(self, "values", tuple(values))

    def __str__(self) -> str:
        return "{ " + ", ".join(_format_value(v) for v in self.values) + " }"


def _format_value(value: Any) -> str:
    """Python 값 → caps 문자열 조각."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (IntRange, Options)):
        return str(value)
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}"
    if isinstance(value, GstStrEnum):
        return value.value
    if isinstance(value, GstEnum):
        return value.nick
    if isinstance(value, tuple) and len(value) == 2 and all(isinstance(v, int) for v in value):
        return f"{value[0]}/{value[1]}"  # framerate=(30, 1)
    if isinstance(value, (list, set)):
        return "{ " + ", ".join(_format_value(v) for v in value) + " }"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return repr(value)
    text = str(value)
    if any(c in text for c in " ,;{}[]()=\"'"):
        escaped = text.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return text


class Caps:
    """미디어 타입 + 필드 + feature 로 이루어진 caps 하나.

    필드 이름은 snake_case 로 써도 되고(내부에서 '-' 로 변환), None 인 값은
    caps 에서 생략된다 — 지정하지 않은 필드는 협상에 열어둔다는 뜻이다.
    """

    media_type: str = ""

    def __init__(
        self,
        media_type: str | None = None,
        *,
        features: Iterable[str | Memory] = (),
        **fields: Any,
    ) -> None:
        resolved = media_type or type(self).media_type
        if not resolved:
            raise ValueError("media_type 을 지정해야 합니다 (예: 'video/x-raw')")
        self.media_type = resolved
        self.features: tuple[str, ...] = tuple(
            f.value if isinstance(f, Memory) else str(f) for f in features
        )
        self.fields: dict[str, Any] = {
            k.replace("_", "-"): v for k, v in fields.items() if v is not None
        }

    # -- 변환 -------------------------------------------------------------

    def to_string(self) -> str:
        """gst-launch 에 그대로 넣을 수 있는 caps 문자열."""
        head = self.media_type
        if self.features:
            head += "(" + ", ".join(self.features) + ")"
        if not self.fields:
            return head
        body = ", ".join(f"{k}={_format_value(v)}" for k, v in self.fields.items())
        return f"{head}, {body}"

    def to_gst(self):
        """Gst.Caps 로 변환."""
        Gst = require("Gst")
        text = self.to_string()
        caps = Gst.Caps.from_string(text)
        if caps is None:
            raise ValueError(f"caps 문자열로 변환할 수 없습니다: {text}")
        return caps

    @classmethod
    def from_string(cls, text: str) -> "Caps":
        """gst-launch caps 문자열 파싱."""
        Gst = require("Gst")
        caps = Gst.Caps.from_string(text)
        if caps is None:
            raise ValueError(f"caps 문자열을 파싱할 수 없습니다: {text}")
        return cls.from_gst(caps)

    @classmethod
    def from_gst(cls, caps) -> "Caps":
        """Gst.Caps → 데이터모델. 여러 구조면 첫 번째만 취한다."""
        if caps.get_size() == 0:
            return Caps("ANY")
        structure = caps.get_structure(0)
        features = caps.get_features(0)
        feature_names: tuple[str, ...] = ()
        if features is not None:
            text = features.to_string()
            if text and text != "memory:SystemMemory":
                feature_names = tuple(t.strip() for t in text.split(","))

        fields: dict[str, Any] = {}
        for i in range(structure.n_fields()):
            key = structure.nth_field_name(i)
            fields[key.replace("-", "_")] = structure.get_value(key)
        return Caps(structure.get_name(), features=feature_names, **fields)

    # -- 조합 -------------------------------------------------------------

    def with_fields(self, **fields: Any) -> "Caps":
        """필드를 덮어쓴 새 Caps 를 반환(원본 불변)."""
        merged = {k.replace("-", "_"): v for k, v in self.fields.items()}
        merged.update(fields)
        return Caps(self.media_type, features=self.features, **merged)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Caps):
            return NotImplemented
        return (
            self.media_type == other.media_type
            and self.fields == other.fields
            and set(self.features) == set(other.features)
        )

    def __hash__(self) -> int:
        return hash((self.media_type, tuple(sorted(self.fields.items(), key=str)), self.features))

    def __str__(self) -> str:
        return self.to_string()

    def __repr__(self) -> str:
        return f"<Caps {self.to_string()}>"


class VideoCaps(Caps):
    """`video/x-raw` caps.

    Args:
        format: VideoFormat 멤버 또는 'NV12' 같은 문자열.
        width, height: 픽셀 크기. IntRange 도 가능.
        framerate: 정수(30), (30, 1) 튜플, 또는 Fraction(30000, 1001).
        memory: Memory.NVMM 처럼 caps feature 를 지정.
    """

    media_type = "video/x-raw"

    def __init__(
        self,
        *,
        format: Any = None,  # noqa: A002 - caps 필드 이름과 일치시킨다
        width: int | IntRange | None = None,
        height: int | IntRange | None = None,
        framerate: int | tuple[int, int] | Fraction | None = None,
        memory: Memory | str | None = None,
        media_type: str | None = None,
        **extra: Any,
    ) -> None:
        if isinstance(framerate, int):
            framerate = Fraction(framerate, 1)
        features = (memory,) if memory is not None else ()
        super().__init__(
            media_type,
            features=features,
            format=format,
            width=width,
            height=height,
            framerate=framerate,
            **extra,
        )


class AudioCaps(Caps):
    """`audio/x-raw` caps."""

    media_type = "audio/x-raw"

    def __init__(
        self,
        *,
        format: Any = None,  # noqa: A002
        rate: int | IntRange | None = None,
        channels: int | IntRange | None = None,
        layout: str | None = "interleaved",
        media_type: str | None = None,
        **extra: Any,
    ) -> None:
        super().__init__(
            media_type,
            format=format,
            rate=rate,
            channels=channels,
            layout=layout,
            **extra,
        )


def coerce_caps(value: Any) -> Any:
    """Caps / 문자열 / Gst.Caps 를 Gst.Caps 로 통일."""
    Gst = require("Gst")
    if isinstance(value, Gst.Caps):
        return value
    if isinstance(value, Caps):
        return value.to_gst()
    if isinstance(value, str):
        caps = Gst.Caps.from_string(value)
        if caps is None:
            raise ValueError(f"caps 문자열을 파싱할 수 없습니다: {value}")
        return caps
    raise TypeError(f"caps 로 쓸 수 없는 값: {value!r}")
