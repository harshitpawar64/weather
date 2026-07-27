import msgspec

from weather.models import Location

LATITUDE = 42.00
LONGITUDE = 42.00
CITY = "City"
REGION = "Region"
COUNTRY = "Country"
DISPLAY_NAME = f"{CITY}, {REGION}, {COUNTRY}"

LOCATION = Location(latitude=LATITUDE, longitude=LONGITUDE, display_name=DISPLAY_NAME)
ENCODER = msgspec.json.Encoder()
