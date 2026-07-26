"""introspection 결과 → .pyi 타입 스텁 생성기.

런타임은 동적이므로 이 스텁이 없어도 동작한다. 스텁은 IDE 자동완성과
mypy 를 위한 것이다.

    python -m gstreamer_python_sdk.codegen              # 큐레이션된 것만
    python -m gstreamer_python_sdk.codegen --all        # 설치된 전부 (느리고 큼)
    python -m gstreamer_python_sdk.codegen --include compositor,rtspclientsink

스텁은 이 시스템에 설치된 GStreamer 를 그대로 반영한다. 다른 머신(예: x86
개발 PC ↔ Jetson)에서는 다시 생성해야 정확하다.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable

from ._bootstrap import gst_version_string, init
from .elements import CURATED
from .enums import GstEnum, GstFlags
from .errors import UnknownElementError
from .introspect import ElementSpec, PropertyKind, PropertySpec, inspect_element, list_factories

__all__ = ["generate", "write_stub", "main"]

_HEADER = '''"""자동 생성된 타입 스텁 — 직접 수정하지 마세요.

    python -m gstreamer_python_sdk.codegen

생성 환경: {version}
엘리먼트 {count}개
"""

from fractions import Fraction
from typing import Any, ClassVar

from ..caps import Caps
from ..element import Element, Prop
from ..enums import GstEnum, GstFlags
from ..introspect import ElementSpec

CURATED: dict[str, str]

def make(class_name: str, factory_name: str) -> type[Element]: ...
def available() -> dict[str, str]: ...
def _nested_enums(class_name: str, spec: ElementSpec) -> dict[str, Any]: ...
'''


def _docstring(text: str, indent: str) -> list[str]:
    """따옴표 충돌 없이 docstring 블록을 만든다."""
    safe = text.replace("\\", "\\\\").replace('"""', "'''")
    lines = safe.splitlines() or [""]
    if len(lines) == 1:
        return [f'{indent}"""{lines[0]}"""']
    out = [f'{indent}"""{lines[0]}']
    out += [f"{indent}{line}" if line else "" for line in lines[1:]]
    out.append(f'{indent}"""')
    return out


def _enum_block(enum_type: type[GstEnum] | type[GstFlags]) -> list[str]:
    base = "GstFlags" if issubclass(enum_type, GstFlags) else "GstEnum"
    lines = [f"class {enum_type.__name__}({base}):"]
    gtype = getattr(enum_type, "__gtype_name__", enum_type.__name__)
    lines += _docstring(gtype, "    ")
    # 값을 반드시 대입해야 한다. `NAME: int` 는 타이핑 스펙상 enum 멤버가 아니라
    # 단순 애노테이션으로 해석되어 타입 검사기가 멤버로 인식하지 못한다.
    for member in enum_type:
        lines.append(f"    {member.name} = {int(member)}  # {member.nick}")
    lines.append("")
    return lines


def _default_repr(prop: PropertySpec) -> str:
    """스텁의 기본값은 항상 `...` 이지만, 주석으로 실제 기본값을 남긴다."""
    if prop.default is None:
        return ""
    if isinstance(prop.default, (GstEnum, GstFlags)):
        return f"  # 기본값: {prop.default.nick}"
    return f"  # 기본값: {prop.default!r}"


