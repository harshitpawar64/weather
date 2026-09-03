# Changelog

## [1.2.0](https://github.com/harshitpawar64/weather/compare/v1.1.1...v1.2.0) (2026-09-03)


### Features

* add show, set, and reset subcommands for config management in CLI ([d1e8a51](https://github.com/harshitpawar64/weather/commit/d1e8a517f31825f88bc461063dee514c3640b952))
* add stats subcommand for cache inspection in CLI ([50c01e1](https://github.com/harshitpawar64/weather/commit/50c01e11aa3bea73446889b650c9fceeea681e61))


### Refactor

* add UnitSystem display properties and simplify onboarding ([0ac436f](https://github.com/harshitpawar64/weather/commit/0ac436fa87a4ead767b56e85b7ce81b76134d70e))
* omit defaults in ConfigData and rename Config.clear to reset ([a97d0ee](https://github.com/harshitpawar64/weather/commit/a97d0ee25c9d4822db87357af4f0092547aba2b9))


### Documentation

* add Codecov badge to README ([9004d36](https://github.com/harshitpawar64/weather/commit/9004d3631825c74a043b049b5e6eea91f70de01e))

## [1.1.1](https://github.com/harshitpawar64/weather/compare/v1.1.0...v1.1.1) (2026-08-29)


### Bug Fixes

* handle invalid date strings in format_sun and format_day ([92b6cd5](https://github.com/harshitpawar64/weather/commit/92b6cd558b24fb43e00c20163ae846d1e731bc38))
* handle malformed coordinates from IPInfo ([8ec6d51](https://github.com/harshitpawar64/weather/commit/8ec6d514013c30365435f5191820410f157db52e))
* truncate pollutant concentrations in US AQI calculation to prevent breakpoint gaps ([56bf7b1](https://github.com/harshitpawar64/weather/commit/56bf7b14550c2206585b2415d7505f915a1c42cf))


### Refactor

* rename utc_dt to local_dt in OpenMeteo weather provider ([1a168ca](https://github.com/harshitpawar64/weather/commit/1a168caf3afec5ac14fbc1d171e557fa344f25c3))

## [1.1.0](https://github.com/harshitpawar64/weather/compare/v1.0.1...v1.1.0) (2026-08-25)


### Features

* support -V short flag for version in CLI ([457371e](https://github.com/harshitpawar64/weather/commit/457371ec09afb26c0e79ee23339ac688126e4f41))
* support optional UV index in AQI providers and default theme ([92af43c](https://github.com/harshitpawar64/weather/commit/92af43c43be668a88af728144798e7d5f436e3ff))


### Documentation

* update location option description and remove duplicate setup command help message ([421e6c0](https://github.com/harshitpawar64/weather/commit/421e6c0681f6db85f1871627a779d16172fb4d61))

## [1.0.1](https://github.com/harshitpawar64/weather/compare/v1.0.0...v1.0.1) (2026-08-23)


### Bug Fixes

* handle empty AQI data from OpenWeather ([44c61cc](https://github.com/harshitpawar64/weather/commit/44c61ccea740b971758744cdb434cabba773b16a))
* handle OSError on cache clear ([1e32639](https://github.com/harshitpawar64/weather/commit/1e32639b61f642b4089227b55e626fae823fb3fb))


### Refactor

* modularize cli and test suite, defer unit/theme fallback to app ([e894dc7](https://github.com/harshitpawar64/weather/commit/e894dc721b28d10da79e033a7c6029734b56b909))


### Documentation

* update demo assets in README to use absolute URLs ([c401312](https://github.com/harshitpawar64/weather/commit/c40131294c5552859794b592cf924bc0cde5ee21))

## [1.0.0](https://github.com/harshitpawar64/weather/compare/v0.1.0...v1.0.0) (2026-08-21)


### Features

* add config and cache management commands in CLI ([bdc2358](https://github.com/harshitpawar64/weather/commit/bdc2358bb774fe689e39dbb5d85bac8c6f858d03))
* add core data models ([de98f55](https://github.com/harshitpawar64/weather/commit/de98f55c1d494dcee2f42f49373c33039599ac6c))
* add days option in CLI for adjustable forecast range ([d056f67](https://github.com/harshitpawar64/weather/commit/d056f67a103a99f67ee26dcffa93d783bccf5a08))
* add night condition icons and modularize ASCII icons ([c7e0a3f](https://github.com/harshitpawar64/weather/commit/c7e0a3fbf03aa39a5534c01b447a3412402d19ff))
* add provider interfaces ([c5aa90b](https://github.com/harshitpawar64/weather/commit/c5aa90be292223ab18e2a4009f76fc50e057df52))
* add theme option in CLI and fallback to config theme ([5614475](https://github.com/harshitpawar64/weather/commit/5614475b3ea60ad7107f23e21687767f4e82208c))
* add WMO weather conditions mapping with ASCII icons ([fd2495e](https://github.com/harshitpawar64/weather/commit/fd2495e403dca93e11a03b19808c06964e338239))
* handle null forecast values and polar extremes ([ffe8fca](https://github.com/harshitpawar64/weather/commit/ffe8fca7cfcf26a46ea29ea081b17358ff4ebe01))
* implement application orchestrator and main CLI entrypoint ([0c92263](https://github.com/harshitpawar64/weather/commit/0c92263da75839afeebd73671bb234b3e5918461))
* implement AQIService with provider fallback pipeline ([96e09d3](https://github.com/harshitpawar64/weather/commit/96e09d35673474852f28d23334ab25e2e0bfb20e))
* implement cache pruning and atomic file writes ([c93f6a1](https://github.com/harshitpawar64/weather/commit/c93f6a1ab81be6c06f0d72463f83d33fd1fcd770))
* implement CountryIs geolocation provider ([941aa53](https://github.com/harshitpawar64/weather/commit/941aa53ef5a148e2ef870edeac3a52f78af3a08f))
* implement custom exceptions and skip unconfigured providers ([baf2f40](https://github.com/harshitpawar64/weather/commit/baf2f403a452a8e260e77e7113997c9649bf10ad))
* implement fallback to stale cache for weather and AQI ([4258836](https://github.com/harshitpawar64/weather/commit/425883653526ee071aec8fd1c1bea7efd05d5e86))
* implement FreeIPAPI geolocation provider ([ce5603d](https://github.com/harshitpawar64/weather/commit/ce5603dc3c9e9e4b0a9af8c6723c1fe82f287407))
* implement GeocodingService with provider fallback pipeline ([13ff239](https://github.com/harshitpawar64/weather/commit/13ff23916d0fdfcf9c51e59bb0f2d95b73a47f6e))
* implement GeolocationService with provider fallback pipeline ([a552166](https://github.com/harshitpawar64/weather/commit/a5521664f468bb7605a927534dbc9ccc4c54a741))
* implement interactive onboarding for first-run setup ([e00a1e5](https://github.com/harshitpawar64/weather/commit/e00a1e5428d5f7d95172b25f53faac7934a331de))
* implement IPInfo geolocation provider ([bf72147](https://github.com/harshitpawar64/weather/commit/bf7214711134726be9a4746e05bab7b10302ba2e))
* implement IPWhoIs geolocation provider ([89c5132](https://github.com/harshitpawar64/weather/commit/89c51326f88d7f1156aa1ebd25bc769b3e7293fa))
* implement JSON output flag in CLI ([74bc4a1](https://github.com/harshitpawar64/weather/commit/74bc4a1b99e678989db1f6ccbefadc5ab558da5e))
* implement metric and imperial unit flags in CLI ([3adc52f](https://github.com/harshitpawar64/weather/commit/3adc52f6d0d9e6a4174832bd736e04f93044b47a))
* implement modular UI rendering and theme config ([fb6bf42](https://github.com/harshitpawar64/weather/commit/fb6bf42323b97aa7bd4c1f358743e2644d2c0813))
* implement Nominatim geocoding provider ([6fbab91](https://github.com/harshitpawar64/weather/commit/6fbab91f21ea32d742e014b724602d96c43a7ab0))
* implement OpenMeteo AQI provider ([59b055e](https://github.com/harshitpawar64/weather/commit/59b055e57338b85ca70e7a01ff57f576e50f8f81))
* implement OpenMeteo geocoding provider ([0f1de02](https://github.com/harshitpawar64/weather/commit/0f1de024f8c33506bd10ca73401726ecda649324))
* implement OpenMeteo weather provider ([69f40e1](https://github.com/harshitpawar64/weather/commit/69f40e1b098895a23f04f34c1b1341d45a2e78c1))
* implement OpenWeather AQI provider ([308f562](https://github.com/harshitpawar64/weather/commit/308f562e64ad104049c477c6462441ae4feedcf9))
* implement persistent caching for geocoding, weather and AQI ([db98ee2](https://github.com/harshitpawar64/weather/commit/db98ee20b01d441bbb13ebb0064762168d4da960))
* implement persistent TOML configuration ([ecefe06](https://github.com/harshitpawar64/weather/commit/ecefe062e9237c69945d89117c72d45ac51225d7))
* implement setup CLI command and lazy-load weather.app ([315b278](https://github.com/harshitpawar64/weather/commit/315b2784b6861810e88c8643e9aa9681a8b3d054))
* implement verbose logging using Rich and graceful interrupt handling ([d67dfc8](https://github.com/harshitpawar64/weather/commit/d67dfc836e139e04dda49c77e9621805092f729b))
* implement WeatherService with provider fallback pipeline ([38e6ce3](https://github.com/harshitpawar64/weather/commit/38e6ce30f2f4e84ddae43f9b15e43456eab912d9))
* improve onboarding ([fafa233](https://github.com/harshitpawar64/weather/commit/fafa233d21ced03b21d1df8cc58235889a706deb))
* redesign default theme and implement thermal color mapping ([42cc41c](https://github.com/harshitpawar64/weather/commit/42cc41c108a76400e51893704970b394650a4a19))
* support optional AQI across models, cache and UI ([4cbac02](https://github.com/harshitpawar64/weather/commit/4cbac02e3e560992711d5048933d25635cd05b48))


### Bug Fixes

* adjust forecast panel padding and remove extra newlines in fog icons ([215156f](https://github.com/harshitpawar64/weather/commit/215156f51b160822768ef7412640b9cfd8af8a16))
* handle empty and duplicate fields in geolocation display names ([93d7044](https://github.com/harshitpawar64/weather/commit/93d7044ddc70ca551edcb34f216f33273fbd07fb))
* improve logging and error handling in CLI ([81b3ca6](https://github.com/harshitpawar64/weather/commit/81b3ca6fa8a45628dd6573f15fc6497031c4ea1b))
* persist geocoding query in cache ([e74b0b0](https://github.com/harshitpawar64/weather/commit/e74b0b0ff8b3ee9a6d0c06338112ac9292127c6d))
* persist pruned cache and encapsulate file writes in Cache and Config ([d052004](https://github.com/harshitpawar64/weather/commit/d052004ac794100c14f3c56802f9c57162ef51bd))
* remove inaccurate postal code from IPInfo geolocation ([0dab93e](https://github.com/harshitpawar64/weather/commit/0dab93ef8e179cd431997c4de2548f7e89441382))
* trim trailing whitespace to fix icon centering in columns ([8c85fd5](https://github.com/harshitpawar64/weather/commit/8c85fd5bf2e0a3c8792cc7077f98549d46b1a048))


### Refactor

* abstract API URL and key handling to base provider ([3562afe](https://github.com/harshitpawar64/weather/commit/3562afe38c670252ef42c0ba63977fce0f78b257))
* annotate method overrides with override decorator ([b83b1be](https://github.com/harshitpawar64/weather/commit/b83b1be003a293b7d11691b1ad0359547cf918a4))
* disable timestamps in logging configuration ([748f9ff](https://github.com/harshitpawar64/weather/commit/748f9fffa4c752eb3b37e0816b6bfafa136ea759))
* enforce uniform 5-line heights across all weather icons ([e4b895b](https://github.com/harshitpawar64/weather/commit/e4b895b403030954077f427b82287e50577d38b4))
* improve Cache and Config ([09f5e77](https://github.com/harshitpawar64/weather/commit/09f5e77a22e20df9d459f3d65bc9d3520d1655f7))
* improve type hints and coordinate validation errors ([b45eafd](https://github.com/harshitpawar64/weather/commit/b45eafdbf8582e6af56e3c3c7d38c0fd4cb6b793))
* support Python &gt;=3.12 ([1b67d87](https://github.com/harshitpawar64/weather/commit/1b67d87384aa5aaf16910d49535e56a1ff518b2a))
* use deferred string formatting in logger calls ([9736f6e](https://github.com/harshitpawar64/weather/commit/9736f6ee4b149a23a4c6a32146eb95fba914de19))
* use timezone-aware timestamps and extract datetime utils ([4a9a0dd](https://github.com/harshitpawar64/weather/commit/4a9a0dd7d8fac95a803ec0b736d7110b05ebec19))
* use UnitSystem enum instead of primitive unit strings ([4eb23a0](https://github.com/harshitpawar64/weather/commit/4eb23a0d822a15eaa23ce73cb91b9bb9de9e6f27))


### Documentation

* add Contributor Covenant 3.0 Code of Conduct ([55a4e00](https://github.com/harshitpawar64/weather/commit/55a4e00084d1e6a627482bddb1c6987169f36ccc))
* update installation instructions for PyPI package ([257559e](https://github.com/harshitpawar64/weather/commit/257559e89a873f6a025ad31fd5e8d99093bbbd23))
* update README.md, add demo assets and VHS scripts ([ab194f1](https://github.com/harshitpawar64/weather/commit/ab194f14d729cc44c0c8f0d5ab9f4bf84e054ca5))
