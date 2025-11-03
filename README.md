# Aruba SSID Manager

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![PyPI](https://img.shields.io/pypi/v/aruba-ssid-manager)]() [![Python](https://img.shields.io/pypi/pyversions/aruba-ssid-manager)]()

**Configure visible or hidden SSIDs on an Aruba controller via SSH.**

## Requirements
- Python 3.9+
- `pexpect>=4.8`

## Installation
```bash
pip install -e .
```

## Quick Start
Run the packaged CLI to configure an SSID in one shot:
```bash
aruba-ssid-manager --host 10.0.0.1 --username admin --password pass \
  --ssid MySSID --vlan 10 --wlan-profile MyProfile --hidden
```

Prefer guided prompts? Launch the package module directly:
```bash
python -m aruba_ssid_manager --interactive
```

The CLI exits with `0` on success and `1` on failure, making it easy to integrate into automation pipelines or CI jobs.

## Repository Layout
```
docs/                      Reference documentation
scripts/                   Automation helpers (smoke tests)
src/aruba_ssid_manager/    Library and CLI implementation
tests/                     Pytest suite (uses src/ layout)
CHANGELOG.md               Release history
pyproject.toml             Packaging metadata
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
