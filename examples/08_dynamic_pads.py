"""decodebin 의 동적 패드와 디코더 선택 제어.

    python3 examples/08_dynamic_pads.py [입력파일]

두 가지를 보여준다:

1. **pad-added** — decodebin 은 파일을 열어보기 전에는 스트림이 몇 개인지
   모른다. src 패드가 처음부터 있지 않고(presence=sometimes) 재생을 시작한
   뒤에 하나씩 생기므로 미리 link() 할 수 없다. 콜백에서 연결한다.

2. **autoplug-select** — decodebin 은 rank 가 가장 높은 디코더를 고른다.
   Jetson 에서는 nvv4l2decoder(rank primary+11)가 avdec_h264(primary)를
   이기는데, 스트림에 따라 이 하드웨어 디코더가 실패하는 경우가 있다.
   이 시그널로 특정 팩토리를 건너뛰게 만들 수 있다.

입력 파일이 없으면 이 예제가 직접 하나 만든다.
"""

import pathlib
import sys
import tempfile

from gstreamer_python_sdk import Pipeline, VideoCaps, require
from gstreamer_python_sdk.elements import (
    DecodeBin,
    FakeSink,
    FileSink,
    FileSrc,
    H264Parse,
    Mp4Mux,
    VideoConvert,
    VideoTestSrc,
    X264Enc,
)

# GstAutoplugSelectResult — decodebin 이 동적으로 등록하는 enum 이라 typelib 에
# 없다. 정수로 그대로 돌려주면 된다.
AUTOPLUG_TRY, AUTOPLUG_EXPOSE, AUTOPLUG_SKIP = 0, 1, 2

# 이 시스템에서 문제를 일으키는 디코더. 비워두면 GStreamer 기본 선택을 따른다.
SKIP_DECODERS = {"nvv4l2decoder"}


def make_sample(path: pathlib.Path) -> None:
    """테스트용 MP4 를 하나 만든다."""
    print(f"입력 파일 생성 중: {path}")
    pipeline = Pipeline()
    pipeline.build(
        VideoTestSrc(num_buffers=60),
        VideoCaps(width=640, height=480, framerate=30),
        VideoConvert(),
        X264Enc(tune=X264Enc.Tune.ZEROLATENCY),
        H264Parse(),
        Mp4Mux(),
        FileSink(location=str(path)),
    )
    with pipeline:
        pipeline.wait_eos(timeout=60)


def main() -> None:
    if len(sys.argv) > 1:
        source = pathlib.Path(sys.argv[1])
    else:
        source = pathlib.Path(tempfile.gettempdir()) / "sdk_dynamic_input.mp4"
        if not source.exists():
            make_sample(source)

    Gst = require("Gst")  # 패드 caps 와 링크 결과를 직접 볼 때만 필요하다

    src = FileSrc(location=str(source))
    decode = DecodeBin()
    conv = VideoConvert()
    sink = FakeSink(sync=False)

    pipeline = Pipeline(name="dynamic-pads")
    pipeline.add(src, decode, conv, sink)

    # 정적으로 연결 가능한 부분만 미리 연결한다. decodebin 의 출력은 아직 없다.
    pipeline.link(src, decode)
    pipeline.link(conv, sink)

    chosen: list[str] = []
    linked = False

    def on_autoplug_select(_bin, _pad, _caps, factory) -> int:
        """decodebin 이 엘리먼트를 하나 붙이려 할 때마다 물어본다."""
        name = factory.get_name()
        if name in SKIP_DECODERS:
            print(f"  [autoplug] {name} 건너뜀 → 다음 후보로")
            return AUTOPLUG_SKIP
        chosen.append(name)
        print(f"  [autoplug] {name} 채택")
        return AUTOPLUG_TRY

    def on_pad_added(_element, pad) -> None:
        """decodebin 이 디코딩된 스트림을 노출할 때마다 호출된다."""
        nonlocal linked
        caps = pad.get_current_caps() or pad.query_caps(None)
        media = caps.get_structure(0).get_name()

        if not media.startswith("video/") or linked:
            print(f"  [pad-added] {pad.get_name()} ({media}) → 건너뜀")
            return

        result = pad.link(conv.pad("sink"))
        if result == Gst.PadLinkReturn.OK:
            linked = True
            print(f"  [pad-added] {pad.get_name()} ({media}) → videoconvert 에 연결")
        else:
            print(f"  [pad-added] 연결 실패: {result.value_nick}")

    decode.on("autoplug-select", on_autoplug_select)
    decode.on("pad-added", on_pad_added)

    print(f"디코딩: {source}")
    with pipeline:
        pipeline.wait_eos(timeout=60)

    print(f"\n실제로 사용된 엘리먼트: {' → '.join(chosen)}")
    print(f"최종 체인: {' → '.join(e.factory_name for e in pipeline.ordered())}")


if __name__ == "__main__":
    main()
