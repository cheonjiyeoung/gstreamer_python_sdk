"""gi / GStreamer 부트스트랩.

설계 원칙:

1. 이 모듈을 import 하는 것만으로는 gi 를 import 하지 않고, Gst.init() 도
   호출하지 않는다. 둘 다 비싸고 전역 상태를 건드리기 때문에 실제로
   필요해지는 시점까지 미룬다(lazy).
2. sys.path 는 "정상 import 가 실패했을 때만" 그리고 "현재 인터프리터의
   ABI 와 맞는 gi 를 실제로 찾았을 때만" 건드린다. dist-packages 를 무조건
   append 하면 시스템의 낡은 numpy/cv2 까지 딸려오고, Python 버전이 다르면
   조용히 깨진다.
3. 모든 진입점은 멱등(idempotent)하고 thread-safe.

환경 변수:
    GST_SDK_GI_PATH      gi 가 있는 디렉터리를 직접 지정(콜론 구분). 최우선.
    GST_SDK_NO_PATH_PATCH=1  sys.path 자동 보정을 완전히 끈다.
"""

from __future__ import annotations

import glob
import importlib
import os
import sys
import threading
from types import ModuleType
from typing import Sequence

from .errors import GiNotFoundError, GstInitError

__all__ = [
    "init",
    "ensure_initialized",
    "is_initialized",
    "require",
    "gst_version",
    "gst_version_string",
]

# gi.require_version 에 넘길 기본 버전. 여기 없는 네임스페이스는 require() 호출 시
# version 인자를 명시해야 한다(Gtk 처럼 버전이 갈리는 것들을 추측하지 않기 위함).
_DEFAULT_VERSIONS = {
    "GLib": "2.0",
    "GObject": "2.0",
    "Gio": "2.0",
    "Gst": "1.0",
    "GstApp": "1.0",
    "GstAudio": "1.0",
    "GstBase": "1.0",
    "GstController": "1.0",
    "GstNet": "1.0",
    "GstPbutils": "1.0",
    "GstRtp": "1.0",
    "GstRtsp": "1.0",
    "GstRtspServer": "1.0",
    "GstSdp": "1.0",
    "GstTag": "1.0",
    "GstVideo": "1.0",
    "GstWebRTC": "1.0",
}

_INSTALL_HINT = (
    "PyGObject(gi) 또는 GStreamer typelib 을 찾을 수 없습니다.\n"
    "  Debian/Ubuntu/JetPack:\n"
    "    sudo apt install python3-gi python3-gi-cairo gir1.2-gstreamer-1.0 \\\n"
    "        gir1.2-gst-plugins-base-1.0 gstreamer1.0-plugins-good\n"
    "  venv 를 쓴다면 시스템 패키지가 보이도록 만들어야 합니다:\n"
    "    python3 -m venv --system-site-packages venv\n"
    "  또는 경로를 직접 지정: export GST_SDK_GI_PATH=/usr/lib/python3/dist-packages"
)

_lock = threading.RLock()
_gi: ModuleType | None = None
_initialized = False
_patched_paths: list[str] = []


# --------------------------------------------------------------------------
# gi 탐색
# --------------------------------------------------------------------------


def _abi_tag() -> str:
    """현재 인터프리터의 확장 모듈 ABI 태그 (예: 'cpython-310')."""
    return f"cpython-{sys.version_info.major}{sys.version_info.minor}"


def _candidate_dirs() -> list[str]:
    """gi 패키지가 들어있을 만한 디렉터리 후보. 우선순위 순."""
    env = os.environ.get("GST_SDK_GI_PATH")
    dirs = [d for d in env.split(os.pathsep) if d] if env else []

    ver = f"python{sys.version_info.major}.{sys.version_info.minor}"
    dirs += [
        # Debian 계열은 버전 비의존 경로에 python3 패키지를 둔다 (Jetson/JetPack 포함)
        "/usr/lib/python3/dist-packages",
        f"/usr/lib/{ver}/dist-packages",
        f"/usr/local/lib/{ver}/dist-packages",
        # RHEL/Fedora/Arch 계열
        f"/usr/lib64/{ver}/site-packages",
        f"/usr/lib/{ver}/site-packages",
        f"/usr/local/lib/{ver}/site-packages",
    ]

    seen: set[str] = set()
    out: list[str] = []
    for d in dirs:
        if d not in seen and os.path.isdir(d):
            seen.add(d)
            out.append(d)
    return out


