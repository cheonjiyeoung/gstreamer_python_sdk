"""tee 로 스트림 분기하기 — 요청(request) 패드 다루기.

    python3 examples/07_tee_branch.py

                        ┌ queue → videoconvert → fakesink   (미리보기 대용)
    videotestsrc → tee ─┤
                        └ queue → jpegenc → multifilesink   (스냅샷 저장)

tee 의 src 패드는 미리 존재하지 않고 요청해야 생긴다. 각 분기 바로 뒤에
queue 를 두지 않으면 한쪽이 막힐 때 전체가 멈춘다.
"""

import pathlib
import tempfile

from gstreamer_python_sdk import Element, Pipeline, VideoCaps
from gstreamer_python_sdk.elements import FakeSink, JpegEnc, Queue, Tee, VideoConvert, VideoTestSrc


def main() -> None:
    outdir = pathlib.Path(tempfile.mkdtemp(prefix="sdk_tee_"))

    src = VideoTestSrc(num_buffers=30, pattern=VideoTestSrc.Pattern.BALL)
    tee = Tee(name="t")

    # 분기 1 — 그냥 버린다(실제로는 화면 출력이 들어갈 자리)
    q1, conv1, sink1 = Queue(), VideoConvert(), FakeSink(sync=False)

    # 분기 2 — JPEG 로 저장
    q2, conv2, enc = Queue(), VideoConvert(), JpegEnc()
    sink2 = Element("multifilesink", location=str(outdir / "frame_%03d.jpg"))

    pipeline = Pipeline(name="tee-demo")
    pipeline.add(src, tee, q1, conv1, sink1, q2, conv2, enc, sink2)

    # 소스 → tee
    pipeline.link(src, VideoCaps(width=320, height=240, framerate=30), tee)
    # 각 분기 내부 연결
    pipeline.link(q1, conv1, sink1)
    pipeline.link(q2, conv2, enc, sink2)

    # tee 의 요청 패드를 각 분기의 queue 에 연결한다. 템플릿 이름('src_%u')을
    # 주면 GStreamer 가 패드를 알아서 하나씩 새로 만들어 준다.
    for queue in (q1, q2):
        pipeline.link_pads(tee, "src_%u", queue, "sink")
        print(f"  tee.src_%u → {queue.name}.sink")

    with pipeline:
        pipeline.wait_eos(timeout=30)

    files = sorted(outdir.glob("*.jpg"))
    print(f"\n저장된 JPEG: {len(files)}개 → {outdir}")
    if files:
        print(f"  예: {files[0].name} ({files[0].stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
