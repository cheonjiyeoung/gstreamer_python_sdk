"""Caps 를 문자열이 아니라 데이터모델로.

    python3 examples/03_caps.py

`"video/x-raw,format=NV12,width=1920,..."` 대신 VideoCaps(...) 를 쓴다.
Pipeline.link() 중간에 끼우면 capsfilter 가 자동으로 생성되어 삽입된다.
"""

from gstreamer_python_sdk import (
    AudioCaps,
    Caps,
    Fraction,
    IntRange,
    Memory,
    Options,
    Pipeline,
    VideoCaps,
    VideoFormat,
)
from gstreamer_python_sdk.elements import FakeSink, VideoConvert, VideoTestSrc


def main() -> None:
    print("--- 데이터모델 → caps 문자열 ---")
    print(" 기본     :", VideoCaps(format=VideoFormat.NV12, width=1920, height=1080, framerate=30))
    print(" NVMM     :", VideoCaps(width=1920, height=1080, memory=Memory.NVMM))
    print(" 범위     :", VideoCaps(width=IntRange(320, 1920), framerate=Fraction(30000, 1001)))
    print(" 택일     :", Caps("video/x-h264", alignment=Options("au", "nal")))
    print(" 오디오   :", AudioCaps(rate=48000, channels=2))

    print("\n--- 문자열에서 되읽기 ---")
    parsed = Caps.from_string("video/x-raw(memory:NVMM),format=NV12,width=1280,height=720")
    print(" media_type:", parsed.media_type)
    print(" features  :", parsed.features)
    print(" fields    :", parsed.fields)

    print("\n--- link() 중간에 넣으면 capsfilter 가 자동 생성된다 ---")
    src, conv, sink = VideoTestSrc(num_buffers=30), VideoConvert(), FakeSink(sync=False)
    pipeline = Pipeline(name="caps-demo")
    pipeline.add(src, conv, sink)
    pipeline.link(
        src,
        VideoCaps(format=VideoFormat.I420, width=320, height=240, framerate=30),
        conv,
        sink,
    )
    print(" 조립:", " → ".join(e.factory_name for e in pipeline.ordered()))

    with pipeline:
        pipeline.wait_eos(timeout=10)
    print(" 완료")


if __name__ == "__main__":
    main()