def _abi_compatible(gi_dir: str) -> bool:
    """해당 gi 디렉터리의 C 확장이 현재 인터프리터와 호환되는지 확인.

    gi 는 순수 파이썬이 아니라 _gi.<abi>.so 를 포함한다. Python 3.10 용
    바이너리를 3.11 인터프리터에 경로만 추가하면 import 시점에 깨진다.
    """
    if glob.glob(os.path.join(gi_dir, f"_gi.{_abi_tag()}-*.so")):
        return True
    # 일부 배포판은 ABI 태그 없이 빌드한다. 태그된 .so 가 하나도 없을 때만 허용.
    if not glob.glob(os.path.join(gi_dir, "_gi.cpython-*.so")):
        return bool(glob.glob(os.path.join(gi_dir, "_gi*.so")))
    return False


def _import_gi() -> ModuleType:
    """gi 를 import 한다. 필요하면(그리고 안전할 때만) sys.path 를 보정."""
    global _gi
    if _gi is not None:
        return _gi

    try:
        import gi  # noqa: PLC0415 - lazy import 가 이 모듈의 목적
    except ImportError as first_error:
        if os.environ.get("GST_SDK_NO_PATH_PATCH") == "1":
            raise GiNotFoundError(f"{first_error}\n\n{_INSTALL_HINT}") from first_error
        gi = _import_gi_from_system(first_error)

    _gi = gi
    return gi


def _import_gi_from_system(first_error: ImportError) -> ModuleType:
    """시스템 경로에서 ABI 호환 gi 를 찾아 sys.path 에 추가하고 import."""
    tried: list[str] = []
    for d in _candidate_dirs():
        gi_dir = os.path.join(d, "gi")
        if not os.path.isfile(os.path.join(gi_dir, "__init__.py")):
            continue
        tried.append(d)
        if not _abi_compatible(gi_dir):
            continue
        # insert(0) 이 아니라 append: 이미 정상 설치된 패키지의 우선순위를 뺏지 않는다.
        sys.path.append(d)
        try:
            import gi  # noqa: PLC0415

            _patched_paths.append(d)
            return gi
        except ImportError:
            sys.path.remove(d)

    detail = ""
    if tried:
        detail = (
            f"\n  gi 를 찾긴 했지만 현재 인터프리터({sys.executable}, "
            f"Python {sys.version_info.major}.{sys.version_info.minor}, {_abi_tag()})와 "
            f"호환되지 않습니다: {', '.join(tried)}"
        )
    raise GiNotFoundError(f"{first_error}{detail}\n\n{_INSTALL_HINT}") from first_error


# --------------------------------------------------------------------------
# 네임스페이스 로딩
# --------------------------------------------------------------------------


def require(namespace: str, version: str | None = None) -> ModuleType:
    """gi.require_version 후 gi.repository.<namespace> 를 반환한다.

    Gst.init() 은 호출하지 않는다(네임스페이스 로딩과 초기화는 별개).

        Gst = require("Gst")
        GstVideo = require("GstVideo")

    Args:
        namespace: GIR 네임스페이스 이름.
        version: 생략 시 _DEFAULT_VERSIONS 값을 사용. 목록에 없으면 필수.
    """
    with _lock:
        gi = _import_gi()

        if version is None:
            version = _DEFAULT_VERSIONS.get(namespace)
            if version is None:
                raise ValueError(
                    f"'{namespace}' 의 기본 버전을 모릅니다. "
                    f"require('{namespace}', version='...') 로 명시하세요."
                )

        try:
            gi.require_version(namespace, version)
        except ValueError as e:
            already = gi.get_required_version(namespace)
            if already is None:
                # 버전 충돌이 아니라 typelib 자체가 없는 경우다. 둘을 구분하지
                # 않으면 "이미 None 을 사용 중"이라는 엉뚱한 메시지가 나간다.
                raise GiNotFoundError(
                    f"{namespace}-{version} typelib 을 찾을 수 없습니다: {e}\n"
                    f"  보통 gir1.2-* 패키지가 빠진 경우입니다 "
                    f"(예: apt-file search {namespace}-{version}.typelib)\n\n{_INSTALL_HINT}"
                ) from e
            # 이미 다른 버전이 요구/로드된 경우. 같은 버전이면 무시해도 된다.
            if already != version:
                raise ValueError(
                    f"{namespace} {version} 을 요구했지만 이 프로세스는 이미 "
                    f"{namespace} {already} 를 사용 중입니다."
                ) from e

        try:
            return importlib.import_module(f"gi.repository.{namespace}")
        except ImportError as e:
            raise GiNotFoundError(
                f"{namespace}-{version} typelib 을 로드할 수 없습니다: {e}\n\n{_INSTALL_HINT}"
            ) from e


