"""appsink 로 프레임을 numpy 배열로 꺼내오기.

    python3 examples/09_appsink_numpy.py

caps 를 데이터모델로 못 박아 두면 appsink 가 받을 포맷이 확정되므로,
버퍼를 numpy 로 reshape 할 때 추측할 필요가 없다.

SDK 가 덮지 않는 저수준 기능(버퍼 map 등)은 `.gst` 와 `require("Gst")` 로
언제든 내려갈 수 있다 — 이 예제가 그 경계를 보여준다.
"""

import numpy as np

from gstreamer_python_sdk import Pipeline, VideoCaps, VideoFormat, require
from gstreamer_python_sdk.elements import AppSink, VideoConvert, VideoTestSrc

WIDTH, HEIGHT, FRAMES = 320, 240, 10


def main() -> None:
    Gst = require("Gst")

    # appsink 가 받을 포맷을 caps 로 못 박는다 — RGB 3채널.
    wanted = VideoCaps(format=VideoFormat.RGB, width=WIDTH, height=HEIGHT, framerate=30)

    src = VideoTestSrc(num_buffers=FRAMES, pattern=VideoTestSrc.Pattern.SMPTE)
    conv = VideoConvert()
    sink = AppSink(caps=wanted, emit_signals=False, max_buffers=2, drop=False, sync=False)

    pipeline = Pipeline(name="appsink-demo")
    pipeline.add(src, conv, sink)
    pipeline.link(src, conv, sink)

    print("appsink caps:", wanted)

    with pipeline:
        count = 0
        while count < FRAMES:
            # try_pull_sample 은 타임아웃(ns)을 받고, EOS 면 None 을 돌려준다.
            sample = sink.gst.emit("try-pull-sample", 5 * Gst.SECOND)
            if sample is None:
                break

            buf = sample.get_buffer()
            ok, info = buf.map(Gst.MapFlags.READ)
            if not ok:
                continue
            try:
                frame = np.frombuffer(info.data, dtype=np.uint8).reshape(HEIGHT, WIDTH, 3)
                if count == 0:
                    print(f"\n첫 프레임: shape={frame.shape} dtype={frame.dtype}")
                    print(f"  좌상단 픽셀 RGB: {frame[0, 0]}")
                    print(f"  평균 밝기: {frame.mean():.1f}")
            finally:
                buf.unmap(info)  # map 한 버퍼는 반드시 unmap 해야 한다

            count += 1

    print(f"\n받은 프레임: {count}개")


if __name__ == "__main__":
    main()
