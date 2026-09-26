"""사람 확정 규칙 (spec 5.3, 수정 예정).

TODO(구현):
- 머리 중심이 사람 박스 상단 top_ratio 영역 안에 있고, 머리/사람 너비 비율이 범위 안이면 후보
- 신뢰도 높은 사람부터 1:1 배정, 기대 위치(사람 상단 중앙)에 가까운 머리 우선
- 미배정 person/head 개수 반환 (로그용)
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .config import MatchParams


@dataclass
class MatchResult:
    confirmed: np.ndarray  # 확정된 person 인덱스
    head_of: np.ndarray  # confirmed[i]에 배정된 head 인덱스
    unmatched_persons: int
    unmatched_heads: int


def confirm_people(
    persons: np.ndarray,
    person_scores: np.ndarray,
    heads: np.ndarray,
    params: MatchParams,
) -> MatchResult:
    raise NotImplementedError
