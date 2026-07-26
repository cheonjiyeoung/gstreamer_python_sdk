"""파이프라인 그래프 보기.

    python3 examples/14_graph.py [출력.png]

세 가지 방법이 있고 필요한 것이 다르다.

* `diagram()`    — 의존성 없음. 터미널용. 협상된 caps 까지 보여준다.
* `to_dot()`     — Graphviz DOT 텍스트. GStreamer 가 만들어 준다.
* `save_graph()` — DOT 를 PNG/SVG 로 렌더링. `sudo apt install graphviz` 필요.

diagram() 은 NULL 상태에서는 패드 템플릿만, PLAYING 상태에서는 실제로
협상된 caps 를 보여준다. 협상 문제를 추적할 때 이 차이가 핵심이다.
"""

import pathlib
import sys

from gstreamer_python_sdk import GstSdkError, Pipeline, VideoCaps, VideoFormat
from gstreamer_python_sdk.elements import FakeSink, VideoConvert, VideoScale, VideoTestSrc


def main() -> None:
    src = VideoTestSrc(num_buffers=30, pattern=VideoTestSrc.Pattern.SMPTE)
    pipeline = Pipeline(name="graph-demo")
    pipeline.build(
        src,
        VideoCaps(format=VideoFormat.I420, width=640, height=480, framerate=30),
        VideoScale(),
        VideoCaps(width=320, height=240),
        VideoConvert(),
        VideoCaps(format=VideoFormat.RGB),
        FakeSink(sync=False),
    )

    print("=== NULL 상태 — 아직 협상 전 ===")
    print(pipeline.diagram())

    with pipeline:
        print("\n=== PLAYING 상태 — 실제 협상된 caps ===")
        print(pipeline.diagram())
        dot = pipeline.to_dot()
        pipeline.wait_eos(timeout=30)

    print(f"\nDOT 텍스트: {len(dot):,} 자")

    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/sdk_graph.png")
    try:
        saved = pipeline.save_graph(out)
        print(f"이미지 저장: {saved} ({saved.stat().st_size:,} bytes)")
    except GstSdkError as e:
        print(f"\n이미지 렌더링 건너뜀:\n{e}")


if __name__ == "__main__":
    main()
