"""GLib 메인루프 수명주기와 Ctrl+C 처리.

녹화 파이프라인에서 Ctrl+C 를 그냥 받으면 프로세스가 죽으면서 mux 가
마무리되지 않아 재생 불가능한 파일이 남는다. 올바른 종료 절차는

    EOS 전송 → mux 가 헤더를 씀 → EOS 가 sink 에 도달 → 그때 NULL 로 내림

이다. `run_pipeline()` 이 이걸 대신 해 준다.

    run_pipeline(pipeline)              # Ctrl+C 로 안전하게 마무리
    run_pipeline(pipeline, seconds=10)  # 10초 뒤 자동으로 EOS
"""

from __future__ import annotations

import signal
import threading
from typing import Any, Callable

from ._bootstrap import require
from .errors import GstError

__all__ = ["MainLoop", "run_pipeline"]


class MainLoop:
    """GLib.MainLoop 래퍼. 유닉스 시그널을 메인루프 안에서 안전하게 받는다.

        with MainLoop() as loop:
            loop.timeout_add(5, loop.quit)
            loop.run()
    """

    def __init__(self, *, handle_sigint: bool = True, handle_sigterm: bool = True) -> None:
        GLib = require("GLib")
        self._glib = GLib
        self._loop = GLib.MainLoop()
        self._sources: list[int] = []
        self._interrupt_handlers: list[Callable[[int], None]] = []
        self._fallback_handlers: dict[int, Any] = {}
        self._lock = threading.RLock()

        if handle_sigint:
            self._install(signal.SIGINT)
        if handle_sigterm:
            self._install(signal.SIGTERM)

    # -- 실행 --------------------------------------------------------------

    def run(self) -> None:
        """quit() 가 불릴 때까지 블로킹."""
        self._loop.run()

    def quit(self, *_args: Any) -> bool:
        """메인루프를 끝낸다. GLib 콜백으로도 쓸 수 있게 False 를 반환."""
        if self._loop.is_running():
            self._loop.quit()
        return False

    @property
    def running(self) -> bool:
        return self._loop.is_running()

    @property
    def glib_loop(self):
        """감싸고 있는 GLib.MainLoop."""
        return self._loop

    # -- 타이머 ------------------------------------------------------------

    def timeout_add(self, seconds: float, handler: Callable[[], Any]) -> int:
        """seconds 뒤에 handler 를 부른다. handler 가 True 를 반환하면 반복된다."""
        return self._add(lambda cb: self._glib.timeout_add(int(seconds * 1000), cb), handler)

    def idle_add(self, handler: Callable[[], Any]) -> int:
        """메인루프가 한가할 때 handler 를 부른다. 다른 스레드에서 호출해도 안전."""
        return self._add(self._glib.idle_add, handler)

    def _add(self, attach: Callable[[Callable[[], bool]], int], handler: Callable[[], Any]) -> int:
        """GLib 소스를 붙이고, 스스로 끝난 소스는 추적 목록에서 빼둔다.

        콜백이 False 를 반환하면 GLib 이 소스를 제거한다. 그걸 기억해 두지
        않으면 close() 가 이미 사라진 id 를 지우려다 경고를 낸다.
        """
        box: dict[str, int] = {}

        def _callback() -> bool:
            keep = bool(handler())
            if not keep:
                source_id = box.get("id")
                if source_id is not None and source_id in self._sources:
                    self._sources.remove(source_id)
            return keep

        source_id = attach(_callback)
        box["id"] = source_id
        self._sources.append(source_id)
        return source_id

    def remove(self, source_id: int) -> None:
        self._glib.source_remove(source_id)
        if source_id in self._sources:
            self._sources.remove(source_id)

    # -- 시그널 ------------------------------------------------------------

    def on_interrupt(self, handler: Callable[[int], None]) -> None:
        """SIGINT/SIGTERM 을 받았을 때 부를 콜백. handler(signum)."""
        self._interrupt_handlers.append(handler)

    def _install(self, signum: int) -> None:
        """유닉스 시그널을 메인루프 컨텍스트로 끌어온다.

        GLib.unix_signal_add 는 시그널을 메인루프 반복 안에서 배달하므로
        signal.signal 핸들러와 달리 GStreamer 상태를 안전하게 건드릴 수 있다.
        """
        unix_signal_add = getattr(self._glib, "unix_signal_add", None)
        if unix_signal_add is not None:
            source_id = unix_signal_add(
                self._glib.PRIORITY_DEFAULT, signum, self._dispatch_interrupt, signum
            )
            self._sources.append(source_id)
            return

        # GLib 이 유닉스 시그널을 지원하지 않는 환경 — 기본 방식으로 폴백한다.
        previous = signal.getsignal(signum)
        self._fallback_handlers[signum] = previous
        signal.signal(
            signum, lambda s, _frame: self._glib.idle_add(self._dispatch_interrupt, s)
        )

    def _dispatch_interrupt(self, signum: int) -> bool:
        for handler in list(self._interrupt_handlers):
            handler(signum)
        if not self._interrupt_handlers:
            self.quit()
        return True  # 시그널 소스를 유지한다(두 번째 Ctrl+C 도 받아야 하므로)

    # -- 정리 --------------------------------------------------------------

    def close(self) -> None:
        """등록한 GLib 소스와 시그널 핸들러를 되돌린다."""
        # source_remove() 는 없는 id 를 받으면 GLib 경고를 찍는다. 예외로도
        # 못 막으므로 지우기 전에 존재 여부를 확인한다.
        context = self._glib.MainContext.default()
        for source_id in list(self._sources):
            source = context.find_source_by_id(source_id)
            if source is not None and not source.is_destroyed():
                source.destroy()
        self._sources.clear()
        for signum, previous in self._fallback_handlers.items():
            signal.signal(signum, previous)
        self._fallback_handlers.clear()

    def __enter__(self) -> "MainLoop":
        return self

    def __exit__(self, *_exc: Any) -> None:
        self.quit()
        self.close()


