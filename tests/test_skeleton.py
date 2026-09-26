"""뼈대 검증: 모듈 import, 설정 파일 로드, 설정 검증."""

import importlib
from pathlib import Path

import pytest

from ywhob.config import ConfigError, load_cameras, load_service
from ywhob.main import main

ROOT = Path(__file__).resolve().parents[1]
SERVICE = ROOT / "configs" / "service.yaml"
CAMERAS = ROOT / "configs" / "cameras.example.yaml"


@pytest.mark.parametrize(
    "module", ["aggregate", "blur", "capture", "detect", "matching", "pipeline", "publish"]
)
def test_modules_import(module):
    importlib.import_module(f"ywhob.{module}")


def test_service_yaml_matches_spec():
    cfg = load_service(SERVICE)
    assert cfg.cycle_seconds == 30
    assert cfg.capture.frames == 5 and cfg.capture.window_seconds == 3.0
    assert cfg.detector.max_det == 1000
    assert cfg.aggregate.up == (0.45, 0.75) and cfg.aggregate.down == (0.35, 0.65)


def test_cameras_example_loads():
    cams = load_cameras(CAMERAS)
    assert [z.zone_id for z in cams[0].zones] == ["hall_a_front", "hall_a_back"]
    assert cams[0].matching.top_ratio == 0.4


def test_hysteresis_must_have_gap(tmp_path):
    p = tmp_path / "s.yaml"
    p.write_text("aggregate:\n  up: [0.45, 0.75]\n  down: [0.50, 0.65]\n", encoding="utf-8")
    with pytest.raises(ConfigError):
        load_service(p)


def test_unknown_key_reported(tmp_path):
    p = tmp_path / "s.yaml"
    p.write_text("detector:\n  persn_conf: 0.3\n", encoding="utf-8")
    with pytest.raises(ConfigError, match="detector"):
        load_service(p)


def test_duplicate_zone_id_rejected(tmp_path):
    p = tmp_path / "c.yaml"
    zone = "{zone_id: z1, roi: [[0,0],[1,0],[1,1]], capacity: 10}"
    p.write_text(
        f"cameras:\n  - {{id: a, url: x, zones: [{zone}]}}\n  - {{id: b, url: y, zones: [{zone}]}}\n",
        encoding="utf-8",
    )
    with pytest.raises(ConfigError):
        load_cameras(p)


def test_cli_check_only():
    main(["--service", str(SERVICE), "--cameras", str(CAMERAS), "--check"])
