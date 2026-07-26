"""RTSP 서버 (GstRtspServer).

    server = RtspServer(port=8554)
    server.add_route("/live",
        VideoTestSrc(is_live=True),
        VideoCaps(width=640, height=480, framerate=30),
        VideoConvert(),
        X264Enc(tune=X264Enc.Tune.ZEROLATENCY),
        RtpH264Pay(name="pay0", pt=96),
    )
    server.run()        # rtsp://<host>:8554/live

GstRtspServer 의 `set_launch()` 는 gst-launch 문자열만 받는다. 그래서 이
모듈은 `launch_string()` 으로 데이터모델을 문자열로 직렬화해서 넘긴다 —
호출하는 쪽은 계속 엘리먼트 객체로만 다루면 된다.

**패드 이름 규칙**: 각 route 의 마지막 payloader 는 반드시 `name="pay0"` 이어야
한다. GstRtspServer 가 그 이름으로 RTP 스트림을 찾는다. 오디오까지 보내려면
`pay1` 을 추가한다.

이 모듈은 `gir1.2-gst-rtsp-server-1.0` 패키지를 요구한다.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from ._bootstrap import ensure_initialized, require
from .caps import Caps
from .element import Element, launch_string
from .errors import GstSdkError

__all__ = ["RtspServer", "RtspRoute"]

_INSTALL_HINT = (
    "RTSP 서버에는 GstRtspServer typelib 이 필요합니다.\n"
    "  sudo apt install gir1.2-gst-rtsp-server-1.0 gstreamer1.0-rtsp"
)


@dataclass(frozen=True)
class RtspRoute:
    """마운트된 경로 하나."""

    path: str
    launch: str
    shared: bool

    def url(self, host: str, port: int) -> str:
        return f"rtsp://{host}:{port}{self.path}"


class RtspServer:
    """RTSP 서버. 경로별로 파이프라인을 하나씩 붙인다."""

    def __init__(self, *, port: int = 8554, address: str = "0.0.0.0") -> None:
        ensure_initialized()
        try:
            self._rtsp = require("GstRtspServer")
        except Exception as e:  # noqa: BLE001 - typelib 부재를 친절한 메시지로
            raise GstSdkError(f"{e}\n\n{_INSTALL_HINT}") from e

        self._server = self._rtsp.RTSPServer()
        self._server.set_service(str(port))
        self._server.set_address(address)
        self._routes: dict[str, RtspRoute] = {}
        self._source_id: int | None = None
        self.port = port
        self.address = address

    # -- 경로 --------------------------------------------------------------

    def add_route(
        self,
        path: str,
        *items: Element | Caps | str,
        shared: bool = True,
        latency: int | None = None,
    ) -> RtspRoute:
        """경로 하나에 파이프라인을 붙인다.

        Args:
            path: '/live' 처럼 슬래시로 시작하는 마운트 경로.
            *items: 엘리먼트와 caps. 마지막은 `name="pay0"` 인 payloader 여야 한다.
            shared: True 면 여러 클라이언트가 하나의 파이프라인을 공유한다.
                False 면 접속마다 새 파이프라인이 뜬다(카메라는 보통 True).
            latency: 지터버퍼 지연(ms).

        Returns:
            등록된 RtspRoute.
        """
        if not path.startswith("/"):
            path = "/" + path
        if path in self._routes:
            raise GstSdkError(f"'{path}' 경로는 이미 등록되어 있습니다")

        launch = launch_string(*items)
        _require_payloader(path, launch)

        factory = self._rtsp.RTSPMediaFactory()
        factory.set_launch(f"( {launch} )")
        factory.set_shared(shared)
        if latency is not None:
            factory.set_latency(latency)

        self._server.get_mount_points().add_factory(path, factory)
        route = RtspRoute(path=path, launch=launch, shared=shared)
        self._routes[path] = route
        return route

    def remove_route(self, path: str) -> bool:
        if not path.startswith("/"):
            path = "/" + path
        if path not in self._routes:
            return False
        self._server.get_mount_points().remove_factory(path)
        del self._routes[path]
        return True

    @property
    def routes(self) -> tuple[RtspRoute, ...]:
        return tuple(self._routes.values())

    def urls(self, host: str | None = None) -> list[str]:
        """클라이언트가 접속할 주소들. 0.0.0.0 은 실제 IP 로 바꿔 보여준다."""
        shown = host or (_local_ip() if self.address == "0.0.0.0" else self.address)
        return [route.url(shown, self.port) for route in self._routes.values()]

    # -- 실행 --------------------------------------------------------------

    def attach(self) -> None:
        """기본 GLib 메인 컨텍스트에 서버를 붙인다. 메인루프는 따로 돌려야 한다."""
        if self._source_id is not None:
            return
        if not self._routes:
            raise GstSdkError("등록된 경로가 없습니다. add_route() 를 먼저 부르세요.")
        self._source_id = self._server.attach(None)

    def detach(self) -> None:
        if self._source_id is None:
            return
        GLib = require("GLib")
        source = GLib.MainContext.default().find_source_by_id(self._source_id)
        if source is not None and not source.is_destroyed():
            source.destroy()
        self._source_id = None

    def run(self, *, verbose: bool = True) -> None:
        """서버를 붙이고 메인루프를 돌린다. Ctrl+C 로 종료."""
        from .mainloop import MainLoop

        self.attach()
        loop = MainLoop()

        def _on_interrupt(_signum: int) -> None:
            loop.quit()

        loop.on_interrupt(_on_interrupt)

        if verbose:
            print(f"RTSP 서버 시작 — {self.address}:{self.port}")
            for url in self.urls():
                print(f"  {url}")
            print("  재생: gst-play-1.0 <url>   /   ffplay -rtsp_transport tcp <url>")
            print("Ctrl+C 로 종료합니다.")

        try:
            loop.run()
        finally:
            loop.close()
            self.detach()
            if verbose:
                print("\nRTSP 서버 종료")

    def __repr__(self) -> str:
        return f"<RtspServer {self.address}:{self.port} routes={len(self._routes)}>"


def _require_payloader(path: str, launch: str) -> None:
    """pay0 이 없으면 GstRtspServer 가 런타임에 알기 어려운 오류를 낸다."""
    if re.search(r"\bname=pay0\b", launch):
        return
    raise GstSdkError(
        f"'{path}' 경로의 마지막 엘리먼트는 name=\"pay0\" 인 payloader 여야 합니다.\n"
        f"  예: RtpH264Pay(name=\"pay0\", pt=96)\n"
        f"  현재: {launch}"
    )


def _local_ip() -> str:
    """바깥으로 나가는 인터페이스의 IP. 접속 주소를 안내하기 위한 것뿐이다."""
    import socket

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # 실제로 패킷을 보내지는 않는다
            return str(s.getsockname()[0])
    except OSError:
        return "127.0.0.1"
