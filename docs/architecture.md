# Architecture

## Overview

Aruba SSID Configurator is a Python 3 command-line utility designed to programmatically configure visible or hidden SSIDs on Aruba wireless controllers via SSH. The architecture emphasizes clarity, type safety, and structured logging.

## System Design

### Core Components

1. **Argument Parser** (`aruba_ssid_configurator.cli.parse_arguments`)
   - Handles command-line argument parsing using Python's `argparse` module
   - Supports both full CLI argument mode and interactive mode
   - Returns a parsed `argparse.Namespace` object with user inputs

2. **Logging System** (`setup_logging()`)
   - Configured using Python's built-in `logging` module
   - Supports console output and optional file logging
   - Adjustable verbosity levels (INFO or DEBUG)
   - Structured format: `timestamp [LEVEL] message`

3. **Interactive Input Handler** (`interactive_input()`)
   - Prompts user for required parameters when in interactive mode
   - Securely handles password input using `getpass` module
   - Returns a dictionary with all required configuration parameters

4. **SSID Configuration Engine** (`configure_ssid()`)
   - Establishes SSH connection to Aruba controller
   - Uses `pexpect` library for SSH session management
   - Sequences Aruba CLI commands to configure SSID
   - Handles both visible and hidden SSID configurations

5. **Main Orchestrator** (`aruba_ssid_configurator.cli.main`)
   - Entry point for the application and console script
   - Determines execution mode (CLI vs. interactive)
   - Orchestrates workflow from argument parsing to configuration
   - Implements error handling and graceful shutdown

### Data Flow

```
User Input (CLI args or interactive prompts)
    ↓
Argument Parsing & Validation
    ↓
Logging Configuration
    ↓
Parameter Dictionary Creation
    ↓
SSH Session Establishment
    ↓
Aruba CLI Command Sequencing
    ↓
Configuration Completion / Error Handling
```

## Module Dependencies

### External Libraries
- **pexpect** (≥4.8): SSH session management and command automation
- **argparse**: Command-line argument parsing (Python stdlib)
- **logging**: Structured logging (Python stdlib)
- **getpass**: Secure password input (Python stdlib)

### Internal Modules
- **src/aruba_ssid_configurator/configurator.py**: Core SSH configuration logic and logging helpers
- **src/aruba_ssid_configurator/cli.py**: Argument parsing and command-line orchestration
- **src/aruba_ssid_configurator/__main__.py**: Enables `python -m aruba_ssid_configurator`
- **version_bumper.py**: Utility for semantic versioning

## SSH Communication Protocol

The application uses `pexpect` to establish an interactive SSH session with the Aruba controller:

1. Spawn SSH process with target controller
2. Wait for password prompt and authenticate
3. Send configuration commands in sequence:
   - Enter configuration mode (`configure terminal`)
   - Define SSID profile and parameters
   - Apply VLAN and WLAN profile settings
   - Optionally hide SSID broadcast
   - Save configuration (`write memory`)
4. Monitor command responses for successful execution

## Type System

The codebase uses Python 3.9+ type annotations for improved code clarity:

- `Dict[str, Any]`: Parameter dictionaries
- `bool`: Boolean flags
- `int`: Numeric IDs (VLAN)
- `str`: String identifiers and paths
- `argparse.Namespace`: Parsed command arguments

## Error Handling

The application implements layered error handling:

1. **User Interruption** (`KeyboardInterrupt`)
   - Graceful shutdown with status message
   - Exit code: 0

2. **Configuration Errors** (Generic `Exception`)
   - Log critical error with details
   - Exit code: 1

3. **SSH/pexpect Errors**
   - Caught as generic exceptions during `configure_ssid()`
   - Logged with full exception details

## Configuration Parameters

| Parameter | Type | Required | Purpose |
|-----------|------|----------|---------|
| host | str | Yes | Controller IP address |
| username | str | Yes | SSH authentication username |
| password | str | Yes | SSH authentication password |
| ssid | str | Yes | SSID name to configure |
| vlan | int | Yes | VLAN ID to assign |
| wlan_profile | str | Yes | WLAN profile name |
| hidden | bool | No | Whether SSID is hidden (default: False) |

## Execution Modes

### CLI Mode
All parameters provided via command-line arguments. Requires complete parameter set.

### Interactive Mode
Prompts user for each parameter sequentially. Activated with `--interactive` flag or when incomplete CLI arguments provided.

## Version Management

The project uses semantic versioning (MAJOR.MINOR.PATCH) managed by:
- `__version__` constant in main module
- `version_bumper.py` for automated version updates
- Git tags for release tracking

## Security Considerations

- Passwords are handled securely via `getpass` module
- SSH credentials transmitted through standard SSH protocol
- Optional file logging for audit trails
- No credentials stored in version control

---

Author: Kris Armstrong
