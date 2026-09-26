"""단계 연결 (spec 2, 6).

    [capture ×N] ─frame queue─▶ [inference] ─result queue─▶ [aggregate → blur → publish]

TODO(구현):
- 카메라별 캡처 스레드: i × (cycle / N) 오프셋으로 시점 분산
- 큐 크기 제한, 가득 차면 가장 오래된 주기를 버림
- 주기 처리 시간 로깅, cycle_seconds 초과 시 경고
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import numpy as np

from .config import CameraConfig, ServiceConfig
from .detect import FrameDetections


@dataclass
class CaptureItem:
    """캡처 → 추론. frames가 min_frames보다 적으면 error 주기."""

    camera_id: str
    captured_at: datetime
    frames: list[np.ndarray]


@dataclass
class DetectItem:
    """추론 → 후처리. 블러를 위해 원본 frames를 함께 넘기고, 후처리 후 폐기한다."""

    camera_id: str
    captured_at: datetime
    frames: list[np.ndarray]
    detections: list[FrameDetections]


class Pipeline:
    def __init__(self, service: ServiceConfig, cameras: list[CameraConfig]):
        self.service = service
        self.cameras = cameras

    def run(self) -> None:
        """캡처, 추론, 후처리 워커를 띄우고 종료 신호까지 대기."""
        raise NotImplementedError

    def postprocess(self, item: DetectItem) -> None:
        """사람 확정 → 구역 집계 → 판정 → 블러 → 전송."""
        raise NotImplementedError
