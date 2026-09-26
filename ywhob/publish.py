"""Redis 전송 (spec 5.8, 9).

TODO(구현):
- 이미지(ywhob:img:{zone_id}, TTL)를 먼저, 구역 JSON(ywhob:zone:{zone_id})을 나중에 쓰기
- image_url에 ?v={unix_ts} 버전 쿼리
- low: 직전 값을 confidence low로, updated_at 유지 / error: status error
- Redis 장애는 로그만 남기고 파이프라인은 계속
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from .config import RedisConfig

KST = timezone(timedelta(hours=9))


class Publisher:
    def __init__(self, client, cfg: RedisConfig):
        self.r = client
        self.cfg = cfg

    def publish(
        self,
        zone_id: str,
        level: int,
        score: float,
        confidence: str,
        image: bytes | None,
        updated_at: datetime,
    ) -> bool:
        raise NotImplementedError

    def publish_low(self, zone_id: str) -> bool:
        raise NotImplementedError

    def publish_error(self, zone_id: str, updated_at: datetime) -> bool:
        raise NotImplementedError

    def heartbeat(self, at: datetime) -> None:
        raise NotImplementedError
