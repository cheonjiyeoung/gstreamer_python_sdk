"""소프트웨어 인코딩으로 MP4 파일 만들기.

    python3 examples/05_encode_file.py [출력경로]

녹화에서 중요한 것: 파일을 정상적으로 마무리하려면 EOS 가 mux 를 거쳐
filesink 까지 도달해야 한다. 그냥 NULL 로 내려버리면 moov atom 이 없는
깨진 파일이 남는다. num-buffers 로 소스가 스스로 EOS 를 보내게 하거나,
`pipeline.send_eos()` 를 부른 뒤 wait_eos() 로 기다린다.
"""

import pathlib
import sys

from gstreamer_python_sdk import Pipeline, VideoCaps, VideoFormat
from gstreamer_python_sdk.elements import (
    FileSink,
    H264Parse,
    Mp4Mux,
    VideoConvert,
    VideoTestSrc,
    X264Enc,
)

FPS = 30
SECONDS = 3


def main() -> None:
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/sdk_sw_encode.mp4")

    src = VideoTestSrc(num_buffers=FPS * SECONDS, pattern=VideoTestSrc.Pattern.SMPTE)
    conv = VideoConvert()
    # zerolatency 튜닝 + 2Mbps. tune 은 flags 라 '|' 로 조합할 수도 있다.
    enc = X264Enc(bitrate=2000, tune=X264Enc.Tune.ZEROLATENCY, key_int_max=FPS)
    parse = H264Parse()
    mux = Mp4Mux()
    sink = FileSink(location=str(out))

    pipeline = Pipeline(name="sw-encode")
    pipeline.add(src, conv, enc, parse, mux, sink)
    pipeline.link(
        src,
        VideoCaps(format=VideoFormat.I420, width=640, height=480, framerate=FPS),
        conv,
        enc,
        parse,
        mux,
        sink,
    )

    print("조립:", " → ".join(e.factory_name for e in pipeline.ordered()))
    print(f"인코딩 중... ({SECONDS}초 분량)")

    with pipeline:
        # 소스가 num_buffers 를 다 내보내면 스스로 EOS 를 보낸다.
        pipeline.wait_eos(timeout=60)

    print(f"완료: {out} ({out.stat().st_size:,} bytes)")
    print(f"확인: gst-discoverer-1.0 {out}")


if __name__ == "__main__":
    main()
