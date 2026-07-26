"""GObject enum/flags → Python Enum 동적 생성.

GStreamer 의 enum 프로퍼티(예: videotestsrc 의 pattern)는 GIR typelib 에
등록되지 않은 동적 GType 인 경우가 많아 `gtype.pytype` 이 None 이다. 대신
GParamSpec 의 enum_class / flags_class 를 통해 값과 nick 을 모두 얻을 수 있고,
이 모듈은 그것을 진짜 Python Enum 으로 바꾼다.

    Pattern = enum_from_pspec(pspec)     # <enum 'VideoTestSrcPattern'>
    Pattern.SMPTE                        # 0
    Pattern.SMPTE.nick                   # 'smpte'
    Pattern.coerce("ball")               # <VideoTestSrcPattern.BALL: 18>
"""

from __future__ import annotations

import enum
import keyword
import re
import threading
from typing import Any, ClassVar

__all__ = [
    "GstEnum",
    "GstFlags",
    "GstStrEnum",
    "Memory",
    "enum_from_pspec",
    "flags_from_pspec",
    "member_name_for",
    "class_name_for",
]

_lock = threading.RLock()
_cache: dict[str, type] = {}


# --------------------------------------------------------------------------
# 기반 Enum 타입
# --------------------------------------------------------------------------


class GstEnum(enum.IntEnum):
    """GStreamer GEnum 프로퍼티에 대응. int 로도 nick 문자열로도 다룰 수 있다.

    {정수값: nick} 매핑인 `_nicks` 는 클래스 생성 후 주입된다. Enum 클래스
    본문에서 값을 대입하면 그 이름이 enum 멤버가 되어버리므로 밖에서 넣는다.
    애노테이션만 두는 것은 안전하다 — 값이 없으면 멤버로 취급되지 않는다.
    """

    _nicks: ClassVar[dict[int, str]]

    @property
    def nick(self) -> str:
        """gst-launch 문법에서 쓰는 문자열 (예: 'smpte')."""
        return type(self)._nicks.get(int(self), str(int(self)))

    @classmethod
    def from_nick(cls, nick: str) -> "GstEnum":
        for value, n in cls._nicks.items():
            if n == nick:
                return cls(value)
        raise ValueError(
            f"{cls.__name__} 에 nick '{nick}' 이 없습니다. "
            f"가능한 값: {', '.join(sorted(cls._nicks.values()))}"
        )

    @classmethod
    def coerce(cls, value: Any) -> "GstEnum":
        """Enum 멤버 / 정수 / nick 문자열 무엇이든 받아 멤버로 변환."""
        if isinstance(value, cls):
            return value
        if isinstance(value, str):
            return cls.from_nick(value)
        if isinstance(value, int):
            return cls(value)
        raise TypeError(f"{cls.__name__} 로 변환할 수 없는 값: {value!r}")

    def __str__(self) -> str:
        return self.nick


GstEnum._nicks = {}  # 서브클래스가 자기 것을 주입하기 전까지의 기본값


class GstFlags(enum.IntFlag):
    """GStreamer GFlags 프로퍼티에 대응. '+' 로 연결된 nick 문자열도 받는다."""

    _nicks: ClassVar[dict[int, str]]

    @property
    def nicks(self) -> tuple[str, ...]:
        return tuple(n for v, n in type(self)._nicks.items() if v and int(self) & v == v)

    @property
    def nick(self) -> str:
        return "+".join(self.nicks) or "0"

    @classmethod
    def coerce(cls, value: Any) -> "GstFlags":
        if isinstance(value, cls):
            return value
        if isinstance(value, int):
            return cls(value)
        if isinstance(value, str):
            result = cls(0)
            for part in re.split(r"[+|,]", value):
                part = part.strip()
                if not part:
                    continue
                match = next((v for v, n in cls._nicks.items() if n == part), None)
                if match is None:
                    raise ValueError(
                        f"{cls.__name__} 에 nick '{part}' 이 없습니다. "
                        f"가능한 값: {', '.join(sorted(cls._nicks.values()))}"
                    )
                result |= cls(match)
            return result
        if isinstance(value, (list, tuple, set)):
            result = cls(0)
            for item in value:
                result |= cls.coerce(item)
            return result
        raise TypeError(f"{cls.__name__} 로 변환할 수 없는 값: {value!r}")

    def __str__(self) -> str:
        return self.nick


GstFlags._nicks = {}


class GstStrEnum(str, enum.Enum):
    """caps 문자열에 그대로 들어가는 값들(VideoFormat 등)."""

    def __str__(self) -> str:
        return self.value


class Memory(GstStrEnum):
    """Caps feature — 버퍼가 어느 메모리에 있는지.

    Jetson 의 하드웨어 엘리먼트(nvv4l2*)는 대부분 NVMM 을 요구한다.
    """

    SYSTEM = "memory:SystemMemory"
    NVMM = "memory:NVMM"
    DMABUF = "memory:DMABuf"
    GL = "memory:GLMemory"
    EGL_IMAGE = "memory:EGLImage"


# --------------------------------------------------------------------------
# 이름 변환
# --------------------------------------------------------------------------


def member_name_for(nick: str) -> str:
    """GStreamer nick → Python Enum 멤버 이름. 'zone-plate' → 'ZONE_PLATE'."""
    name = re.sub(r"[^0-9a-zA-Z]+", "_", nick).strip("_").upper()
    if not name:
        name = "UNNAMED"
    if name[0].isdigit():
        name = f"V{name}"
    if keyword.iskeyword(name.lower()) and name in {"NONE", "TRUE", "FALSE"}:
        name = f"{name}_"
    return name


