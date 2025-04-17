# Aruba SSID Configurator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![PyPI](https://img.shields.io/pypi/v/aruba-ssid-configurator)]() [![Python](https://img.shields.io/pypi/pyversions/aruba-ssid-configurator)]()

**Configure visible or hidden SSIDs on an Aruba controller via SSH.**

## Requirements
- Python 3.9+
- `pexpect>=4.8`

## Installation
```bash
pip install pexpect
```

## Usage
### CLI Mode
```bash
python aruba_ssid_configurator.py --host 10.0.0.1 --username admin --password pass \
  --ssid MySSID --vlan 10 --wlan-profile MyProfile --hidden
```

### Interactive Mode
```bash
python aruba_ssid_configurator.py --interactive
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
