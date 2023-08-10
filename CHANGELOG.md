# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Changed
- added concept of tolerance to limits: atol, rtol
- added concept of deadband to limits
- added concept of delay to limits

## [2023.8.1]

### Fixed
- create entire directory tree for limits config, if needed

## [2023.8.0]

### Fixed
- complete refactor of limits behavior, doesn't force metadata into happi anymore

## [2023.7.0]

### Added
- actually check safety limits within SafetyCallback
- support for child devices
- support for fallback position

### Changed
- each run now stored in folder
- happi db now backed up for each run
- recipe now backed up for each run

### Fixed
- safety features now support yaq devices

## [2023.6.1]

### Added
- concept of limits for hardware, if out of bounds go back to safe position

### Fixed
- no python changes, just remove VERISON file in favor of __version__.py

## [2023.6.0]

### Added
- minimum viable can actually run reactions via Bluesky

## [2023.4.0]

### Added
- initial release

[Unreleased]: https://github.com/uw-madison-chem-shops/auto_rxn/compare/v2023.8.1...main
[2023.8.1]: https://github.com/uw-madison-chem-shops/auto_rxn/compare/v2023.8.0...v2023.8.1
[2023.8.0]: https://github.com/uw-madison-chem-shops/auto_rxn/compare/v2023.7.0...v2023.8.0
[2023.7.0]: https://github.com/uw-madison-chem-shops/auto_rxn/compare/v2023.6.1...v2023.7.0
[2023.6.1]: https://github.com/uw-madison-chem-shops/auto_rxn/compare/v2023.6.0...v2023.6.1
[2023.6.0]: https://github.com/uw-madison-chem-shops/auto_rxn/compare/v2023.4.0...v2023.6.0
[2023.4.0]: https://github.com/uw-madison-chem-shops/auto_rxn/tags/v2023.4.0

