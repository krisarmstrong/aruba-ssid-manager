# API Reference

## Module: aruba_ssid_manager

### Functions

#### `setup_logging(verbose: bool, logfile: str | None = None) -> None`

Configure logging to output to console and optional file.

**Parameters:**
- `verbose` (bool): If `True`, set log level to DEBUG; otherwise INFO
- `logfile` (str | None, optional): Optional path to file for logging output. Defaults to `None`

**Returns:**
- None

**Example:**
```python
from aruba_ssid_manager import setup_logging

setup_logging(verbose=True, logfile="/var/log/aruba_config.log")
```

**Behavior:**
- Creates root logger with specified verbosity
- Adds console handler (stdout) with structured formatting
- If `logfile` provided, adds file handler with same formatting
- Format: `%(asctime)s [%(levelname)s] %(message)s`

---

#### `parse_arguments() -> argparse.Namespace`

Parse command-line arguments for the application.

**Returns:**
- `argparse.Namespace`: Object containing parsed arguments with attributes:
  - `host` (str): Controller IP address
  - `username` (str): SSH login username
  - `password` (str): SSH login password
  - `ssid` (str): SSID name to configure
  - `vlan` (int): VLAN ID to assign
  - `wlan_profile` (str): WLAN profile name
  - `hidden` (bool): Set SSID as hidden (default: False)
  - `interactive` (bool): Run in interactive mode (default: False)
  - `logfile` (str): Optional logfile path
  - `verbose` (bool): Enable debug-level logging (default: False)

**Example:**
```python
from aruba_ssid_manager import parse_arguments

args = parse_arguments()
print(f"Connecting to {args.host} as {args.username}")
```

**Argument Details:**

| Argument | Short | Type | Required | Default | Help |
|----------|-------|------|----------|---------|------|
| `--host` | - | str | No | None | Controller IP address |
| `--username` | - | str | No | None | SSH login username |
| `--password` | - | str | No | None | SSH login password |
| `--ssid` | - | str | No | None | SSID name to configure |
| `--vlan` | - | int | No | None | VLAN ID to assign |
| `--wlan-profile` | - | str | No | None | WLAN profile name |
| `--hidden` | - | bool | No | False | Set SSID as hidden |
| `--interactive` | - | bool | No | False | Run in interactive mode |
| `--logfile` | - | str | No | None | Optional logfile path |
| `--verbose` | - | bool | No | False | Enable debug-level logging |

---

#### `interactive_input() -> Dict[str, Any]`

Prompt user for parameters in interactive mode.

**Returns:**
- `Dict[str, Any]`: Parameter dictionary with keys:
  - `host` (str): Controller IP address
  - `username` (str): SSH username
  - `password` (str): SSH password
  - `ssid` (str): SSID name
  - `vlan` (int): VLAN ID
  - `wlan_profile` (str): WLAN profile name
  - `hidden` (bool): Whether SSID is hidden

**Example:**
```python
from aruba_ssid_manager import interactive_input

params = interactive_input()
# User is prompted for each parameter
```

**Interactive Prompts:**
1. Controller IP: (text input)
2. Username: (text input)
3. Password: (masked input via getpass)
4. SSID Name: (text input)
5. VLAN ID: (integer input)
6. WLAN Profile: (text input)
7. Hidden SSID? (y/n): (yes/no input)

**Note:** Password input is masked and not echoed to terminal for security.

---

#### `configure_ssid(params: Dict[str, Any]) -> None`

Connect via SSH and configure the specified SSID.

**Parameters:**
- `params` (Dict[str, Any]): Parameter dictionary containing:
  - `host` (str): Controller IP address
  - `username` (str): SSH username
  - `password` (str): SSH password
  - `ssid` (str): SSID name
  - `vlan` (int): VLAN ID
  - `wlan_profile` (str): WLAN profile name
  - `hidden` (bool): Whether to hide SSID broadcast

**Returns:**
- None

