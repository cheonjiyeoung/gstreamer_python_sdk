"""엘리먼트 메타데이터를 읽어 데이터모델로 만든다.

gst-inspect-1.0 가 보여주는 정보(프로퍼티 타입/기본값/범위/enum 값, 패드
템플릿)를 파싱 없이 GObject introspection 으로 직접 얻어 dataclass 로 담는다.
이 데이터모델이 런타임 검증과 .pyi 코드 생성 양쪽의 단일 소스다.
"""

from __future__ import annotations

import keyword
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

from ._bootstrap import ensure_initialized, require
from .enums import GstEnum, GstFlags, enum_from_pspec, flags_from_pspec
from .errors import UnknownElementError

__all__ = [
    "PropertyKind",
    "PropertySpec",
    "PadSpec",
    "ElementSpec",
    "inspect_element",
    "list_factories",
    "to_python_name",
    "to_gst_name",
]


class PropertyKind(str, Enum):
    """프로퍼티의 값 종류. 검증과 타입 힌트 생성에 쓰인다."""

    BOOL = "bool"
    INT = "int"
    FLOAT = "float"
    STRING = "string"
    ENUM = "enum"
    FLAGS = "flags"
    CAPS = "caps"
    FRACTION = "fraction"
    STRUCTURE = "structure"
    OBJECT = "object"
    OTHER = "other"


_FUNDAMENTAL_KIND = {
    "gboolean": PropertyKind.BOOL,
    "gint": PropertyKind.INT,
    "guint": PropertyKind.INT,
    "gint64": PropertyKind.INT,
    "guint64": PropertyKind.INT,
    "glong": PropertyKind.INT,
    "gulong": PropertyKind.INT,
    "gchar": PropertyKind.INT,
    "guchar": PropertyKind.INT,
    "gfloat": PropertyKind.FLOAT,
    "gdouble": PropertyKind.FLOAT,
    "gchararray": PropertyKind.STRING,
    "GEnum": PropertyKind.ENUM,
    "GFlags": PropertyKind.FLAGS,
    "GObject": PropertyKind.OBJECT,
    "GInterface": PropertyKind.OBJECT,
}

_BOXED_KIND = {
    "GstCaps": PropertyKind.CAPS,
    "GstFraction": PropertyKind.FRACTION,
    "GstStructure": PropertyKind.STRUCTURE,
    "GstValueArray": PropertyKind.OTHER,
}

#: PropertyKind → .pyi 에 쓸 타입 힌트. ENUM/FLAGS 는 생성된 클래스 이름으로 대체된다.
PYTHON_HINT = {
    PropertyKind.BOOL: "bool",
    PropertyKind.INT: "int",
    PropertyKind.FLOAT: "float",
    PropertyKind.STRING: "str",
    PropertyKind.CAPS: "Caps | str",
    PropertyKind.FRACTION: "Fraction | tuple[int, int]",
    PropertyKind.STRUCTURE: "dict[str, Any] | str",
    PropertyKind.OBJECT: "Any",
    PropertyKind.OTHER: "Any",
}


def to_python_name(gst_name: str) -> str:
    """'num-buffers' → 'num_buffers'.

    basesink 의 'async' 처럼 Python 예약어와 겹치는 이름은 뒤에 밑줄을 붙여
    'async_' 로 만든다. 키워드 인자로 넘길 수 있어야 하기 때문이다.
    """
    name = gst_name.replace("-", "_")
    if keyword.iskeyword(name):
        name += "_"
    return name


def to_gst_name(python_name: str) -> str:
    """'num_buffers' → 'num-buffers', 'async_' → 'async'."""
    name = python_name[:-1] if python_name.endswith("_") else python_name
    return name.replace("_", "-")


