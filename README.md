# Aruba SSID Configurator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![PyPI](https://img.shields.io/pypi/v/aruba-ssid-configurator)]() [![Python](https://img.shields.io/pypi/pyversions/aruba-ssid-configurator)]()

**Configure visible or hidden SSIDs on an Aruba controller via SSH.**

## Requirements
- Python 3.9+
- `pexpect>=4.8`

## Installation
```bash
pip install -e .
```

## Usage
### CLI Mode
```bash
aruba-ssid-configurator --host 10.0.0.1 --username admin --password pass \
  --ssid MySSID --vlan 10 --wlan-profile MyProfile --hidden
```

### Interactive Mode
```bash
python -m aruba_ssid_configurator --interactive
```

## Repository Layout
```
docs/                      Reference documentation
scripts/                   Automation helpers (smoke tests)
src/aruba_ssid_configurator/   Library and CLI implementation
tests/                     Pytest suite (uses src/ layout)
CHANGELOG.md               Release history
pyproject.toml             Packaging metadata
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
