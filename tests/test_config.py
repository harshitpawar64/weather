from pathlib import Path
from unittest.mock import MagicMock

import pytest

import tests.constants as c
from weather.config import Config
from weather.models import Theme, UnitSystem


def test_config_default_when_file_missing(config: Config) -> None:
    assert config.location is None
    assert config.unit_system == UnitSystem.METRIC
    assert config.theme == Theme.DEFAULT


def test_config_save_and_read(tmp_path: Path) -> None:
    cfg1 = Config(config_dir=tmp_path)
    cfg1.save(location=c.LOCATION, unit_system=UnitSystem.IMPERIAL, theme=Theme.DEFAULT)

    cfg2 = Config(config_dir=tmp_path)
    assert cfg2.location == c.LOCATION
    assert cfg2.unit_system == UnitSystem.IMPERIAL
    assert cfg2.theme == Theme.DEFAULT


def test_config_save_partial_update(config: Config) -> None:
    config.save(location=c.LOCATION)
    assert config.location == c.LOCATION
    assert config.unit_system == UnitSystem.METRIC

    config.save(unit_system=UnitSystem.IMPERIAL)
    assert config.location == c.LOCATION
    assert config.unit_system == UnitSystem.IMPERIAL


def test_config_read_corrupted_file(tmp_path: Path) -> None:
    config_file = tmp_path / "config.toml"
    config_file.write_bytes(b"INVALID_TOML_[[{")

    cfg = Config(config_dir=tmp_path)
    assert cfg.location is None
    assert cfg.unit_system == UnitSystem.METRIC
    assert cfg.theme == Theme.DEFAULT


def test_config_clear(config: Config) -> None:
    config.save(location=c.LOCATION)
    assert config.file.exists()

    config.clear()
    assert not config.file.exists()


def test_config_write_error(config: Config, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        Path, "write_bytes", MagicMock(side_effect=OSError("Disk full"))
    )
    config.save(location=c.LOCATION)
