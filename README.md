# weather ⛅

[![CI](https://github.com/harshitpawar64/weather/actions/workflows/ci.yml/badge.svg?event=push)](https://github.com/harshitpawar64/weather/actions/workflows/ci.yml)
[![python](https://img.shields.io/badge/Python-3.12_|_3.13_|_3.14-35c555.svg?logo=python&labelColor=31373c&logoColor=skyblue)](https://www.python.org/)

[![uv](https://img.shields.io/badge/uv-black.svg?logo=uv)](https://docs.astral.sh/uv/)
[![ruff](https://img.shields.io/badge/ruff-black.svg?logo=ruff)](https://docs.astral.sh/ruff/)
[![ty](https://img.shields.io/badge/ty-black.svg?logo=ty)](https://docs.astral.sh/ty/)
[![pytest](https://img.shields.io/badge/pytest-black.svg?logo=pytest)](https://docs.pytest.org/)

A fast, beautiful terminal weather client with multi-provider fallbacks, AQI metrics, and smart caching.

![weather demo](https://raw.githubusercontent.com/harshitpawar64/weather/main/assets/demo.gif)

---

## Install

```bash
# With uv (recommended)
uv tool install weathr

# With pipx
pipx install weathr
```

---

## First-Run Onboarding

On your first launch (or at any time by running `weather setup`), `weather` launches an interactive onboarding flow. It detects your location using IP geolocation, asks to confirm your preferred city, and lets you pick your default unit system.

![onboarding demo](https://raw.githubusercontent.com/harshitpawar64/weather/main/assets/onboarding.gif)

Your preferences are saved locally (`config.toml`). After setup, simply running `weather` displays your local forecast instantly.

---

## Usage

```bash
# Check current weather + 6-day forecast for your saved location
weather

# Check weather for any city, landmark, address or postal codes
weather -l Tokyo
weather -l "Berlin, Germany"
weather -l 94103

# Specify total days of forecast (1 to 16 days)
weather -d 3
weather -l London -d 10

# Override unit system
weather --metric     # °C, km/h, mm
weather --imperial   # °F, mph, in

# Output JSON for scripting
weather --json
weather -l "Reykjavik" --json | jq .weather.current.temperature

# Verbose logging
weather -l "Berlin" -v
```

---

## CLI Options & Subcommands

### Options

| **Flag**     | **Short** |   **Default**  | **Description**                                 |
|--------------|:---------:|:--------------:|-------------------------------------------------|
| `--location` |    `-l`   | Saved location | City, landmark, address or postal codes.        |
| `--days`     |    `-d`   |       `7`      | Total days of forecast, including today. (1-16) |
| `--metric`   |           |                | Use metric units (°C, km/h, mm)                 |
| `--imperial` |           |                | Use imperial units (°F, mph, in)                |
| `--json`     |           |     `False`    | Output result in JSON format.                   |
| `--theme`    |    `-t`   |    `default`   | Theme to use for rendering output.              |
| `--verbose`  |    `-v`   |     `False`    | Enable verbose debug logging.                   |
| `--version`  |           |                | Show version and exit.                          |

### Default File Paths

| **OS**  | **Config Path (`weather config path`)**             | **Cache Path (`weather cache path`)**     |
|---------|-----------------------------------------------------|-------------------------------------------|
| Linux   | `~/.config/weather/config.toml`                     | `~/.cache/weather/cache.bin`              |
| macOS   | `~/Library/Application Support/weather/config.toml` | `~/Library/Caches/weather/cache.bin`      |
| Windows | `%LOCALAPPDATA%\weather\config.toml`                | `%LOCALAPPDATA%\weather\Cache\cache.bin`  |

### Cache Management

`weather` maintains a fast binary msgpack cache to eliminate redundant network calls:

```bash
# View cache file location
weather cache path

# Remove expired entries (>1 week old)
weather cache prune

# Wipe the cache entirely
weather cache clear
```

### Configuration Management

```bash
# Run interactive setup at any time
weather setup

# Display config file path
weather config path
```

Config file example (`config.toml`):

```toml
unit_system = "metric"
theme = "default"

[location]
latitude = 37.774929
longitude = -122.419416
display_name = "San Francisco, California, United States"
```

---

## Optional: OpenWeather API Key

`weather` works out of the box with **zero configuration** using Open-Meteo. If you want [OpenWeather](https://openweathermap.org/) as an automatic secondary fallback for Air Quality (AQI) data, [obtain a free API key](https://openweathermap.org/api) and set the `OPENWEATHER_API_KEY` environment variable:

### Linux & macOS (Bash / Zsh)

```bash
echo 'export OPENWEATHER_API_KEY="your_api_key_here"' >> ~/.bashrc  # or ~/.zshrc
source ~/.bashrc  # or source ~/.zshrc
```

### Windows (Powershell)

```powershell
[System.Environment]::SetEnvironmentVariable('OPENWEATHER_API_KEY', 'your_api_key_here', 'User')
```

---

## Attributions & Data Sources

This project is powered by several free and open data providers:

- **Weather Forecast**:
  - [Open-Meteo](https://open-meteo.com/en/docs/) (Weather Forecast API) under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

- **Air Quality**:
  - [Open-Meteo](https://open-meteo.com/en/docs/air-quality-api/) (Air Quality API) under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
  - [OpenWeather](https://openweathermap.org/) (Air Pollution API).
- **Geocoding**:
  - [Nominatim](https://nominatim.org/) (Data © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright)).
  - [Open-Meteo](https://open-meteo.com/en/docs/geocoding-api/) (Geocoding API) under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- **IP Geolocation**:
  - [IPWhoIs](https://ipwhois.io/)
  - [FreeIPAPI](https://freeipapi.com/)
  - [CountryIs](https://country.is/)
  - [IPInfo](https://ipinfo.io/)

---

## License

This project is licensed under the [MIT License](LICENSE).
