"""SDK 예외 계층.

이 모듈은 gi 에 의존하지 않는다(순환 import 방지). GLib.Error 를 다루는
헬퍼는 함수 안에서 필요할 때만 gi 를 건드린다.
"""

from __future__ import annotations

__all__ = [
    "GstSdkError",
    "GiNotFoundError",
    "GstInitError",
    "PipelineParseError",
    "StateChangeError",
    "GstError",
    "GstTimeout",
    "UnknownElementError",
    "PropertyError",
    "LinkError",
]


class GstSdkError(Exception):
    """SDK 가 발생시키는 모든 예외의 최상위."""


class GiNotFoundError(GstSdkError, ImportError):
    """PyGObject(gi) 또는 GStreamer typelib 을 찾지 못함."""


class GstInitError(GstSdkError):
    """gst_init_check() 실패."""


class PipelineParseError(GstSdkError):
    """parse_launch 문자열 오류."""

    def __init__(self, description: str, message: str) -> None:
        super().__init__(f"{message}\n  description: {description}")
        self.description = description
        self.message = message


class StateChangeError(GstSdkError):
    """상태 전이 실패 또는 전이 대기 타임아웃."""

    def __init__(self, target: str, result: str, cause: "GstError | None" = None) -> None:
        detail = f" ({cause})" if cause is not None else ""
        super().__init__(f"{target} 로 상태 전이 실패: {result}{detail}")
        self.target = target
        self.result = result
        self.cause = cause


class GstTimeout(GstSdkError):
    """버스 메시지 대기 타임아웃."""


class UnknownElementError(GstSdkError):
    """설치되지 않은 엘리먼트 팩토리.

    Jetson 전용 nv* 엘리먼트처럼 플랫폼에 따라 없을 수 있으므로, 어떤 패키지를
    깔아야 하는지 힌트를 함께 준다.
    """

    def __init__(self, factory_name: str, suggestions=(), detail: str = "") -> None:
        msg = f"'{factory_name}' 엘리먼트를 찾을 수 없습니다"
        if detail:
            msg += f" — {detail}"
        if suggestions:
            msg += f"\n  혹시 이것들인가요? {', '.join(suggestions)}"
        msg += (
            f"\n  설치 확인: gst-inspect-1.0 {factory_name}"
            "\n  플러그인 설치: sudo apt install gstreamer1.0-plugins-good "
            "gstreamer1.0-plugins-bad gstreamer1.0-libav"
        )
        super().__init__(msg)
        self.factory_name = factory_name
        self.suggestions = tuple(suggestions)


class PropertyError(GstSdkError):
    """존재하지 않거나, 쓸 수 없거나, 값이 허용 범위를 벗어난 프로퍼티."""

    def __init__(self, element: str, prop: str, reason: str, suggestions=()) -> None:
        msg = f"{element}.{prop}: {reason}"
        if suggestions:
            msg += f"\n  혹시 이것들인가요? {', '.join(suggestions)}"
        super().__init__(msg)
        self.element = element
        self.prop = prop
        self.reason = reason
        self.suggestions = tuple(suggestions)


class LinkError(GstSdkError):
    """엘리먼트 연결 실패. 보통 caps 협상이 안 되는 경우다."""

    def __init__(self, src: str, sink: str, detail: str = "") -> None:
        msg = f"{src} → {sink} 연결 실패"
        if detail:
            msg += f"\n{detail}"
        super().__init__(msg)
        self.src = src
        self.sink = sink


class GstError(GstSdkError):
    """버스에서 올라온 GST_MESSAGE_ERROR.

    Attributes:
        domain: GLib error domain 이름 (예: "gst-stream-error-quark")
        code: domain 내 에러 코드
        debug: GStreamer 가 붙여주는 디버그 문자열 (파일/라인 포함)
        source: 에러를 낸 엘리먼트 이름
    """

    def __init__(
        self,
        message: str,
        *,
        domain: str = "",
        code: int = 0,
        debug: str = "",
        source: str = "",
    ) -> None:
        where = f"[{source}] " if source else ""
        super().__init__(f"{where}{message}")
        self.message = message
        self.domain = domain
        self.code = code
        self.debug = debug
        self.source = source

    @classmethod
    def from_message(cls, msg) -> "GstError":
        """Gst.Message(ERROR) → GstError."""
        gerror, debug = msg.parse_error()
        src = msg.src
        return cls(
            gerror.message,
            domain=_quark_name(gerror.domain),
            code=gerror.code,
            debug=debug or "",
            source=src.get_name() if src is not None else "",
        )


def _quark_name(domain) -> str:
    """GLib quark(int) 을 사람이 읽을 수 있는 도메인 이름으로."""
    if isinstance(domain, str):
        return domain
    try:
        from gi.repository import GLib

        return GLib.quark_to_string(domain) or str(domain)
    except Exception:  # noqa: BLE001 - 진단 문자열이므로 실패해도 무시
        return str(domain)
