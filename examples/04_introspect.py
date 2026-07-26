"""설치된 엘리먼트를 코드로 탐색하기 — gst-inspect-1.0 대신.

    python3 examples/04_introspect.py
    python3 examples/04_introspect.py nvv4l2h264enc

큐레이션 목록에 없는 엘리먼트도 전부 쓸 수 있다. 이름만 알면 Element(...) 로
바로 쓰거나 make(...) 로 클래스를 만들 수 있다.
"""

import sys

from gstreamer_python_sdk import Element, inspect_element, list_factories
from gstreamer_python_sdk.elements import CURATED, available, make


def main() -> None:
    factory = sys.argv[1] if len(sys.argv) > 1 else "videotestsrc"

    print(f"설치된 엘리먼트: {len(list_factories())}개")
    print(f"  Source/Video : {len(list_factories('Source/Video'))}개")
    print(f"  Encoder      : {len(list_factories('Encoder'))}개")
    print(f"이름 있는 클래스: {len(CURATED)}개 중 이 시스템에 {len(available())}개 설치됨")

    print(f"\n--- {factory} ---")
    spec = inspect_element(factory)
    print(f"이름  : {spec.long_name}")
    print(f"klass : {spec.klass}")
    print(f"설명  : {spec.description}")

    print(f"\n프로퍼티 {len(spec.properties)}개 중 쓰기 가능 {len(spec.writable_properties)}개:")
    for prop in list(spec.writable_properties)[:10]:
        print(f"  {prop.describe()}")
    if len(spec.writable_properties) > 10:
        print(f"  ... 외 {len(spec.writable_properties) - 10}개")

    print("\n패드:")
    for pad in spec.pads:
        caps = pad.caps if len(pad.caps) <= 70 else pad.caps[:67] + "..."
        print(f"  {pad.direction:4s} {pad.name:12s} ({pad.presence})  {caps}")

    # 큐레이션 밖 엘리먼트를 쓰는 두 가지 방법
    print("\n--- 큐레이션 밖 엘리먼트 ---")
    box = Element("videobox", top=10, bottom=10)
    print(f"  Element 직접   : {box!r}, top={box.top}")

    Compositor = make("Compositor", "compositor")
    comp = Compositor(background="black")
    print(f"  클래스로 승격  : {comp!r}, background={comp.background!r}")


if __name__ == "__main__":
    main()
