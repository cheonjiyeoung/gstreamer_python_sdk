"""버스 메시지를 콜백으로 받기.

    python3 examples/10_bus_callbacks.py

`wait_eos()` 는 EOS 까지 블로킹하며 그 사이의 다른 메시지는 볼 수 없다.
경고·상태 전이·태그·버퍼링을 관찰하거나 진행 상황을 표시하려면 버스를
콜백으로 다룬다.

여기서는 메인루프 없이 `bus.run()` 으로 직접 펌프한다. GLib 메인루프와
함께 쓰는 방법은 11번 예제를 보라.
"""

from gstreamer_python_sdk import Message, MessageType, Pipeline, VideoCaps
from gstreamer_python_sdk.elements import FakeSink, VideoConvert, VideoTestSrc


def main() -> None:
    src = VideoTestSrc(num_buffers=45, pattern=VideoTestSrc.Pattern.BALL)
    conv = VideoConvert()
    sink = FakeSink(sync=False)

    pipeline = Pipeline(name="bus-demo")
    pipeline.add(src, conv, sink)
    pipeline.link(src, VideoCaps(width=320, height=240, framerate=15), conv, sink)

    bus = pipeline.bus
    counts: dict[str, int] = {}

    # 종류별 전용 콜백 — payload 가 파싱되어 넘어온다.
    bus.on_eos(lambda: print("  [eos] 스트림 끝"))
    bus.on_error(lambda err: print(f"  [error] {err}"))
    bus.on_warning(lambda err: print(f"  [warning] {err}"))
    bus.on_state_changed(
        lambda old, new, _pending: print(f"  [state] {old.value_nick} → {new.value_nick}")
    )

    # 일반 콜백 — 여러 종류를 한 번에 받는다.
    def tally(msg: Message) -> None:
        counts[msg.type_name] = counts.get(msg.type_name, 0) + 1

    bus.on_any(tally)

    # 특정 종류만 골라 받기
    bus.on(
        [MessageType.STREAM_START, MessageType.ASYNC_DONE],
        lambda msg: print(f"  [{msg.type_name}] from {msg.source}"),
    )

    print("재생 시작")
    pipeline.play()

    # 메인루프 없이 EOS 또는 ERROR 까지 메시지를 펌프한다.
    bus.run(timeout=30)
    pipeline.stop()

    print("\n받은 메시지 집계:")
    for name, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {name:16s} {n}")


if __name__ == "__main__":
    main()
