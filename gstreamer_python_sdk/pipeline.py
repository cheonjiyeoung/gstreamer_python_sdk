"""Pipeline — 엘리먼트를 담고 연결하고 상태를 관리한다.

모듈 레벨에서 `from gi.repository import Gst` 를 하지 않는다. 그렇게 하면
`import gstreamer_python_sdk.pipeline` 만으로 gi 가 로드되어 lazy 설계가
깨진다. 필요한 시점에 _bootstrap.require("Gst") 로 가져온다.

    src, conv, sink = VideoTestSrc(num_buffers=100), VideoConvert(), AutoVideoSink()

    pipeline = Pipeline()
    pipeline.add(src, conv, sink)
    pipeline.link(src, VideoCaps(width=640, height=480), conv, sink)

    with pipeline:
        pipeline.wait_eos()
"""

from __future__ import annotations

from typing import Any, Iterator, Sequence

from ._bootstrap import ensure_initialized, require
from .caps import Caps
from .element import Element
from .errors import GstError, GstTimeout, LinkError, PipelineParseError, StateChangeError

__all__ = ["Pipeline"]

_NS_PER_SEC = 1_000_000_000


def _to_ns(seconds: float | None) -> int:
    """초 → 나노초. None 이면 무한 대기(Gst.CLOCK_TIME_NONE)."""
    if seconds is None:
        return require("Gst").CLOCK_TIME_NONE
    return int(seconds * _NS_PER_SEC)


def _unwrap(element):
    """Element 래퍼든 raw Gst.Element 든 Gst.Element 로 통일."""
    return element.gst if isinstance(element, Element) else element


