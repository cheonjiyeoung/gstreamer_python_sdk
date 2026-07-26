"""Jetson 하드웨어(NVENC) 인코딩 — NVMM 메모리 caps 사용.

    python3 examples/06_jetson_hw_encode.py [출력경로]

Jetson 의 nvv4l2* 엘리먼트는 시스템 메모리가 아니라 NVMM 버퍼를 요구한다.
그 요구사항을 `VideoCaps(..., memory=Memory.NVMM)` 으로 표현한다.

nvv4l2h264enc 가 없는 환경(x86 등)에서는 안내 후 종료한다.
"""

import pathlib
import sys

from gstreamer_python_sdk import Memory, Pipeline, UnknownElementError, VideoCaps, VideoFormat

FPS = 30
SECONDS = 3


def main() -> int:
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/sdk_hw_encode.mp4")

    try:
        from gstreamer_python_sdk.elements import (
            FileSink,
            H264Parse,
            Mp4Mux,
            NvV4l2H264Enc,
            NvVidConv,
            VideoTestSrc,
        )

        enc = NvV4l2H264Enc(
            bitrate=4_000_000,
            preset_level=NvV4l2H264Enc.PresetLevel.FASTPRESET,
            control_rate=NvV4l2H264Enc.ControlRate.CONSTANT_BITRATE,
            iframeinterval=FPS,
            insert_sps_pps=True,
        )
        conv = NvVidConv()
    except UnknownElementError as e:
        print("이 시스템에는 Jetson 하드웨어 인코더가 없습니다.\n")
        print(e)
        print("\n소프트웨어 인코딩은 05_encode_file.py 를 보세요.")
        return 1

    src = VideoTestSrc(num_buffers=FPS * SECONDS, pattern=VideoTestSrc.Pattern.BALL)
    parse, mux, sink = H264Parse(), Mp4Mux(), FileSink(location=str(out))

    pipeline = Pipeline(name="jetson-hw-encode")
    pipeline.add(src, conv, enc, parse, mux, sink)
    pipeline.link(
        src,
        VideoCaps(format=VideoFormat.I420, width=1280, height=720, framerate=FPS),
        conv,
        # nvvidconv 출력을 NVMM 으로 — 이게 없으면 인코더와 협상이 실패한다.
        VideoCaps(format=VideoFormat.NV12, width=1280, height=720, memory=Memory.NVMM),
        enc,
        parse,
        mux,
        sink,
    )

    print("조립:", " → ".join(e.factory_name for e in pipeline.ordered()))
    print(f"설정: {enc.bitrate // 1000} kbps, preset={enc.preset_level.nick}")
    print(f"NVENC 인코딩 중... ({SECONDS}초 분량)")

    with pipeline:
        pipeline.wait_eos(timeout=60)

    print(f"완료: {out} ({out.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
