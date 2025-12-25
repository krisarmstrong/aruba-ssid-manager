"""
Aruba SSID Configuration Tool

This script adds a visible or hidden SSID to an Aruba controller via SSH.
Supports both CLI argument and interactive input modes.
Compatible with bump_version.py (version-managed).

Platform: Linux, macOS, Windows
Python: 3.6+

Usage:
  CLI Mode:
    python aruba_ssid_tool.py --host 10.0.0.1 --username admin --password pass \
      --ssid MySSID --vlan 10 --wlan-profile MyProfile --hidden

  Interactive Mode:
    python aruba_ssid_tool.py

Author: Your Name
Version: 0.1.0
"""

__version__ = "0.1.0"

import argparse
import getpass
import logging
import platform
import sys
import pexpect

def setup_logging(verbose: bool):
    """
    Configures logging to console with DEBUG or INFO level based on verbosity.

    Args:
        verbose (bool): If True, sets log level to DEBUG. Otherwise, INFO.
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

def parse_arguments():
    """
    Parses command-line arguments for both CLI and interactive mode.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Add SSID to Aruba controller")
    parser.add_argument("--host", help="Controller IP address")
    parser.add_argument("--username", help="Login username")
    parser.add_argument("--password", help="Login password")
    parser.add_argument("--ssid", help="SSID name to configure")
    parser.add_argument("--vlan", help="VLAN ID to assign", type=int)
    parser.add_argument("--wlan-profile", help="WLAN profile name")
    parser.add_argument("--hidden", help="Set SSID as hidden", action='store_true')
    parser.add_argument("--interactive", help="Use interactive mode", action='store_true')
    parser.add_argument("--verbose", help="Enable debug logging", action='store_true')
    return parser.parse_args()

def interactive_input():
    """
    Prompts user for inputs interactively.

    Returns:
        dict: Dictionary containing user-provided values.
    """
    print("Interactive Mode:")
    return {
        'host': input("Controller IP: "),
        'username': input("Username: "),
        'password': getpass.getpass("Password: "),
        'ssid': input("SSID Name: "),
        'vlan': int(input("VLAN ID: ")),
        'wlan_profile': input("WLAN Profile: "),
        'hidden': input("Hidden SSID (y/n)? ").lower().startswith('y')
    }

def configure_ssid(params):
    """
    Connects to the Aruba controller via SSH and configures an SSID.

    Args:
        params (dict): Contains host, username, password, ssid, vlan,
                       wlan_profile, and hidden as keys.

    Raises:
        pexpect.exceptions.ExceptionPexpect: If any step in automation fails.
    """
    logging.info("Connecting to Aruba controller at %s", params['host'])
    session = pexpect.spawn(f"ssh {params['username']}@{params['host']}", encoding='utf-8', timeout=10)

    session.expect("Password:")
    session.sendline(params['password'])
    session.expect('#')

    # Enter configuration mode
    session.sendline("configure terminal")
    session.expect('#')

    # Begin SSID profile configuration
    session.sendline(f"wlan ssid-profile {params['ssid']}")
    session.expect('#')
    session.sendline(f"ssid-name {params['ssid']}")
    if params['hidden']:
        session.sendline("hide-ssid")
    session.expect('#')
    session.sendline(f"vlan {params['vlan']}")
    session.expect('#')
    session.sendline(f"wlan-profile {params['wlan_profile']}")
    session.expect('#')

    # Exit and save configuration
    session.sendline("exit")
    session.expect('#')
    session.sendline("exit")
    session.expect('#')
    session.sendline("write memory")
    session.expect('#')

    logging.info("SSID '%s' configured successfully.", params['ssid'])

def main():
    """
    Main entry point. Determines mode, gathers inputs, and calls configuration logic.
    """
    args = parse_arguments()
    setup_logging(args.verbose)

    # Fallback to interactive if required args are missing
    if args.interactive or not all([args.host, args.username, args.password, args.ssid, args.vlan, args.wlan_profile]):
        params = interactive_input()
    else:
        params = {
            'host': args.host,
            'username': args.username,
            'password': args.password,
            'ssid': args.ssid,
            'vlan': args.vlan,
            'wlan_profile': args.wlan_profile,
            'hidden': args.hidden
        }

    try:
        configure_ssid(params)
    except Exception as e:
        logging.error("Failed to configure SSID: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()