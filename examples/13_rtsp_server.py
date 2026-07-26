"""RTSP 서버로 스트리밍하기.

    python3 examples/13_rtsp_server.py                  # 테스트 패턴 송출
    python3 examples/13_rtsp_server.py --device /dev/video0
    python3 examples/13_rtsp_server.py --port 8555 --hardware

    # 다른 터미널에서
    gst-play-1.0 rtsp://<ip>:8554/live
    ffplay -rtsp_transport tcp rtsp://<ip>:8554/live

GstRtspServer 의 `set_launch()` 는 gst-launch 문자열만 받는다. SDK 가
`launch_string()` 으로 데이터모델을 직렬화해 주므로 여기서는 계속 엘리먼트
객체로만 다룬다.

**규칙**: 각 경로의 마지막 payloader 이름은 반드시 `pay0` 이어야 한다.
GstRtspServer 가 그 이름으로 RTP 스트림을 찾는다.

`gir1.2-gst-rtsp-server-1.0` 패키지가 필요하며, 없으면 안내 후 종료한다.
"""

import argparse
import sys

from gstreamer_python_sdk import GstSdkError, VideoCaps, VideoFormat, launch_string
from gstreamer_python_sdk.elements import (
    RtpH264Pay,
    V4l2Src,
    VideoConvert,
    VideoTestSrc,
    X264Enc,
)

WIDTH, HEIGHT, FPS = 640, 480, 30


def build_route(device: str | None, hardware: bool) -> list:
    """송출할 파이프라인을 엘리먼트 목록으로 만든다."""
    source = V4l2Src(device=device) if device else VideoTestSrc(is_live=True)
    raw = VideoCaps(format=VideoFormat.I420, width=WIDTH, height=HEIGHT, framerate=FPS)

    if hardware:
        # Jetson 하드웨어 인코더 경로 — NVMM 버퍼를 거쳐야 한다.
        from gstreamer_python_sdk import Memory
        from gstreamer_python_sdk.elements import NvV4l2H264Enc, NvVidConv

        return [
            source,
            raw,
            NvVidConv(),
            VideoCaps(format=VideoFormat.NV12, width=WIDTH, height=HEIGHT, memory=Memory.NVMM),
            NvV4l2H264Enc(bitrate=2_000_000, insert_sps_pps=True, iframeinterval=FPS),
            RtpH264Pay(name="pay0", pt=96, config_interval=1),
        ]

    return [
        source,
        raw,
        VideoConvert(),
        X264Enc(bitrate=1500, tune=X264Enc.Tune.ZEROLATENCY, key_int_max=FPS),
        RtpH264Pay(name="pay0", pt=96, config_interval=1),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="RTSP 서버 예제")
    parser.add_argument("--port", type=int, default=8554)
    parser.add_argument("--path", default="/live")
    parser.add_argument("--device", default=None, help="V4L2 카메라 (예: /dev/video0)")
    parser.add_argument("--hardware", action="store_true", help="Jetson NVENC 사용")
    parser.add_argument(
        "--dry-run", action="store_true", help="서버를 띄우지 않고 launch 문자열만 출력"
    )
    args = parser.parse_args()

    items = build_route(args.device, args.hardware)

    # 데이터모델이 어떤 gst-launch 문자열이 되는지 — 서버가 실제로 받는 값이다.
    print("launch 문자열:")
    print(f"  ( {launch_string(*items)} )\n")
    if args.dry_run:
        return 0

    try:
        from gstreamer_python_sdk import RtspServer

        server = RtspServer(port=args.port)
        server.add_route(args.path, *items, shared=True)
    except GstSdkError as e:
        print("RTSP 서버를 시작할 수 없습니다.\n")
        print(e)
        print("\n--dry-run 으로 launch 문자열만 확인할 수 있습니다.")
        return 1

    server.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
