"""실행 진입점: `uv run ywhob --cameras configs/cameras.yaml`"""

from __future__ import annotations

import argparse
import logging

from .config import load_cameras, load_service
from .pipeline import Pipeline


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(prog="ywhob", description="CCTV 혼잡도 측정 파이프라인")
    ap.add_argument("--service", default="configs/service.yaml")
    ap.add_argument("--cameras", default="configs/cameras.yaml")
    ap.add_argument("--check", action="store_true", help="설정만 검증하고 종료")
    args = ap.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    service = load_service(args.service)
    cameras = load_cameras(args.cameras)
    zones = sum(len(c.zones) for c in cameras)
    logging.info("설정 로드: 카메라 %d대, 구역 %d개", len(cameras), zones)
    if args.check:
        return
    Pipeline(service, cameras).run()


if __name__ == "__main__":
    main()
