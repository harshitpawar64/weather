import msgspec
from platformdirs import user_config_path

from weather.models import Location, UnitSystem

_CONFIG_DIR = user_config_path("weather", "Harshit Pawar")
_CONFIG_DIR.mkdir(parents=True, exist_ok=True)


class ConfigData(msgspec.Struct):
    location: Location | None = None
    unit_system: UnitSystem = UnitSystem.METRIC


class Config:
    def __init__(self):
        self.file = _CONFIG_DIR / "config.toml"
        self._data = self._read()

    def _read(self) -> ConfigData:
        try:
            return msgspec.toml.decode(self.file.read_bytes(), type=ConfigData)
        except FileNotFoundError, msgspec.ValidationError, msgspec.DecodeError:
            return ConfigData()

    @property
    def location(self) -> Location | None:
        return self._data.location

    @property
    def unit_system(self) -> UnitSystem:
        return self._data.unit_system

    def save(
        self, location: Location | None = None, unit_system: UnitSystem | None = None
    ) -> None:
        if not location:
            location = self._data.location
        if not unit_system:
            unit_system = self._data.unit_system

        self._data = ConfigData(location=location, unit_system=unit_system)

        self.file.write_bytes(msgspec.toml.encode(self._data))

    def clear(self):
        self.file.unlink(missing_ok=True)