class Pipeline:
    """Gst.Pipeline 래퍼.

    세 가지 방식으로 만들 수 있다:

        Pipeline("videotestsrc ! fakesink")        # gst-launch 문자열
        Pipeline([src, conv, sink])                # 순서대로 add + link
        Pipeline()                                 # 빈 파이프라인 후 add/link
    """

    def __init__(
        self,
        description: str | Sequence[Element] | None = None,
        *,
        name: str | None = None,
    ) -> None:
        ensure_initialized()
        Gst = require("Gst")

        elements: Sequence[Element] | None = None
        if description is not None and not isinstance(description, str):
            elements, description = description, None

        if description is None:
            self._pipeline = Gst.Pipeline.new(name)
            self.description = ""
        else:
            GLib = require("GLib")
            try:
                self._pipeline = Gst.parse_launch(description)
            except GLib.Error as e:
                raise PipelineParseError(description, e.message) from e
            if name is not None:
                self._pipeline.set_name(name)
            self.description = description

        self._bus = self._pipeline.get_bus()
        self._bus_wrapper: Any = None  # bus 프로퍼티에서 처음 쓸 때 만든다
        self._owned: list[Element] = []  # 자동 생성한 capsfilter 등을 붙잡아 둔다

        if elements:
            self.build(*elements)

    # -- 하부 객체 접근 ---------------------------------------------------

    @property
    def gst(self):
        """감싸고 있는 Gst.Pipeline. SDK 가 못 덮는 기능은 여기로 내려가면 된다."""
        return self._pipeline

    @property
    def name(self) -> str:
        return self._pipeline.get_name()

    @property
    def bus(self):
        """콜백으로 버스 메시지를 받기 위한 Bus 래퍼.

        `wait_eos()` 로 충분한 경우에는 쓸 필요가 없다. 경고·상태 전이·태그
        같은 다른 메시지를 보거나 메인루프와 함께 돌릴 때 쓴다.
        """
        if self._bus_wrapper is None:
            from .bus import Bus

            self._bus_wrapper = Bus(self)
        return self._bus_wrapper

    def __getitem__(self, element_name: str) -> Element:
        """`pipeline["mysink"]` — 이름으로 엘리먼트를 찾아 래퍼로 돌려준다."""
        el = self._pipeline.get_by_name(element_name)
        if el is None:
            available = [e.name for e in self]
            raise KeyError(
                f"'{element_name}' 엘리먼트가 파이프라인에 없습니다. 있는 이름: {available}"
            )
        return Element.wrap(el)

    def __contains__(self, element_name: object) -> bool:
        return self._pipeline.get_by_name(str(element_name)) is not None

    def ordered(self) -> list[Element]:
        """소스 → 싱크 순서로 정렬된 엘리먼트 목록.

        `iter(pipeline)` 은 GStreamer 내부 순서(대략 역순)를 그대로 내보내므로,
        사람이 읽을 순서가 필요할 때는 이쪽을 쓴다.
        """
        Gst = require("Gst")
        it = self._pipeline.iterate_sorted()
        out: list[Element] = []
        while True:
            result, value = it.next()
            if result == Gst.IteratorResult.DONE:
                break
            if result == Gst.IteratorResult.OK:
                out.append(Element.wrap(value))
            elif result == Gst.IteratorResult.RESYNC:
                it.resync()
                out.clear()
            else:
                break
        out.reverse()  # iterate_sorted 는 싱크부터 준다
        return out

    def __iter__(self) -> Iterator[Element]:
        Gst = require("Gst")
        it = self._pipeline.iterate_elements()
        while True:
            result, value = it.next()
            if result == Gst.IteratorResult.DONE:
                return
            if result == Gst.IteratorResult.OK:
                yield Element.wrap(value)
            elif result == Gst.IteratorResult.RESYNC:
                it.resync()
            else:
                raise GstError("엘리먼트 순회 실패")

    # -- 조립 -------------------------------------------------------------

    def add(self, *elements: Element) -> "Pipeline":
        """엘리먼트를 파이프라인에 넣는다. self 를 반환."""
        for element in elements:
            # gst-python 이 Gst.Bin.add 를 오버라이드해서 성공 시 None 을 반환하고
            # 실패 시 Gst.AddError 를 던진다. bool 로 판정하면 안 된다.
            try:
                result = self._pipeline.add(_unwrap(element))
            except Exception as e:  # noqa: BLE001 - Gst.AddError 를 SDK 예외로 변환
                raise GstError(f"{element} 를 파이프라인에 추가하지 못했습니다: {e}") from e
            if result is False:
                raise GstError(f"{element} 를 파이프라인에 추가하지 못했습니다")
        return self

    def link(self, *items: Element | Caps | str) -> "Pipeline":
        """주어진 순서대로 연결한다. self 를 반환.

        중간에 Caps 를 끼우면 capsfilter 를 자동으로 만들어 넣는다:

            pipeline.link(src, VideoCaps(width=640, height=480), conv, sink)

        연결에 실패하면 양쪽 패드의 caps 를 담은 LinkError 를 던진다.
        """
        chain: list[Element] = []
        for item in items:
            if isinstance(item, (Caps, str)):
                if not chain:
                    raise LinkError("<없음>", str(item), "caps 앞에 엘리먼트가 있어야 합니다")
                chain.append(self._make_capsfilter(item))
            else:
                chain.append(item)

        for src, sink in zip(chain, chain[1:]):
            if not _unwrap(src).link(_unwrap(sink)):
                from .element import _link_hint

                detail = (
                    _link_hint(src, sink)
                    if isinstance(src, Element) and isinstance(sink, Element)
                    else ""
                )
                raise LinkError(src.name, sink.name, detail)
        return self

    def build(self, *items: Element | Caps | str) -> "Pipeline":
        """add + link 을 한 번에. 가장 흔한 선형 파이프라인용."""
        self.add(*[i for i in items if isinstance(i, Element)])
        return self.link(*items)

    def link_pads(
        self,
        src: Element,
        src_pad: str,
        sink: Element,
        sink_pad: str = "sink",
    ) -> "Pipeline":
        """패드 이름을 지정해 연결한다. tee/demuxer 처럼 패드가 여러 개일 때."""
        if not _unwrap(src).link_pads(src_pad, _unwrap(sink), sink_pad):
            raise LinkError(f"{src.name}.{src_pad}", f"{sink.name}.{sink_pad}")
        return self

    def _make_capsfilter(self, caps: Caps | str) -> Element:
        """link() 중간에 끼워 넣을 capsfilter 를 만들어 파이프라인에 추가."""
        element = Element("capsfilter", caps=caps)
        self.add(element)
        self._owned.append(element)
        if self.state != require("Gst").State.NULL:
            element.gst.sync_state_with_parent()
        return element

    # -- 상태 전이 --------------------------------------------------------

    @property
    def state(self):
        """현재 상태(Gst.State). 전이 중이면 대기하지 않고 즉시 반환."""
        _, current, _ = self._pipeline.get_state(0)
        return current

    def set_state(self, state, timeout: float | None = 5.0):
        """상태를 바꾸고 전이가 끝날 때까지 기다린다.

        Args:
            state: 목표 Gst.State.
            timeout: ASYNC 전이 대기 시간(초). None 이면 무한, 0 이면 대기 안 함.

        Raises:
            StateChangeError: 전이 실패 또는 타임아웃. 버스에 ERROR 가 있으면
                원인을 GstError 로 감싸 cause 에 담는다.
        """
        Gst = require("Gst")
        ret = self._pipeline.set_state(state)

        if ret == Gst.StateChangeReturn.FAILURE:
            raise StateChangeError(state.value_nick, "FAILURE", self._poll_error())

        if ret == Gst.StateChangeReturn.ASYNC and timeout != 0:
            ret, _current, _pending = self._pipeline.get_state(_to_ns(timeout))
            if ret == Gst.StateChangeReturn.FAILURE:
                raise StateChangeError(state.value_nick, "FAILURE", self._poll_error())
            if ret == Gst.StateChangeReturn.ASYNC:
                raise StateChangeError(state.value_nick, f"{timeout}초 내 전이 미완료")

        return ret

    def play(self, timeout: float | None = 5.0):
        return self.set_state(require("Gst").State.PLAYING, timeout)

    def pause(self, timeout: float | None = 5.0):
        return self.set_state(require("Gst").State.PAUSED, timeout)

    def stop(self, timeout: float | None = 5.0):
        """NULL 로 내린다. 리소스(카메라/인코더 등)는 이때 반납된다."""
        return self.set_state(require("Gst").State.NULL, timeout)

    # -- 버스 -------------------------------------------------------------

    def wait_eos(self, timeout: float | None = None) -> None:
        """EOS 까지 블로킹. ERROR 가 오면 GstError 로 올린다.

        Raises:
            GstError: 파이프라인 에러.
            GstTimeout: timeout 내에 EOS 도 ERROR 도 오지 않음.
        """
        Gst = require("Gst")
        msg = self._bus.timed_pop_filtered(
            _to_ns(timeout), Gst.MessageType.ERROR | Gst.MessageType.EOS
        )
        if msg is None:
            raise GstTimeout(f"{timeout}초 내에 EOS 가 오지 않았습니다")
        if msg.type == Gst.MessageType.ERROR:
            raise GstError.from_message(msg)

    def send_eos(self) -> None:
        """파이프라인에 EOS 를 보낸다. 녹화 파일을 정상 마무리할 때 필요하다."""
        self._pipeline.send_event(require("Gst").Event.new_eos())

    def _poll_error(self) -> GstError | None:
        """버스에 쌓인 ERROR 를 논블로킹으로 하나 꺼낸다(진단용)."""
        Gst = require("Gst")
        msg = self._bus.pop_filtered(Gst.MessageType.ERROR)
        return GstError.from_message(msg) if msg is not None else None

    # -- 위치/길이 --------------------------------------------------------

    @property
    def position(self) -> float | None:
        """현재 재생 위치(초). 아직 알 수 없으면 None."""
        Gst = require("Gst")
        ok, pos = self._pipeline.query_position(Gst.Format.TIME)
        return pos / _NS_PER_SEC if ok and pos >= 0 else None

    @property
    def duration(self) -> float | None:
        """전체 길이(초). 라이브 소스 등에서는 None."""
        Gst = require("Gst")
        ok, dur = self._pipeline.query_duration(Gst.Format.TIME)
        return dur / _NS_PER_SEC if ok and dur >= 0 else None

    # -- 진단 -------------------------------------------------------------

    def diagram(self, *, show_caps: bool = True) -> str:
        """소스 → 싱크 순서의 텍스트 다이어그램. 의존성 없음.

        PLAYING 상태에서 부르면 실제로 협상된 caps 가 보이므로 협상 문제를
        추적할 때 유용하다.
        """
        from .graph import diagram

        return diagram(self, show_caps=show_caps)

    def to_dot(self, path: str | None = None) -> str:
        """파이프라인 그래프를 Graphviz DOT 텍스트로. path 를 주면 파일로도 쓴다."""
        from .graph import to_dot

        return to_dot(self, path)

    def save_graph(self, path, image_format: str | None = None):
        """그래프를 PNG/SVG 등으로 렌더링한다. graphviz(dot) 가 필요하다."""
        from .graph import save_graph

        return save_graph(self, path, image_format)

    # -- 컨텍스트 매니저 --------------------------------------------------

    def __enter__(self) -> "Pipeline":
        try:
            self.play()
        except Exception:
            # 진입 실패 시 __exit__ 은 호출되지 않는다. 여기서 직접 내려주지
            # 않으면 파이프라인이 READY 로 남아 리소스를 붙잡는다.
            try:
                self.stop(timeout=0)
            except Exception:  # noqa: BLE001 - 원래 예외를 가리지 않는다
                pass
            raise
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        # 정리 중 발생한 상태 전이 실패로 원래 예외를 가리지 않는다.
        try:
            self.stop()
        except Exception:  # noqa: BLE001
            if exc_type is None:
                raise

    def __repr__(self) -> str:
        desc = self.description or " → ".join(e.factory_name for e in self.ordered()) or "<empty>"
        if len(desc) > 60:
            desc = desc[:57] + "..."
        return f"<Pipeline {self.name!r} state={self.state.value_nick} {desc!r}>"
