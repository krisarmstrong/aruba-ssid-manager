# Aruba SSID Tool

A cross-platform Python utility to add visible or hidden SSIDs to an Aruba controller using SSH.

## Features

- Supports CLI arguments and interactive prompts
- Adds visible or hidden SSIDs
- Logging support with verbosity control
- Compatible with bump_version.py
- Works on Linux, macOS, Windows (Python 3.6+)

## Usage

### CLI Mode
```bash
python aruba_ssid_tool.py --host 10.0.0.1 --username admin --password pass \
  --ssid MySSID --vlan 10 --wlan-profile MyProfile --hidden
```

### Interactive Mode
```bash
python aruba_ssid_tool.py --interactive
```

## Arguments

| Argument         | Description                         |
|------------------|-------------------------------------|
| `--host`         | Aruba controller IP address         |
| `--username`     | SSH login username                  |
| `--password`     | SSH login password                  |
| `--ssid`         | SSID name to configure              |
| `--vlan`         | VLAN ID to assign                   |
| `--wlan-profile` | WLAN profile name                   |
| `--hidden`       | Flag to set SSID as hidden          |
| `--interactive`  | Prompt for values interactively     |
| `--verbose`      | Enable debug-level logging          |

## Version

Current version: `0.1.0`  
Managed with `bump_version.py`
