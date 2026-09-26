"""전체 균일 블러와 검증 (spec 5.7).

TODO(구현):
- 축소(1/downscale) → 가우시안 블러 → 출력 크기로 확대 → JPEG
- 검증: 축소 해상도 확인, 선명도(라플라시안 분산) <= sharpness_max, 예외 시 실패
- 실패하면 None (호출 측은 이미지를 보내지 않음)
"""

from __future__ import annotations

import numpy as np

from .config import BlurConfig


def privacy_blur(frame: np.ndarray, cfg: BlurConfig) -> bytes | None:
    raise NotImplementedError
