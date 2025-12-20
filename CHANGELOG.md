# Changelog

## [1.2.2] - 2025-12-20
- Excluded legacy archive files from lint/format passes to keep CI clean.
- Bumped version references across code, tests, and documentation.

## [1.2.0] - 2025-11-03
- Renamed the project to **Aruba SSID Manager** with package import `aruba_ssid_manager` and CLI `aruba-ssid-manager`.
- Restructured the source tree, documentation, and tooling to use the new naming.
- Bumped the semantic version constant to `1.2.0`.

## [1.1.1] - 2025-11-03
- Removed legacy `version_bumper.py` helper in favor of Git-managed version tags.
- Updated documentation and tests to reflect the simplified release process.

## [1.1.0] - 2025-11-03
- Migrated project to a modern `src/` package layout with consistent naming.
- Added `pyproject.toml` packaging metadata and console entry point `aruba-ssid-manager`.
- Introduced reusable CLI module and backward-compatible script shim.
- Refreshed documentation, tests, and tooling for the new structure.

## [1.0.0] - Major Release
- Bumped version to 1.0.0 for first stable release
- Refactored to `aruba_ssid_manager.py`
- Added robust header, type annotations, structured logging, and optional logfile
- Included README.md, CHANGELOG.md, LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md, .gitignore
- Added pytest scaffold and version_bumper.py

## [0.1.0] - Initial Release
- Combined scripts for adding visible/hidden SSIDs.
- CLI and interactive input modes.
- Integrated logging and version control support.
