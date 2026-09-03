import logging
from pathlib import Path

import msgspec
from platformdirs import user_config_path

from weather.models import Location, Theme, UnitSystem

logger = logging.getLogger(__name__)


class ConfigData(msgspec.Struct, omit_defaults=True):
    location: Location | None = None
    unit_system: UnitSystem = UnitSystem.METRIC
    theme: Theme = Theme.DEFAULT


class Config:
    def __init__(self, config_dir: Path | None = None) -> None:
        self.file = (
            config_dir or user_config_path("weather", ensure_exists=True)
        ) / "config.toml"

        self._data = self._read()

    def _read(self) -> ConfigData:
        try:
            return msgspec.toml.decode(self.file.read_bytes(), type=ConfigData)
        except FileNotFoundError:
            logger.info(
                "Config file not found at '%s'. Using default configuration.", self.file
            )
        except msgspec.DecodeError as e:
            logger.error("Config file at '%s' is corrupted. (%s)", self.file, e)

        return ConfigData()

    def _write(self) -> None:
        try:
            temp_file = self.file.with_suffix(".tmp")
            temp_file.write_bytes(msgspec.toml.encode(self._data))
            temp_file.replace(self.file)
        except OSError as e:
            temp_file.unlink(missing_ok=True)
            logger.error("Failed to write config file to '%s': %s", self.file, e)

    @property
    def location(self) -> Location | None:
        return self._data.location

    @property
    def unit_system(self) -> UnitSystem:
        return self._data.unit_system

    @property
    def theme(self) -> Theme:
        return self._data.theme

    def save(
        self,
        location: Location | None = None,
        unit_system: UnitSystem | None = None,
        theme: Theme | None = None,
    ) -> None:
        if not location:
            location = self._data.location
        if not unit_system:
            unit_system = self._data.unit_system
        if not theme:
            theme = self._data.theme

        self._data = ConfigData(location=location, unit_system=unit_system, theme=theme)
        self._write()

    def reset(self) -> None:
        self.file.unlink(missing_ok=True)
        self.file.with_suffix(".tmp").unlink(missing_ok=True)
