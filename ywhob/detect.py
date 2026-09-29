"""사람 검출 (spec 5.2).

TODO(구현):
- Ultralytics YOLO로 .pt/.onnx/.engine 로드, 5장 배치 추론
- 모델의 0번 클래스가 person인지 확인하고 0번만 남긴다 (COCO 가중치도 0번이 person이라 그대로 쓸 수 있음)
- person_conf 임계값 적용, max_det 반영
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence

import numpy as np

from .config import DetectorConfig

PERSON = 0


@dataclass
class FrameDetections:
    """한 프레임의 검출 결과. 박스는 xyxy 픽셀 좌표."""

    persons: np.ndarray  # (N, 4)
    person_scores: np.ndarray  # (N,)


class Detector(Protocol):
    def detect(self, frames: Sequence[np.ndarray]) -> list[FrameDetections]: ...


class YoloDetector:
    """YOLO26s 래퍼."""

    def __init__(self, cfg: DetectorConfig):
        self.cfg = cfg

    def detect(self, frames: Sequence[np.ndarray]) -> list[FrameDetections]:
        raise NotImplementedError
