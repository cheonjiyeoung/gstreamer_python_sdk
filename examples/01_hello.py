"""가장 단순한 파이프라인 — 문자열 없이 조립하기.

    python3 examples/01_hello.py

gst-launch-1.0 로는 이것과 같다:
    gst-launch-1.0 videotestsrc num-buffers=60 ! videoconvert ! fakesink
"""

from gstreamer_python_sdk import Pipeline
from gstreamer_python_sdk.elements import FakeSink, VideoConvert, VideoTestSrc


def main() -> None:
    src = VideoTestSrc(num_buffers=60)
    conv = VideoConvert()
    sink = FakeSink(sync=False)

    pipeline = Pipeline(name="hello")
    pipeline.add(src, conv, sink)
    pipeline.link(src, conv, sink)

    print("조립:", " → ".join(e.factory_name for e in pipeline.ordered()))

    # with 블록: 진입 시 PLAYING, 이탈 시 예외 여부와 관계없이 NULL 로 내려간다.
    with pipeline:
        print("재생 중...")
        pipeline.wait_eos(timeout=10)

    print("완료:", pipeline)


if __name__ == "__main__":
    main()