@dataclass(frozen=True)
class PropertySpec:
    """엘리먼트 프로퍼티 하나에 대한 완전한 기술."""

    name: str  # GStreamer 이름 (kebab-case)
    python_name: str  # snake_case
    kind: PropertyKind
    gtype: str
    blurb: str = ""
    default: Any = None
    minimum: Any = None
    maximum: Any = None
    readable: bool = True
    writable: bool = True
    construct_only: bool = False
    deprecated: bool = False
    enum_type: type[GstEnum] | type[GstFlags] | None = None

    @property
    def choices(self) -> tuple[str, ...]:
        """enum/flags 라면 선택 가능한 nick 목록."""
        if self.enum_type is None:
            return ()
        return tuple(sorted(self.enum_type._nicks.values()))

    def hint(self) -> str:
        """이 프로퍼티에 **넣을 수 있는** 값의 타입 힌트 (__init__ 인자용)."""
        if self.enum_type is not None:
            return f"{self.enum_type.__name__} | str | int"
        if self.kind is PropertyKind.CAPS:
            return "Caps | str"
        if self.kind is PropertyKind.STRING:
            return "str | None"
        return PYTHON_HINT.get(self.kind, "Any")

    def read_hint(self) -> str:
        """이 프로퍼티를 **읽었을 때** 나오는 값의 타입 힌트."""
        if self.enum_type is not None:
            return self.enum_type.__name__  # get() 이 항상 Enum 으로 되돌려준다
        if self.kind is PropertyKind.CAPS:
            return "Caps"
        if self.kind is PropertyKind.STRING:
            return "str | None"
        return PYTHON_HINT.get(self.kind, "Any")

    def attr_hint(self) -> str:
        """클래스 속성 선언용 힌트. 읽기/쓰기 타입이 다르면 Prop[...] 을 쓴다."""
        read, write = self.read_hint(), self.hint()
        return read if read == write else f"Prop[{read}, {write}]"

    def describe(self) -> str:
        bits = [f"{self.python_name}: {self.hint()}"]
        if self.default is not None:
            bits.append(f"= {self.default!r}")
        if self.minimum is not None:
            bits.append(f"[{self.minimum}, {self.maximum}]")
        if self.choices:
            bits.append("{" + ", ".join(self.choices) + "}")
        if not self.writable:
            bits.append("(읽기 전용)")
        elif self.construct_only:
            bits.append("(생성 시에만 설정 가능)")
        return "  ".join(bits)


@dataclass(frozen=True)
class PadSpec:
    """정적 패드 템플릿."""

    name: str
    direction: str  # 'src' | 'sink'
    presence: str  # 'always' | 'sometimes' | 'request'
    caps: str

    @property
    def is_request(self) -> bool:
        return self.presence == "request"

    @property
    def is_sometimes(self) -> bool:
        """decodebin/demuxer 처럼 런타임에 생기는 패드인지."""
        return self.presence == "sometimes"


@dataclass(frozen=True)
class ElementSpec:
    """엘리먼트 팩토리 하나에 대한 완전한 기술."""

    factory_name: str
    long_name: str = ""
    klass: str = ""
    description: str = ""
    properties: Mapping[str, PropertySpec] = field(default_factory=dict)  # python_name 기준
    pads: tuple[PadSpec, ...] = ()

    def get(self, name: str) -> PropertySpec | None:
        """python_name 또는 GStreamer 이름 어느 쪽으로도 조회."""
        return self.properties.get(to_python_name(name))

    @property
    def writable_properties(self) -> tuple[PropertySpec, ...]:
        return tuple(p for p in self.properties.values() if p.writable)

    def describe(self) -> str:
        lines = [
            f"{self.factory_name} — {self.long_name or self.description}",
            f"  klass: {self.klass}",
            "  properties:",
        ]
        lines += [f"    {p.describe()}" for p in self.properties.values()]
        if self.pads:
            lines.append("  pads:")
            lines += [f"    {p.direction:4s} {p.name} ({p.presence})" for p in self.pads]
        return "\n".join(lines)


# --------------------------------------------------------------------------

_lock = threading.RLock()
_specs: dict[str, ElementSpec] = {}

# GObject 가 모든 객체에 얹는 프로퍼티. 엘리먼트 고유 설정이 아니므로 제외한다.
_SKIP_PROPERTIES = {"name", "parent"}


def _kind_of(pspec) -> PropertyKind:
    vtype = pspec.value_type
    kind = _BOXED_KIND.get(vtype.name)
    if kind is not None:
        return kind
    return _FUNDAMENTAL_KIND.get(vtype.fundamental.name, PropertyKind.OTHER)