def run_pipeline(
    pipeline: Any,
    *,
    seconds: float | None = None,
    graceful_eos: bool = True,
    raise_on_error: bool = True,
    on_message: Callable[[Any], None] | None = None,
    verbose: bool = True,
) -> GstError | None:
    """파이프라인을 PLAYING 으로 올리고 EOS/ERROR 까지 메인루프를 돌린다.

    Ctrl+C(SIGINT) 나 SIGTERM 을 받으면 곧바로 죽지 않고 EOS 를 보내 mux 가
    파일을 마무리하게 한다. 한 번 더 누르면 즉시 중단한다.

    Args:
        pipeline: Pipeline 인스턴스.
        seconds: 이 시간이 지나면 자동으로 EOS 를 보낸다. None 이면 무한.
        graceful_eos: 인터럽트 시 EOS 를 보낼지. 끄면 바로 종료한다.
        raise_on_error: ERROR 를 예외로 올릴지. 끄면 GstError 를 반환한다.
        on_message: 모든 버스 메시지를 받아 볼 콜백.
        verbose: 종료 절차를 stdout 에 알릴지.

    Returns:
        오류가 있었고 raise_on_error 가 False 면 GstError, 아니면 None.
    """
    bus = pipeline.bus
    loop = MainLoop()
    failure: dict[str, GstError | None] = {"error": None}
    state = {"eos_sent": False}

    def _say(text: str) -> None:
        if verbose:
            print(text, flush=True)

    def _on_error(err: GstError) -> None:
        failure["error"] = err
        loop.quit()

    def _on_interrupt(signum: int) -> None:
        name = signal.Signals(signum).name
        if not graceful_eos or state["eos_sent"]:
            _say(f"\n{name} — 즉시 중단합니다.")
            loop.quit()
            return
        state["eos_sent"] = True
        _say(f"\n{name} — EOS 를 보내 파일을 마무리합니다. 한 번 더 누르면 즉시 중단.")
        pipeline.send_eos()

    bus.on_eos(loop.quit)
    bus.on_error(_on_error)
    if on_message is not None:
        bus.on_any(on_message)
    bus.watch()
    loop.on_interrupt(_on_interrupt)

    if seconds is not None:
        def _timeout() -> bool:
            state["eos_sent"] = True
            _say(f"{seconds}초 경과 — EOS 를 보냅니다.")
            pipeline.send_eos()
            return False  # 한 번만

        loop.timeout_add(seconds, _timeout)

    try:
        pipeline.play()
        loop.run()
    finally:
        loop.close()
        bus.unwatch()
        pipeline.stop()

    error = failure["error"]
    if error is not None and raise_on_error:
        raise error
    return error
