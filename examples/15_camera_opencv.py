"""USB 카메라 → Jetson 하드웨어 디코딩 → appsink → OpenCV imshow.

    python3 examples/15_camera_opencv.py                      # 창을 띄워 실시간 표시
    python3 examples/15_camera_opencv.py --frames 300         # 300 프레임만
    python3 examples/15_camera_opencv.py --no-display --save /tmp/shot.png
    python3 examples/15_camera_opencv.py --software           # 비교용 소프트웨어 디코딩

파이프라인 (하드웨어 경로):

    v4l2src
      ! image/jpeg, 1280x720, 30/1        카메라가 MJPEG 로 압축해서 내보낸다
      ! nvv4l2decoder mjpeg=true          NVDEC 하드웨어 디코딩 → NVMM 버퍼
      ! nvvidconv                         하드웨어 색공간 변환 (NVMM → 시스템 메모리)
      ! video/x-raw, format=BGRx
      ! videoconvert ! video/x-raw, BGR   OpenCV 가 쓰는 BGR 3채널
      ! appsink

왜 MJPEG 인가 — 이 Jetson 에서 실측한 결과:

* `nvvidconv` 는 **시스템 메모리 → 시스템 메모리** 변환을 하지 못한다
  (caps 에는 있지만 실제로는 `Internal data stream error`). 따라서 카메라의
  YUYV 출력을 곧바로 nvvidconv 에 넣는 경로는 쓸 수 없고, NVMM 버퍼를
  만들어 주는 디코더를 앞에 두어야 한다.
* `nvv4l2decoder` 는 H.264 는 실패하지만 `mjpeg=true` 로는 정상 동작한다.
* `nvjpegdec` 는 단독으로는 되지만 뒤에 nvvidconv 를 붙이면 협상에 실패한다.

`--software` 로 직접 비교할 수 있다. 720p 300 프레임 실측(C922, 30fps 요청):

    하드웨어  27.9 fps   CPU 2.87초 (27%)
    소프트웨어 23.7 fps   CPU 3.77초 (30%)

소프트웨어 경로는 30fps 를 따라가지 못한다. 하드웨어 경로에 남은 CPU 비용은
대부분 NVMM→시스템 메모리 복사와 BGRx→BGR 변환이다.
"""

import argparse
import time

import cv2
import numpy as np

from gstreamer_python_sdk import (
    Caps,
    Element,
    Fraction,
    GstSdkError,
    Pipeline,
    VideoCaps,
    VideoFormat,
    require,
)
from gstreamer_python_sdk.elements import (
    AppSink,
    JpegDec,
    NvV4l2Decoder,
    NvVidConv,
    V4l2Src,
    VideoConvert,
)


def build(
    device: str, width: int, height: int, fps: int, software: bool
) -> tuple[Pipeline, AppSink]:
    """(pipeline, appsink) 을 만든다. 하드웨어/소프트웨어 경로를 고른다."""
    src = V4l2Src(device=device)
    mjpeg = Caps("image/jpeg", width=width, height=height, framerate=Fraction(fps, 1))
    bgr = VideoCaps(format=VideoFormat.BGR, width=width, height=height)

    # 큐를 1로 두고 오래된 프레임은 버린다 — 표시가 밀리면 지연이 쌓이기 때문.
    sink = AppSink(caps=bgr, max_buffers=1, drop=True, sync=False, name="frames")

    pipeline = Pipeline(name="camera")
    chain: list[Element | Caps]
    if software:
        chain = [src, mjpeg, JpegDec(), VideoConvert(), bgr, sink]
    else:
        chain = [
            src,
            mjpeg,
            NvV4l2Decoder(mjpeg=True),          # NVDEC → NVMM
            NvVidConv(),                        # NVMM → 시스템 메모리, 색공간 변환
            VideoCaps(format=VideoFormat.BGRX, width=width, height=height),
            VideoConvert(),                     # BGRx → BGR
            bgr,
            sink,
        ]
    pipeline.build(*chain)
    return pipeline, sink


def pull_frame(sink, height: int, width: int, timeout_s: float = 5.0) -> np.ndarray | None:
    """appsink 에서 프레임 하나를 numpy 배열로. EOS 면 None."""
    Gst = require("Gst")
    sample = sink.gst.emit("try-pull-sample", int(timeout_s * Gst.SECOND))
    if sample is None:
        return None

    buffer = sample.get_buffer()
    ok, info = buffer.map(Gst.MapFlags.READ)
    if not ok:
        return None
    try:
        # copy() 필수 — unmap 하면 원본 메모리가 무효가 된다.
        return np.frombuffer(info.data, dtype=np.uint8).reshape(height, width, 3).copy()
    finally:
        buffer.unmap(info)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--device", default="/dev/video0")
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--frames", type=int, default=0, help="0 이면 무한 (q/ESC 로 종료)")
    parser.add_argument("--software", action="store_true", help="jpegdec 소프트웨어 디코딩")
    parser.add_argument("--no-display", action="store_true", help="창을 띄우지 않음(헤드리스)")
    parser.add_argument("--save", default=None, help="첫 프레임을 이 경로에 저장")
    args = parser.parse_args()

    pipeline, sink = build(args.device, args.width, args.height, args.fps, args.software)

    print(f"경로  : {'소프트웨어(jpegdec)' if args.software else '하드웨어(NVDEC)'}")
    print(f"카메라: {args.device} {args.width}x{args.height}@{args.fps} MJPEG")
    print("체인  : " + " → ".join(e.factory_name for e in pipeline.ordered()))
    if not args.no_display:
        print("창에서 q 또는 ESC 를 누르면 종료합니다.")

    window = "gstreamer-python-sdk — camera"
    count = 0
    started = time.monotonic()
    cpu_started = time.process_time()
    fps_shown = 0.0

    try:
        pipeline.play()
    except GstSdkError as e:
        print(f"\n카메라를 열 수 없습니다:\n{e}")
        print("  다른 프로그램이 장치를 쓰고 있는지 확인하세요: fuser -v " + args.device)
        return 1

    try:
        while True:
            frame = pull_frame(sink, args.height, args.width)
            if frame is None:
                print("\n스트림이 끝났습니다.")
                break
            count += 1

            if args.save and count == 1:
                cv2.imwrite(args.save, frame)
                print(f"첫 프레임 저장: {args.save}")

            elapsed = time.monotonic() - started
            if elapsed > 0:
                fps_shown = count / elapsed

            if not args.no_display:
                cv2.putText(
                    frame,
                    f"{fps_shown:5.1f} fps  |  {'SW' if args.software else 'HW'}  |  {count}",
                    (12, 34),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2,
                )
                cv2.imshow(window, frame)
                key = cv2.waitKey(1) & 0xFF
                if key in (ord("q"), 27):  # q 또는 ESC
                    break

            if args.frames and count >= args.frames:
                break
    except KeyboardInterrupt:
        print("\n중단됨")
    except cv2.error as e:
        print(f"\nOpenCV 창을 열 수 없습니다 (헤드리스 환경?): {e}")
        print("  --no-display 로 다시 실행해 보세요.")
        return 1
    finally:
        pipeline.stop()
        if not args.no_display:
            cv2.destroyAllWindows()

    wall = time.monotonic() - started
    cpu = time.process_time() - cpu_started
    print(f"\n프레임  : {count}개")
    print(f"실시간  : {wall:.1f}초 ({count / wall:.1f} fps)" if wall else "")
    print(f"CPU     : {cpu:.2f}초 ({100 * cpu / wall:.0f}%)" if wall else "")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
