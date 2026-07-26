"""파이프라인 그래프 보기.

세 가지 방법이 있고, 필요한 것이 서로 다르다.

* `diagram()` — 의존성 없음. 터미널용 텍스트. 협상된 caps 까지 보여준다.
* `to_dot()` — Graphviz DOT 텍스트. GStreamer 가 만들어 준다.
* `save_graph()` — DOT 를 PNG/SVG 로 렌더링. `graphviz` 패키지(dot) 필요.

`diagram()` 은 PLAYING 상태에서 부르면 실제로 협상된 caps 가 나오고, NULL
상태에서는 패드 템플릿만 보인다. 협상 문제를 볼 때는 재생 중에 부를 것.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from ._bootstrap import require
from .errors import GstSdkError

__all__ = ["diagram", "to_dot", "save_graph"]

_MAX_CAPS = 78


def to_dot(pipeline: Any, path: str | Path | None = None) -> str:
    """Graphviz DOT 텍스트. path 를 주면 파일로도 쓴다."""
    Gst = require("Gst")
    text = Gst.debug_bin_to_dot_data(pipeline.gst, Gst.DebugGraphDetails.ALL)
    if path is not None:
        Path(path).write_text(text, encoding="utf-8")
    return text


def save_graph(pipeline: Any, path: str | Path, image_format: str | None = None) -> Path:
    """DOT 를 이미지로 렌더링한다.

    Args:
        path: 출력 경로. 확장자로 형식을 정한다(.png, .svg, .pdf ...).
        image_format: 확장자 대신 형식을 직접 지정.

    Raises:
        GstSdkError: graphviz 가 설치되어 있지 않거나 dot 실행이 실패했을 때.
    """
    out = Path(path)
    fmt = image_format or out.suffix.lstrip(".") or "png"

    dot = shutil.which("dot")
    if dot is None:
        raise GstSdkError(
            "graphviz 가 필요합니다 (dot 명령을 찾을 수 없음).\n"
            "  sudo apt install graphviz\n"
            "  설치 없이 보려면 pipeline.diagram() 또는 pipeline.to_dot() 을 쓰세요."
        )

    out.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [dot, f"-T{fmt}", "-o", str(out)],
        input=to_dot(pipeline).encode("utf-8"),
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise GstSdkError(
            f"dot 실행 실패 (코드 {result.returncode}): "
            f"{result.stderr.decode('utf-8', 'replace').strip()}"
        )
    return out


def diagram(pipeline: Any, *, show_caps: bool = True) -> str:
    """소스 → 싱크 순서의 텍스트 다이어그램.

        videotestsrc0  (videotestsrc)
            │ video/x-raw, format=I420, width=320, height=240, framerate=30/1
        capsfilter0  (capsfilter)
            │ ...
        fakesink0  (fakesink)
    """
    elements = pipeline.ordered()
    if not elements:
        return f"{pipeline.name}: <비어 있음>"

    lines = [f"{pipeline.name} [{pipeline.state.value_nick}]"]
    for index, element in enumerate(elements):
        lines.append(f"  {element.name}  ({element.factory_name})")
        if not show_caps or index == len(elements) - 1:
            continue
        caps = _outgoing_caps(element)
        lines.append(f"      │ {caps}" if caps else "      │")
    return "\n".join(lines)


def _outgoing_caps(element: Any) -> str:
    """이 엘리먼트의 src 패드에서 나가는 caps. 협상 전이면 템플릿을 보여준다."""
    gst_element = element.gst
    pad = gst_element.get_static_pad("src")
    if pad is None:
        # tee 처럼 요청 패드만 있는 경우 — 붙어 있는 것 중 하나를 고른다
        pads = [p for p in gst_element.pads if p.get_direction().value_nick == "src"]
        pad = pads[0] if pads else None
    if pad is None:
        return ""

    caps = pad.get_current_caps()
    negotiated = caps is not None
    if caps is None:
        caps = pad.query_caps(None)
    if caps is None:
        return ""

    # 사람이 읽는 용도라 '(int)', '(string)' 같은 타입 표기는 지운다.
    # 'video/x-raw(memory:NVMM)' 의 feature 표기는 '=' 뒤가 아니라 건드리지 않는다.
    text = re.sub(r"=\((?:int|uint|string|boolean|fraction|double|float|long)\)", "=", caps.to_string())
    if not negotiated:
        text = f"(미협상) {text}"
    return text if len(text) <= _MAX_CAPS else text[: _MAX_CAPS - 3] + "..."
