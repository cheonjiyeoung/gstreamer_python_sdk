"""버스 메시지를 콜백으로 받기.

`Pipeline.wait_eos()` 는 EOS 까지 블로킹한다. 그 사이에 오는 다른 메시지
(경고, 상태 전이, 버퍼링, 태그)를 보고 싶거나 여러 파이프라인을 동시에
돌려야 하면 버스를 콜백으로 다뤄야 한다.

    def on_error(err):
        print("에러:", err)

    pipeline.bus.on_error(on_error)
    pipeline.bus.on_state_changed(lambda old, new, _p: print(old.value_nick, "→", new.value_nick))

메시지를 실제로 배달하는 방법은 두 가지다:

* `bus.dispatch()` / `bus.run()` — 직접 펌프한다. 메인루프가 필요 없다.
* `bus.watch()` — GLib 메인루프에 붙인다. mainloop.run_pipeline() 이 쓰는 방식.

둘을 섞지 말 것. watch() 를 걸면 메시지를 GLib 이 가져가므로 dispatch() 와
`Pipeline.wait_eos()` 에는 아무것도 오지 않는다.
"""

from __future__ import annotations

import enum
import threading
import time
from dataclasses import dataclass
from typing import Any, Callable, Iterable

from .errors import GstError

__all__ = ["Bus", "Message", "MessageType"]

_NS_PER_SEC = 1_000_000_000


class MessageType(enum.IntFlag):
    """GStreamer 버스 메시지 종류.

    값은 GStreamer ABI 로 고정되어 있어(1.0 이후 변한 적 없다) 정적으로 적어
    둔다. 덕분에 gi 없이도 import 되고 타입 검사기가 멤버를 볼 수 있다.
    """

    UNKNOWN = 0
    EOS = 1 << 0
    ERROR = 1 << 1
    WARNING = 1 << 2
    INFO = 1 << 3
    TAG = 1 << 4
    BUFFERING = 1 << 5
    STATE_CHANGED = 1 << 6
    STATE_DIRTY = 1 << 7
    STEP_DONE = 1 << 8
    CLOCK_PROVIDE = 1 << 9
    CLOCK_LOST = 1 << 10
    NEW_CLOCK = 1 << 11
    STRUCTURE_CHANGE = 1 << 12
    STREAM_STATUS = 1 << 13
    APPLICATION = 1 << 14
    ELEMENT = 1 << 15
    SEGMENT_START = 1 << 16
    SEGMENT_DONE = 1 << 17
    DURATION_CHANGED = 1 << 18
    LATENCY = 1 << 19
    ASYNC_START = 1 << 20
    ASYNC_DONE = 1 << 21
    REQUEST_STATE = 1 << 22
    STEP_START = 1 << 23
    QOS = 1 << 24
    PROGRESS = 1 << 25
    TOC = 1 << 26
    RESET_TIME = 1 << 27
    STREAM_START = 1 << 28
    NEED_CONTEXT = 1 << 29
    HAVE_CONTEXT = 1 << 30
    # EXTENDED 비트가 켜진 것들은 순수한 단일 비트가 아니라 확장 영역이다.
    EXTENDED = 1 << 31
    DEVICE_ADDED = 0x80000001
    DEVICE_REMOVED = 0x80000002
    PROPERTY_NOTIFY = 0x80000003
    STREAM_COLLECTION = 0x80000004
    STREAMS_SELECTED = 0x80000005
    REDIRECT = 0x80000006
    DEVICE_CHANGED = 0x80000007
    INSTANT_RATE_REQUEST = 0x80000008
    ANY = 0xFFFFFFFF


@dataclass(frozen=True)
class Message:
    """버스 메시지 하나.

    Attributes:
        type: MessageType 멤버.
        source: 메시지를 낸 엘리먼트 이름 (없으면 빈 문자열).
        raw: 원본 Gst.Message — SDK 가 덮지 않는 payload 는 여기서 파싱한다.
    """

    type: Any
    source: str
    raw: Any

    @property
    def type_name(self) -> str:
        return self.raw.type.first_value_nick

    def __str__(self) -> str:
        where = f"[{self.source}] " if self.source else ""
        return f"{where}{self.type_name}"


