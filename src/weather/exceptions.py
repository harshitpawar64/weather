class WeatherError(Exception):
    """Base exception for all weather errors."""


class ProviderError(WeatherError):
    """Base exception for provider-related errors."""


class LocationNotFoundError(ProviderError):
    """Raised when a location query cannot be resolved to geographic coordinates."""


class ServiceError(WeatherError):
    """Base exception for service-related errors."""
