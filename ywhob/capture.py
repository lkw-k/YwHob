"""카메라 수신과 5장 캡처 (spec 5.1).

TODO(구현):
- CameraStream: RTSP(또는 동영상 파일) 상시 연결, 최신 프레임만 유지, 지수 백오프 재연결
- capture_burst: window_seconds 동안 frames장을 균등 간격(0, 0.75, ... 3.0초)으로 수집
- 원본 프레임은 메모리에만 둔다
"""

from __future__ import annotations

import numpy as np

from .config import CameraConfig, CaptureConfig


class CameraStream:
    def __init__(self, camera: CameraConfig, cfg: CaptureConfig):
        self.camera = camera
        self.cfg = cfg

    def start(self) -> None:
        raise NotImplementedError

    def stop(self) -> None:
        raise NotImplementedError


def capture_burst(stream: CameraStream, cfg: CaptureConfig) -> list[np.ndarray]:
    raise NotImplementedError
