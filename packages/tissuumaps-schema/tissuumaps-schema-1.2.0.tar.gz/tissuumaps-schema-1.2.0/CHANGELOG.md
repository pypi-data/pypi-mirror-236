# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.2.0](https://github.com/TissUUmaps/TissUUmaps-schema/compare/v1.1.0...v1.2.0)

New schema versions: 1.2, 0.2

### Added
- New Project.menuButtons field (v0, v1)
- New Filter enum items: SplitChannel, Colormap (v1)
- New Layer.clip field (v1)
- New Project.collectionLayout field (v1)

### Fixed
- Fix default uid value for ExpectedHeader (v0)

### Changed
- Allow extra fields in v0
- Allow dictionary values: ExpectedHeader.cb_gr_dict, ExpectedHeader.pie_dict, ExpectedHeader.shape_gr_dict (v1)
- Allow list values: ExpectedHeader.cb_gr_list, ExpectedHeader.pie_list, ExpectedHeader.shape_gr_list (v1)
- LayerFilter values can be strings, booleans or numbers (v0, v1)

### Removed


## [v1.1.0](https://github.com/TissUUmaps/TissUUmaps-schema/compare/v1.0.2...v1.1.0)

New schema versions: 1.1

### Added
- New field `ExpectedHeader.stroke_width`
- New field: `ExpectedRadios.no_fill`

### Fixed

### Changed

### Removed


## [v1.0.2](https://github.com/TissUUmaps/TissUUmaps-schema/compare/v1.0.1...v1.0.2)

### Added
- Exported tissuumaps_schema.utils.CURRENT_SCHEMA_MODULE as tissuumaps_schema.current
- Exported some additional functionality (e.g. get_major_version) via tissuumaps_schema.utils

### Fixed

### Changed
- Renamed tissuumaps_schema.utils.current_schema_module to tissuumaps_schema.utils.CURRENT_SCHEMA_MODULE

### Removed


## [v1.0.1](https://github.com/TissUUmaps/TissUUmaps-schema/compare/v1.0.0...v1.0.1)

### Added

### Fixed
- Bug in `models` command

### Changed
- Versioning scheme: PATCH indicates Python package bugfixes (removed PATCH from schema versioning)

### Removed


## [v1.0.0](https://github.com/TissUUmaps/TissUUmaps-schema/compare/v0.1.0...v1.0.0)

New schema versions: 1.0, 0.1

### Added
- Schema version 0.1.0 ("expectedCSV" format of an EOL TissUUmaps version)
- Upgrade path from schema version 0.1.0 to schema version 1.0.0

### Fixed
- Class hierarchy
- Bug in `upgrade` command
- Version inference in `validate` command
- Typing and/or default values of:
    - Setting.value (type: int|float -> Any)
    - ExpectedHeader.collectionItem_fixed (type: str -> str|int; default: "" -> 0)
    - ExpectedRadios.collectionItem_fixed (default: False -> True)

### Changed
- Renamed schema version 0.1 to schema version 1.0.0

### Removed


## [v0.1.0](https://github.com/TissUUmaps/TissUUmaps-schema/releases/tag/v0.1.0)

Initial release