def class_name_for(gtype_name: str) -> str:
    """GType 이름 → Enum 클래스 이름. 'GstVideoTestSrcPattern' → 'VideoTestSrcPattern'."""
    name = gtype_name
    if name.startswith("Gst") and len(name) > 3 and name[3].isupper():
        name = name[3:]
    name = re.sub(r"[^0-9a-zA-Z_]", "_", name)
    if not name or name[0].isdigit():
        name = f"E{name}"
    return name


# --------------------------------------------------------------------------
# 생성
# --------------------------------------------------------------------------


def _build(base: type, gtype_name: str, pairs: list[tuple[str, int]], nicks: dict[int, str]):
    """이름 충돌을 정리한 뒤 Enum 클래스를 만든다."""
    seen: dict[str, int] = {}
    members: list[tuple[str, int]] = []
    for member_name, value in pairs:
        if member_name in seen:
            if seen[member_name] == value:
                continue  # 완전한 중복은 버린다
            member_name = f"{member_name}_{value}"  # 같은 이름 다른 값 → 접미사
        seen[member_name] = value
        members.append((member_name, value))

    cls = base(class_name_for(gtype_name), members, module=__name__)
    cls._nicks = nicks
    cls.__doc__ = f"{gtype_name} (GStreamer 에서 자동 생성)"
    cls.__gtype_name__ = gtype_name
    return cls


def enum_from_pspec(pspec) -> type[GstEnum] | None:
    """GParamSpec(enum) → GstEnum 서브클래스. enum 이 아니면 None."""
    gvalues = getattr(pspec, "enum_class", None)
    if gvalues is None:
        return None
    gtype_name = pspec.value_type.name
    with _lock:
        cached = _cache.get(gtype_name)
        if cached is not None:
            return cached

        nicks: dict[int, str] = {}
        pairs: list[tuple[str, int]] = []
        for gv in gvalues.__enum_values__.values():
            value = int(gv)
            nick = gv.value_nick
            nicks[value] = nick
            pairs.append((member_name_for(nick), value))

        cls = _build(GstEnum, gtype_name, pairs, nicks)
        _cache[gtype_name] = cls
        return cls


def flags_from_pspec(pspec) -> type[GstFlags] | None:
    """GParamSpec(flags) → GstFlags 서브클래스. flags 가 아니면 None."""
    gvalues = getattr(pspec, "flags_class", None)
    if gvalues is None:
        return None
    gtype_name = pspec.value_type.name
    with _lock:
        cached = _cache.get(gtype_name)
        if cached is not None:
            return cached

        nicks: dict[int, str] = {}
        pairs: list[tuple[str, int]] = []
        for gv in gvalues.__flags_values__.values():
            value = int(gv)
            # flags 값은 조합일 수 있어 nick 이 리스트다(value_nicks). 단일 비트만
            # 멤버로 삼고, 조합 값은 '|' 로 표기해 둔다.
            nick_list = list(getattr(gv, "value_nicks", None) or [])
            if not nick_list:
                continue
            nicks[value] = "+".join(nick_list)
            if len(nick_list) == 1:
                pairs.append((member_name_for(nick_list[0]), value))

        cls = _build(GstFlags, gtype_name, pairs, nicks)
        _cache[gtype_name] = cls
        return cls


# --------------------------------------------------------------------------
# caps 값에 쓰이는 대형 enum — GstVideo/GstAudio typelib 에서 지연 생성
# --------------------------------------------------------------------------


def _build_format_enum(namespace: str, enum_attr: str, to_string: str, class_name: str):
    from ._bootstrap import require

    mod = require(namespace)
    gi_enum = getattr(mod, enum_attr)
    converter = getattr(mod, to_string)

    pairs: list[tuple[str, str]] = []
    for name in dir(gi_enum):
        # UNKNOWN 은 변환 함수가 g_return_if_fail 로 거부한다(경고 출력).
        if not name.isupper() or name == "UNKNOWN":
            continue
        member = getattr(gi_enum, name)
        try:
            text = converter(member)
        except Exception:  # noqa: BLE001 - UNKNOWN 등 변환 불가 값은 건너뛴다
            continue
        if text and text != "UNKNOWN":
            pairs.append((member_name_for(text), text))

    # Enum 의 functional API — mypy 는 커스텀 베이스에 대한 이 호출을 모른다.
    cls = GstStrEnum(class_name, sorted(set(pairs)), module=__name__)  # type: ignore[call-overload]
    cls.__doc__ = f"{namespace}.{enum_attr} 에서 자동 생성된 caps 값"
    return cls


def __getattr__(name: str):
    """VideoFormat / AudioFormat 은 gi 를 필요로 하므로 접근 시점에 만든다."""
    specs = {
        "VideoFormat": ("GstVideo", "VideoFormat", "video_format_to_string", "VideoFormat"),
        "AudioFormat": ("GstAudio", "AudioFormat", "audio_format_to_string", "AudioFormat"),
    }
    spec = specs.get(name)
    if spec is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    with _lock:
        if name not in _cache:
            _cache[name] = _build_format_enum(*spec)
        value = _cache[name]
    globals()[name] = value
    return value
