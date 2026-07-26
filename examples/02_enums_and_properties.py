"""프로퍼티를 파이썬 속성처럼, 설정값을 Enum 으로.

    python3 examples/02_enums_and_properties.py

문자열 `pattern=ball` 대신 `VideoTestSrc.Pattern.BALL` 을 쓴다. 오타·범위
초과·타입 오류는 파이프라인이 돌기 전에 예외로 잡힌다.
"""

from gstreamer_python_sdk import PropertyError
from gstreamer_python_sdk.elements import VideoTestSrc


def main() -> None:
    # --- Enum ------------------------------------------------------------
    print("VideoTestSrc.Pattern 멤버:", len(VideoTestSrc.Pattern), "개")
    print("  일부:", [m.name for m in list(VideoTestSrc.Pattern)[:8]])

    src = VideoTestSrc(num_buffers=100, pattern=VideoTestSrc.Pattern.BALL)
    print("\npattern =", repr(src.pattern))
    print("  정수값:", int(src.pattern), "| gst nick:", src.pattern.nick)

    # nick 문자열도 그대로 받는다 — gst-launch 에서 옮겨온 코드가 바로 돌아간다.
    src.pattern = "smpte"
    print("문자열로 설정 후:", repr(src.pattern))

    # --- 프로퍼티 읽기/쓰기 ------------------------------------------------
    src.num_buffers = 50
    print("\nnum_buffers =", src.num_buffers)
    print("is_live     =", src.is_live)

    # --- 검증 --------------------------------------------------------------
    # 아래 네 줄 중 '오타'와 '타입 불일치'는 mypy 가 실행 전에도 잡아낸다
    # (그래서 type: ignore 를 달아 두었다). '범위 초과'와 '없는 enum' 은 값의
    # 문제라 정적으로는 알 수 없고, 런타임 검증이 담당한다.
    print("\n잘못된 값은 파이프라인을 만들기 전에 걸린다:")
    for label, thunk in [
        ("오타", lambda: VideoTestSrc(num_buffer=10)),  # type: ignore[call-arg]
        ("범위 초과", lambda: VideoTestSrc(num_buffers=10**12)),
        ("없는 enum", lambda: VideoTestSrc(pattern="무지개")),
        ("타입 불일치", lambda: VideoTestSrc(is_live="yes")),  # type: ignore[arg-type]
    ]:
        try:
            thunk()
        except PropertyError as e:
            print(f"  [{label}] {str(e).splitlines()[0]}")

    # --- 이 엘리먼트가 무엇을 받는지 ---------------------------------------
    print("\n--- describe() 앞부분 ---")
    print("\n".join(src.describe().splitlines()[:8]))


if __name__ == "__main__":
    main()