**Raises:**
- `pexpect.exceptions.ExceptionPexpect`: On SSH connection failure or command execution failure
- Any SSH-related exceptions from underlying SSH process

**Example:**
```python
from aruba_ssid_manager import configure_ssid

params = {
    'host': '192.168.1.1',
    'username': 'admin',
    'password': 'password123',
    'ssid': 'MyNetwork',
    'vlan': 10,
    'wlan_profile': 'default',
    'hidden': False
}

configure_ssid(params)
```

**Command Sequence:**
The function executes the following Aruba CLI commands:
1. `configure terminal` - Enter configuration mode
2. `wlan ssid-profile {ssid}` - Create/select SSID profile
3. `ssid-name {ssid}` - Set SSID name
4. `hide-ssid` - (optional) Hide SSID if `hidden=True`
5. `vlan {vlan}` - Assign VLAN ID
6. `wlan-profile {wlan_profile}` - Assign WLAN profile
7. `exit` - Exit SSID profile config
8. `exit` - Exit configuration mode
9. `write memory` - Save configuration to persistent storage

**Timeout:** 30 seconds per command

---

#### `main() -> None`

Main entrypoint for the application.

**Returns:**
- None

**Exit Codes:**
- 0: Successful execution or user-initiated cancellation
- 1: Fatal error during configuration

**Behavior:**
1. Parses command-line arguments
2. Configures logging based on arguments
3. Determines execution mode (CLI or interactive)
4. Validates parameter availability
5. Executes SSID configuration
6. Handles errors and user interruption gracefully

**Example:**
```python
from aruba_ssid_manager import main

if __name__ == "__main__":
    main()
```

---

## Constants

### `__version__`

Semantic version string for the application.

**Type:** `str`
**Value:** `"1.2.0"`
**Usage:** Reference in version checking and automated version updates

---

## Usage Examples

### Example 1: Full CLI Mode

```bash
aruba-ssid-manager \
  --host 192.168.1.1 \
  --username admin \
  --password MyPassword \
  --ssid GuestNetwork \
  --vlan 20 \
  --wlan-profile guest \
  --hidden \
  --verbose \
  --logfile /var/log/ssid_config.log
```

### Example 2: Interactive Mode

```bash
aruba-ssid-manager --interactive
```

### Example 3: Programmatic Usage

```python
from aruba_ssid_manager import setup_logging, configure_ssid

setup_logging(verbose=True)

params = {
    'host': '10.0.0.1',
    'username': 'admin',
    'password': 'secure_pass',
    'ssid': 'OfficeNetwork',
    'vlan': 100,
    'wlan_profile': 'office',
    'hidden': False
}

try:
    configure_ssid(params)
    print("SSID configured successfully!")
except Exception as e:
    print(f"Configuration failed: {e}")
```

---

## Exceptions

### pexpect.exceptions.ExceptionPexpect

Raised when:
- SSH connection fails
- Password authentication fails
- Commands fail to execute
- SSH session times out (30 seconds)

**Handling:**
```python
import pexpect
from aruba_ssid_manager import configure_ssid

try:
    configure_ssid(params)
except pexpect.exceptions.ExceptionPexpect as e:
    print(f"SSH Error: {e}")
```

---

## Logging Output

Log messages follow this format:
```
2024-11-03 10:30:45,123 [INFO] Connecting to 192.168.1.1 as admin
2024-11-03 10:30:47,456 [INFO] Successfully configured SSID 'GuestNetwork'
```

### Log Levels
- `DEBUG`: Detailed internal operations (verbose mode)
- `INFO`: Standard operational messages
- `CRITICAL`: Fatal errors that prevent execution

---

## Type Annotations

All functions use Python 3.9+ type hints for clarity:

```python
def setup_logging(verbose: bool, logfile: str | None = None) -> None:
    ...

def parse_arguments() -> argparse.Namespace:
    ...

def interactive_input() -> Dict[str, Any]:
    ...

def configure_ssid(params: Dict[str, Any]) -> None:
    ...

def main() -> None:
    ...
```

---

---

Author: Kris Armstrong
