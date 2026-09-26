"""사람/머리 검출 (spec 5.2).

TODO(구현):
- Ultralytics YOLO로 .pt/.onnx/.engine 로드, 5장 배치 추론
- 모델 클래스가 {0: person, 1: head}인지 확인 (COCO 가중치는 1번이 bicycle)
- 클래스별 신뢰도 임계값 적용, max_det 반영
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence

import numpy as np

from .config import DetectorConfig

PERSON = 0
HEAD = 1


@dataclass
class FrameDetections:
    """한 프레임의 검출 결과. 박스는 xyxy 픽셀 좌표."""

    persons: np.ndarray  # (N, 4)
    person_scores: np.ndarray  # (N,)
    heads: np.ndarray  # (M, 4)
    head_scores: np.ndarray  # (M,)


class Detector(Protocol):
    def detect(self, frames: Sequence[np.ndarray]) -> list[FrameDetections]: ...


class YoloDetector:
    """YOLO26s 래퍼."""

    def __init__(self, cfg: DetectorConfig):
        self.cfg = cfg

    def detect(self, frames: Sequence[np.ndarray]) -> list[FrameDetections]:
        raise NotImplementedError