def _element_block(class_name: str, spec: ElementSpec) -> list[str]:
    lines = [f"class {class_name}(Element):"]

    doc = [f"{spec.factory_name} — {spec.long_name or spec.description}", ""]
    if spec.klass:
        doc.append(f"klass: {spec.klass}")
    pads = [f"{p.direction} {p.name} ({p.presence})" for p in spec.pads]
    if pads:
        doc.append("pads: " + ", ".join(pads))
    lines += _docstring("\n".join(doc), "    ")

    # Element.FACTORY 는 ClassVar 다. 스텁에서 일반 속성으로 다시 선언하면
    # "클래스 변수를 인스턴스 변수로 덮어쓴다"는 오류가 난다.
    lines.append(f'    FACTORY: ClassVar[str]  # "{spec.factory_name}"')

    # 중첩 enum 별칭 (VideoTestSrc.Pattern)
    from .elements import _nested_enums

    for short, enum_type in sorted(_nested_enums(class_name, spec).items()):
        if short != enum_type.__name__:
            lines.append(f"    {short} = {enum_type.__name__}")

    # 프로퍼티 속성 선언 (읽기/쓰기 모두)
    body = False
    for prop in spec.properties.values():
        if not prop.python_name.isidentifier():
            continue
        lines.append(f"    {prop.python_name}: {prop.attr_hint()}{_default_repr(prop)}")
        body = True
    if body:
        lines.append("")

    # __init__ 시그니처 (쓰기 가능한 것만)
    params = ["self", "*", "name: str | None = ..."]
    for prop in spec.writable_properties:
        if not prop.python_name.isidentifier():
            continue
        params.append(f"{prop.python_name}: {prop.hint()} = ...")
    if len(params) <= 3:
        lines.append(f"    def __init__({', '.join(params)}) -> None: ...")
    else:
        lines.append("    def __init__(")
        lines += [f"        {p}," for p in params]
        lines.append("    ) -> None: ...")
    lines.append("")
    return lines


def generate(targets: dict[str, str]) -> tuple[str, list[str]]:
    """{클래스 이름: 팩토리 이름} → (.pyi 내용, 건너뛴 엘리먼트 목록)."""
    init()

    specs: list[tuple[str, ElementSpec]] = []
    skipped: list[str] = []
    for class_name, factory_name in sorted(targets.items()):
        try:
            specs.append((class_name, inspect_element(factory_name)))
        except UnknownElementError:
            skipped.append(f"{class_name} ({factory_name})")

    # enum 은 여러 엘리먼트가 공유할 수 있으므로 이름 기준으로 한 번만 낸다.
    enums: dict[str, type] = {}
    for _, spec in specs:
        for prop in spec.properties.values():
            if prop.enum_type is not None:
                existing = enums.get(prop.enum_type.__name__)
                if existing is None:
                    enums[prop.enum_type.__name__] = prop.enum_type
                elif existing is not prop.enum_type:
                    # 서로 다른 GType 이 같은 이름으로 매핑된 경우 — 런타임 클래스
                    # 이름이 실제로 같으므로 스텁도 하나만 유지한다.
                    pass

    out = [_HEADER.format(version=gst_version_string(), count=len(specs))]
    if skipped:
        out.append("# 이 시스템에 설치되지 않아 제외됨:")
        out += [f"#   {s}" for s in skipped]
        out.append("")

    for name in sorted(enums):
        out += _enum_block(enums[name])
    for class_name, spec in specs:
        out += _element_block(class_name, spec)

    return "\n".join(out), skipped


def write_stub(targets: dict[str, str], output: Path) -> tuple[Path, list[str]]:
    content, skipped = generate(targets)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")

    marker = output.parent.parent / "py.typed"
    if not marker.exists():
        marker.write_text("", encoding="utf-8")
    return output, skipped


def _pascal(factory_name: str) -> str:
    return "".join(p.capitalize() for p in factory_name.replace(".", "_").split("_") if p)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m gstreamer_python_sdk.codegen",
        description="설치된 GStreamer 를 introspect 해서 .pyi 타입 스텁을 만듭니다.",
    )
    parser.add_argument(
        "--all", action="store_true", help="설치된 엘리먼트 전부 (수 MB, IDE 가 느려질 수 있음)"
    )
    parser.add_argument("--include", default="", help="추가할 팩토리 이름 (쉼표 구분)")
    parser.add_argument("--output", type=Path, default=None, help="출력 경로 (.pyi)")
    args = parser.parse_args(list(argv) if argv is not None else None)

    targets = dict(CURATED)
    if args.all:
        targets.update({_pascal(f): f for f in list_factories()})
    for name in filter(None, (n.strip() for n in args.include.split(","))):
        targets[_pascal(name)] = name

    output = args.output or Path(__file__).parent / "elements" / "__init__.pyi"
    path, skipped = write_stub(targets, output)

    print(f"생성: {path} ({len(targets) - len(skipped)}개 엘리먼트)")
    if skipped:
        print(f"제외(미설치) {len(skipped)}개: {', '.join(skipped)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