# --------------------------------------------------------------------------
# 초기화
# --------------------------------------------------------------------------


def init(argv: Sequence[str] | None = None) -> list[str] | None:
    """GStreamer 를 초기화한다. 멱등이며 thread-safe.

    명시적으로 부를 필요는 없다 — Pipeline 등 SDK 진입점이 알아서 부른다.
    다만 첫 파이프라인 생성이 느린 것(플러그인 레지스트리 스캔)을 앞당기고
    싶거나, argv 를 GStreamer 에 넘기고 싶을 때 직접 호출한다.

    Args:
        argv: GStreamer 에 넘길 인자 목록. 기본값 None 은 sys.argv 를 건드리지
            않는다는 뜻 — SDK 가 사용자 CLI 인자를 삼키지 않도록 하는 기본값이다.
            --gst-debug-level 같은 옵션을 쓰려면 sys.argv 를 직접 넘긴다.

    Returns:
        argv 를 넘겼다면 GStreamer 가 소비하고 남은 인자 목록, 아니면 None.

    Raises:
        GiNotFoundError: gi 또는 typelib 을 찾지 못함.
        GstInitError: gst_init_check() 실패.
    """
    global _initialized
    with _lock:
        Gst = require("Gst")

        if _initialized or Gst.is_initialized():
            _initialized = True
            return list(argv) if argv is not None else None

        # init() 이 아니라 init_check(): 실패 시 프로세스를 죽이지 않고 False 반환.
        ok, remaining = Gst.init_check(list(argv) if argv is not None else None)
        if not ok:
            raise GstInitError("gst_init_check() 실패 — GStreamer 초기화 불가")

        _initialized = True
        return remaining


def ensure_initialized() -> None:
    """아직이면 init() 을 호출한다. SDK 내부 진입점에서 쓰는 저비용 가드."""
    if not _initialized:
        init()


def is_initialized() -> bool:
    """GStreamer 가 초기화되었는지."""
    return _initialized


# --------------------------------------------------------------------------
# 진단
# --------------------------------------------------------------------------


def gst_version() -> tuple[int, int, int, int]:
    """(major, minor, micro, nano). Gst.version() 은 초기화 후에만 유효하다."""
    ensure_initialized()
    return tuple(require("Gst").version())


def gst_version_string() -> str:
    """'GStreamer 1.20.3' 형태의 문자열."""
    ensure_initialized()
    return require("Gst").version_string()


def diagnostics() -> dict:
    """설치 상태 진단용 딕셔너리. 버그 리포트에 붙이기 좋다.

    진단이 목적이므로 GStreamer 초기화까지 실제로 시도한다. 어떤 단계에서
    실패하든 예외를 던지지 않고 'error' 키에 담아 반환한다.
    """
    info: dict = {
        "python": sys.version,
        "executable": sys.executable,
        "abi_tag": _abi_tag(),
    }
    try:
        gi = _import_gi()
        info["gi"] = getattr(gi, "__file__", "?")
        info["pygobject"] = ".".join(str(x) for x in gi.version_info)
        info["gstreamer"] = gst_version_string()
    except Exception as e:  # noqa: BLE001 - 진단 함수는 절대 죽지 않아야 한다
        info["error"] = f"{type(e).__name__}: {e}"

    # _import_gi() 가 sys.path 를 건드렸을 수 있으므로 반드시 그 뒤에 읽는다.
    info["patched_sys_path"] = list(_patched_paths)
    info["initialized"] = _initialized
    return info
