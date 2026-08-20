import msgspec

from weather.models import (
    AirQuality,
    CurrentWeather,
    DailyForecast,
    Location,
    UnitSystem,
    UnixTimestamp,
    WeatherData,
)

LATITUDE = 42.00
LONGITUDE = 42.00
CITY = "City"
REGION = "Region"
COUNTRY = "Country"
DISPLAY_NAME = f"{CITY}, {REGION}, {COUNTRY}"
QUERY = "test query"

LOCATION = Location(latitude=LATITUDE, longitude=LONGITUDE, display_name=DISPLAY_NAME)
ENCODER = msgspec.json.Encoder()

DATE = "1970-01-01"
TIME = "1970-01-01T00:00"
SUNRISE = "1970-01-01T06:00"
SUNSET = "1970-01-01T21:00"

CURRENT_WEATHER = CurrentWeather(
    time=TIME,
    weather_code=0,
    temperature=20.0,
    apparent_temperature=19.5,
    humidity=50,
    precipitation=0.0,
    wind_speed=10.0,
    wind_direction=180,
    wind_gusts=12.0,
    is_day=True,
)

DAILY_FORECAST = DailyForecast(
    date=DATE,
    weather_code=0,
    temp_min=15.0,
    temp_max=25.0,
    precipitation_sum=0.0,
    precipitation_prob_max=10,
    wind_speed_max=15.0,
    sunrise=SUNRISE,
    sunset=SUNSET,
)

AIR_QUALITY = AirQuality(
    us_aqi=42.0,
    pm_2_5=9.2,
    pm_10=18.5,
    valid_until=UnixTimestamp(0.0),
)

WEATHER_DATA = WeatherData(
    current=CURRENT_WEATHER,
    daily=[DAILY_FORECAST],
    unit_system=UnitSystem.METRIC,
    valid_until=UnixTimestamp(0.0),
)
