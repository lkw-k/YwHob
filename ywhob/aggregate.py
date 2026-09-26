"""구역 배정, 5장 집계, 신뢰도, EMA, 히스테리시스 판정 (spec 5.4 ~ 5.6).

TODO(구현):
- ZoneAssigner: 확정 사람의 발 위치(박스 하단 중심)로 구역 배정, mask 영역 제외
- classify_confidence: 중앙값, 편차(max-min), high/medium/low
- ZoneTracker: EMA, score = EMA / capacity, 히스테리시스 + confirm_cycles
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .config import AggregateConfig, Polygon, ZoneConfig

HIGH, MEDIUM, LOW = "high", "medium", "low"


class ZoneAssigner:
    def __init__(self, zones: Sequence[ZoneConfig], masks: Sequence[Polygon] = ()):
        self.zone_ids = [z.zone_id for z in zones]

    def count(self, boxes: np.ndarray) -> dict[str, int]:
        """확정 사람 박스 → 구역별 인원."""
        raise NotImplementedError


def classify_confidence(counts: Sequence[int], cfg: AggregateConfig) -> tuple[float, float, str]:
    """(중앙값, 편차, 신뢰도)."""
    raise NotImplementedError


def median_frame_index(counts: Sequence[int]) -> int:
    """인원 수가 중앙값에 가장 가까운 프레임 (블러 대상)."""
    raise NotImplementedError


@dataclass
class ZoneResult:
    zone_id: str
    accepted: bool  # False면 신뢰도 low로 폐기된 주기
    median: float
    spread: float
    confidence: str
    score: float | None  # 한 번도 유효 주기가 없었으면 None
    level: int | None


class ZoneTracker:
    """구역 하나의 EMA와 단계 상태."""

    def __init__(self, zone: ZoneConfig, cfg: AggregateConfig):
        self.zone = zone
        self.cfg = cfg

    def update(self, counts: Sequence[int]) -> ZoneResult:
        raise NotImplementedError
