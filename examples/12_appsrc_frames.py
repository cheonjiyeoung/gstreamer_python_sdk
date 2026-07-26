"""직접 만든 프레임을 파이프라인에 밀어 넣기 (appsrc).

    python3 examples/12_appsrc_frames.py [출력경로]

`FrameSource` 는 caps 를 보고 프레임 하나가 몇 바이트여야 하는지, numpy
배열이라면 어떤 모양이어야 하는지 알려준다. 크기가 어긋난 채로 넣으면
GStreamer 깊은 곳에서 알아보기 어려운 오류가 나므로 push 시점에 막는다.
"""

import pathlib
import sys

import numpy as np

from gstreamer_python_sdk import FrameSource, Pipeline, VideoCaps, VideoFormat
from gstreamer_python_sdk.elements import FileSink, H264Parse, Mp4Mux, VideoConvert, X264Enc

WIDTH, HEIGHT, FPS, SECONDS = 320, 240, 30, 3


def make_frame(index: int) -> np.ndarray:
    """움직이는 그라디언트 + 세로 막대. 순수 numpy 로 만든 프레임."""
    x = np.linspace(0, 255, WIDTH, dtype=np.uint8)
    frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    frame[:, :, 0] = x                                    # R: 가로 그라디언트
    frame[:, :, 1] = np.linspace(0, 255, HEIGHT, dtype=np.uint8)[:, None]  # G: 세로
    bar = (index * 4) % WIDTH
    frame[:, bar : bar + 8, 2] = 255                      # B: 움직이는 막대
    return frame


def main() -> None:
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/sdk_appsrc.mp4")

    caps = VideoCaps(format=VideoFormat.RGB, width=WIDTH, height=HEIGHT, framerate=FPS)
    src = FrameSource(caps, name="frames")

    print(f"caps        : {caps}")
    print(f"프레임 크기 : {src.frame_bytes:,} bytes")
    print(f"배열 모양   : {src.shape}")

    pipeline = Pipeline(name="appsrc-demo")
    pipeline.build(
        src,
        VideoConvert(),
        X264Enc(bitrate=1500, tune=X264Enc.Tune.ZEROLATENCY),
        H264Parse(),
        Mp4Mux(),
        FileSink(location=str(out)),
    )

    # 크기가 틀리면 push 전에 걸린다.
    from gstreamer_python_sdk import GstSdkError

    try:
        src.push(np.zeros((10, 10, 3), dtype=np.uint8))
    except GstSdkError as e:
        print(f"\n크기 검증  : {e}")

    total = FPS * SECONDS
    print(f"\n{total} 프레임 공급 중...")

    # `with pipeline:` 을 쓰면 안 된다. appsrc 는 첫 버퍼가 들어와야 preroll 이
    # 끝나는데 그 버퍼는 우리가 넣어야 하므로, 상태 전이 완료를 기다리면 서로를
    # 기다리다 타임아웃이 난다. timeout=0 으로 비동기 전이만 시작해 둔다.
    pipeline.play(timeout=0)
    try:
        for i in range(total):
            src.push(make_frame(i))
        src.end()                       # EOS — 이게 없으면 파일이 마무리되지 않는다
        pipeline.wait_eos(timeout=60)
    finally:
        pipeline.stop()

    print(f"공급한 프레임: {src.frames_pushed}")
    print(f"저장 완료   : {out} ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