def _property_spec(pspec) -> PropertySpec:
    GObject = require("GObject")
    kind = _kind_of(pspec)

    enum_type: Any = None
    if kind is PropertyKind.ENUM:
        enum_type = enum_from_pspec(pspec)
    elif kind is PropertyKind.FLAGS:
        enum_type = flags_from_pspec(pspec)

    default = getattr(pspec, "default_value", None)
    if enum_type is not None and default is not None:
        try:
            default = enum_type(int(default))
        except (ValueError, TypeError):
            default = None

    flags = pspec.flags
    return PropertySpec(
        name=pspec.name,
        python_name=to_python_name(pspec.name),
        kind=kind,
        gtype=pspec.value_type.name,
        blurb=pspec.blurb or "",
        default=default,
        minimum=getattr(pspec, "minimum", None),
        maximum=getattr(pspec, "maximum", None),
        readable=bool(flags & GObject.ParamFlags.READABLE),
        writable=bool(flags & GObject.ParamFlags.WRITABLE),
        construct_only=bool(flags & GObject.ParamFlags.CONSTRUCT_ONLY),
        deprecated=bool(flags & GObject.ParamFlags.DEPRECATED),
        enum_type=enum_type,
    )


def inspect_element(factory_name: str) -> ElementSpec:
    """팩토리 이름 → ElementSpec. 결과는 캐시된다.

    Raises:
        UnknownElementError: 해당 팩토리가 설치되어 있지 않음.
    """
    with _lock:
        cached = _specs.get(factory_name)
        if cached is not None:
            return cached

    ensure_initialized()
    Gst = require("Gst")

    factory = Gst.ElementFactory.find(factory_name)
    if factory is None:
        raise UnknownElementError(factory_name, _suggest(factory_name))

    # 프로퍼티 목록은 인스턴스가 있어야 읽을 수 있다(클래스 초기화 필요).
    element = factory.create(None)
    if element is None:
        raise UnknownElementError(
            factory_name, [], detail="팩토리는 있지만 인스턴스를 만들 수 없습니다"
        )

    properties: dict[str, PropertySpec] = {}
    for pspec in element.list_properties():
        if pspec.name in _SKIP_PROPERTIES:
            continue
        prop = _property_spec(pspec)
        properties[prop.python_name] = prop

    pads = tuple(
        PadSpec(
            name=t.name_template,
            direction=t.direction.value_nick,
            presence=t.presence.value_nick,
            caps=t.get_caps().to_string() if t.get_caps() else "",
        )
        for t in factory.get_static_pad_templates()
    )

    element_spec = ElementSpec(
        factory_name=factory_name,
        long_name=factory.get_metadata(Gst.ELEMENT_METADATA_LONGNAME) or "",
        klass=factory.get_metadata(Gst.ELEMENT_METADATA_KLASS) or "",
        description=factory.get_metadata(Gst.ELEMENT_METADATA_DESCRIPTION) or "",
        properties=properties,
        pads=pads,
    )
    with _lock:
        _specs[factory_name] = element_spec
    return element_spec


def list_factories(klass_filter: str | None = None) -> list[str]:
    """설치된 엘리먼트 팩토리 이름 전부.

    레지스트리를 직접 읽는다. `ElementFactory.list_get_elements(TYPE_ANY, ...)`
    는 klass 가 미리 정의된 카테고리 비트에 매핑되지 않는 엘리먼트를 빠뜨린다
    (capsfilter, videoconvert, queue, tee, nvvidconv 등 300개 가까이).

    Args:
        klass_filter: 'Source/Video' 처럼 klass 문자열에 포함될 부분 문자열.
    """
    ensure_initialized()
    Gst = require("Gst")
    features = Gst.Registry.get().get_feature_list(Gst.ElementFactory)

    names = []
    for f in features:
        if klass_filter is not None:
            klass = f.get_metadata(Gst.ELEMENT_METADATA_KLASS) or ""
            if klass_filter.lower() not in klass.lower():
                continue
        names.append(f.get_name())
    return sorted(names)


def _suggest(name: str, limit: int = 5) -> list[str]:
    """오타 추정용 유사 이름."""
    import difflib

    try:
        return difflib.get_close_matches(name, list_factories(), n=limit, cutoff=0.6)
    except Exception:  # noqa: BLE001 - 제안은 실패해도 무방
        return []
