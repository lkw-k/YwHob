"""실행 진입점: `uv run ywhob --cameras configs/cameras.yaml [--model s|n]`"""

from __future__ import annotations

import argparse
import dataclasses
import logging
import sys
from pathlib import Path

from .config import load_cameras, load_service
from .pipeline import Pipeline


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(prog="ywhob", description="CCTV 혼잡도 측정 파이프라인")
    ap.add_argument("--service", default="configs/service.yaml")
    ap.add_argument("--cameras", default="configs/cameras.yaml")
    ap.add_argument("--model", help="검출 모델. service.yaml detector.models의 별칭(s: 스몰, n: 나노) 또는 가중치 경로")
    ap.add_argument("--check", action="store_true", help="설정만 검증하고 종료")
    args = ap.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    service = load_service(args.service)
    if args.model:
        service = dataclasses.replace(service, detector=service.detector.with_model(args.model))
    if not Path(args.cameras).is_file():
        logging.error("카메라 설정 없음: %s (configs/cameras.example.yaml을 복사해 RTSP 주소와 ROI를 채운다)", args.cameras)
        sys.exit(1)
    cameras = load_cameras(args.cameras)
    zones = sum(len(c.zones) for c in cameras)
    logging.info("설정 로드: 카메라 %d대, 구역 %d개, 모델 %s", len(cameras), zones, service.detector.model)

    if not Path(service.detector.model).is_file():
        aliases = ", ".join(f"{k}={v}" for k, v in service.detector.models.items())
        msg = "모델 파일 없음: %s (별칭: %s). models/README.md 참고"
        if args.check:
            logging.warning(msg, service.detector.model, aliases or "없음")
        else:
            logging.error(msg, service.detector.model, aliases or "없음")
            sys.exit(1)
    if args.check:
        return
    Pipeline(service, cameras).run()


if __name__ == "__main__":
    main()