class Bus:
    """파이프라인 버스의 콜백 래퍼.

    보통 직접 만들지 않고 `pipeline.bus` 로 얻는다.
    """

    def __init__(self, pipeline: Any) -> None:
        self._pipeline = pipeline
        self._bus = pipeline.gst.get_bus()
        self._handlers: list[tuple[int, int, Callable[[Message], None]]] = []
        self._next_id = 1
        self._signal_id: int | None = None
        self._lock = threading.RLock()

    # -- 등록 --------------------------------------------------------------

    def on(self, types: Any, handler: Callable[[Message], None]) -> int:
        """메시지 종류(하나 또는 여러 개)에 콜백을 건다. 해제용 id 를 반환."""
        mask = _mask(types)
        with self._lock:
            handler_id = self._next_id
            self._next_id += 1
            self._handlers.append((handler_id, mask, handler))
        return handler_id

    def off(self, handler_id: int) -> bool:
        """on() 이 준 id 로 콜백을 해제한다."""
        with self._lock:
            before = len(self._handlers)
            self._handlers = [h for h in self._handlers if h[0] != handler_id]
            return len(self._handlers) != before

    def on_any(self, handler: Callable[[Message], None]) -> int:
        """모든 메시지를 받는다. 디버깅용."""
        return self.on(MessageType.ANY, handler)

    def on_eos(self, handler: Callable[[], None]) -> int:
        """스트림 끝. handler() 는 인자를 받지 않는다."""
        return self.on(MessageType.EOS, lambda _msg: handler())

    def on_error(self, handler: Callable[[GstError], None]) -> int:
        """치명적 오류. handler(GstError) 로 원인이 넘어온다."""
        return self.on(MessageType.ERROR, lambda msg: handler(GstError.from_message(msg.raw)))

    def on_warning(self, handler: Callable[[GstError], None]) -> int:
        """경고. 파이프라인은 계속 돈다."""

        def _fn(msg: Message) -> None:
            gerror, debug = msg.raw.parse_warning()
            handler(
                GstError(
                    gerror.message, code=gerror.code, debug=debug or "", source=msg.source
                )
            )

        return self.on(MessageType.WARNING, _fn)

    def on_state_changed(
        self, handler: Callable[[Any, Any, Any], None], pipeline_only: bool = True
    ) -> int:
        """상태 전이. handler(old, new, pending) — 값은 Gst.State.

        Args:
            pipeline_only: True 면 파이프라인 자신의 전이만 넘긴다. 끄면 모든
                엘리먼트의 전이가 올라와 매우 시끄럽다.
        """

        def _fn(msg: Message) -> None:
            if pipeline_only and msg.raw.src is not self._pipeline.gst:
                return
            handler(*msg.raw.parse_state_changed())

        return self.on(MessageType.STATE_CHANGED, _fn)

    # -- 배달: 직접 펌프하기 -------------------------------------------------

    def dispatch(self, timeout: float = 0.0) -> int:
        """대기 중인 메시지를 모두 꺼내 콜백에 넘긴다. 처리한 개수를 반환.

        Args:
            timeout: 첫 메시지를 기다릴 시간(초). 0 이면 즉시 반환.
        """
        count = 0
        wait = int(timeout * _NS_PER_SEC)
        while True:
            msg = self._bus.timed_pop(wait)
            if msg is None:
                return count
            self._emit(msg)
            count += 1
            wait = 0  # 두 번째부터는 기다리지 않는다

    def run(self, timeout: float | None = None, raise_on_error: bool = True) -> None:
        """메인루프 없이 EOS 또는 ERROR 까지 메시지를 펌프한다.

        Raises:
            GstError: ERROR 메시지를 받았고 raise_on_error 가 True 일 때.
            GstTimeout: timeout 안에 끝나지 않았을 때.
        """
        from .errors import GstTimeout

        deadline = None if timeout is None else time.monotonic() + timeout
        while True:
            remaining = None if deadline is None else max(0.0, deadline - time.monotonic())
            if remaining == 0.0:
                raise GstTimeout(f"{timeout}초 안에 EOS 가 오지 않았습니다")

            slice_s = 0.1 if remaining is None else min(0.1, remaining)
            msg = self._bus.timed_pop(int(slice_s * _NS_PER_SEC))
            if msg is None:
                continue

            self._emit(msg)
            if int(msg.type) & int(MessageType.ERROR):
                if raise_on_error:
                    raise GstError.from_message(msg)
                return
            if int(msg.type) & int(MessageType.EOS):
                return

    # -- 배달: GLib 메인루프에 맡기기 ----------------------------------------

    def watch(self) -> None:
        """GLib 메인루프에 버스를 붙인다. 메인루프가 돌아야 콜백이 불린다."""
        with self._lock:
            if self._signal_id is not None:
                return
            self._bus.add_signal_watch()
            self._signal_id = self._bus.connect("message", lambda _bus, msg: self._emit(msg))

    def unwatch(self) -> None:
        """watch() 를 해제한다."""
        with self._lock:
            if self._signal_id is None:
                return
            self._bus.disconnect(self._signal_id)
            self._bus.remove_signal_watch()
            self._signal_id = None

    @property
    def watching(self) -> bool:
        return self._signal_id is not None

    # -- 내부 --------------------------------------------------------------

    def _emit(self, raw: Any) -> None:
        src = raw.src
        msg = Message(
            type=MessageType(int(raw.type)),
            source=src.get_name() if src is not None else "",
            raw=raw,
        )
        with self._lock:
            handlers = list(self._handlers)
        for _id, mask, fn in handlers:
            if int(raw.type) & mask:
                fn(msg)

    def __repr__(self) -> str:
        mode = "watch" if self.watching else "poll"
        return f"<Bus of {self._pipeline.name!r} handlers={len(self._handlers)} mode={mode}>"


def _mask(types: Any) -> int:
    """MessageType 멤버 / 정수 / 그것들의 목록 → 비트마스크."""
    if isinstance(types, int):
        return int(types)
    if isinstance(types, Iterable):
        mask = 0
        for t in types:
            mask |= _mask(t)
        return mask
    raise TypeError(f"메시지 종류로 쓸 수 없는 값: {types!r}")
