# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.4](https://github.com/krisarmstrong/aruba-ssid-manager/compare/v1.2.3...v1.2.4) (2026-06-17)


### Bug Fixes

* **ci:** add missing noxfile and correct matrix python-version ([#9](https://github.com/krisarmstrong/aruba-ssid-manager/issues/9)) ([73b645a](https://github.com/krisarmstrong/aruba-ssid-manager/commit/73b645a9a38031db6daa8a318a2cbf5b3765fe3a))
* **ci:** pin release-please action commit ([#18](https://github.com/krisarmstrong/aruba-ssid-manager/issues/18)) ([8b7277b](https://github.com/krisarmstrong/aruba-ssid-manager/commit/8b7277b1bc7a72b18d08e956275e1469f7cfc05b))

## [Unreleased]

## [1.2.3] - 2024-12-24

### Changed
- Updated release workflow to use CHANGELOG extraction

## [1.2.2] - 2024-12-20
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
