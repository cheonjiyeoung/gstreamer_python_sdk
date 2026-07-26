"""메인루프로 녹화하고 Ctrl+C 로 안전하게 끝내기.

    python3 examples/11_mainloop_recording.py                 # Ctrl+C 로 종료
    python3 examples/11_mainloop_recording.py --seconds 5     # 5초 뒤 자동 종료
    python3 examples/11_mainloop_recording.py --output out.mp4

녹화 중 Ctrl+C 를 그냥 받으면 프로세스가 죽으면서 mp4mux 가 moov atom 을
쓰지 못해 재생 불가능한 파일이 남는다. `run_pipeline()` 은 인터럽트를 받으면
곧바로 죽지 않고

    EOS 전송 → mux 가 헤더를 씀 → EOS 가 filesink 에 도달 → NULL 로 내림

순서를 밟는다. 한 번 더 누르면 즉시 중단한다.
"""

import argparse
import pathlib

from gstreamer_python_sdk import Pipeline, VideoCaps, VideoFormat, run_pipeline
from gstreamer_python_sdk.elements import (
    FileSink,
    H264Parse,
    Mp4Mux,
    VideoConvert,
    VideoTestSrc,
    X264Enc,
)

FPS = 30


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", default="/tmp/sdk_recording.mp4")
    parser.add_argument(
        "--seconds", type=float, default=None, help="지정하면 그 시간 뒤 자동으로 EOS"
    )
    args = parser.parse_args()
    out = pathlib.Path(args.output)

    # is_live=True — 실제 카메라처럼 실시간으로 프레임을 낸다. num_buffers 를
    # 주지 않았으므로 EOS 는 우리가 보내야만 온다.
    src = VideoTestSrc(is_live=True, pattern=VideoTestSrc.Pattern.BALL)
    conv = VideoConvert()
    enc = X264Enc(bitrate=2000, tune=X264Enc.Tune.ZEROLATENCY, key_int_max=FPS)
    parse, mux, sink = H264Parse(), Mp4Mux(), FileSink(location=str(out))

    pipeline = Pipeline(name="recording")
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

    print(f"녹화: {out}")
    if args.seconds is None:
        print("Ctrl+C 를 누르면 파일을 정상 마무리하고 종료합니다.")

    # 진행 상황 표시 — 메인루프가 도는 동안 버스 메시지가 계속 들어온다.
    def on_message(msg) -> None:
        if msg.type_name == "warning":
            print(f"  경고: {msg}")

    run_pipeline(pipeline, seconds=args.seconds, on_message=on_message)

    size = out.stat().st_size if out.exists() else 0
    print(f"저장 완료: {out} ({size:,} bytes)")
    print(f"확인: gst-discoverer-1.0 {out}")


if __name__ == "__main__":
    main()
