#!/usr/bin/env python3
"""
Project Title: Aruba SSID Configurator

A command-line utility to configure visible or hidden SSIDs on an Aruba controller via SSH.
Supports both interactive prompts and full CLI argument mode. Uses structured logging for clarity.

Author: Kris Armstrong
"""

from __future__ import annotations
import argparse
import getpass
import logging
import sys
import pexpect
from typing import Any, Dict

__version__ = "1.0.0"

def setup_logging(verbose: bool, logfile: str | None = None) -> None:
    """
    Configure logging to output to console and optional file.

    Args:
        verbose (bool): If True, set log level to DEBUG; else INFO.
        logfile (str | None): Optional path to file for logging output.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG if verbose else logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if logfile:
        fh = logging.FileHandler(logfile)
        fh.setLevel(logging.DEBUG if verbose else logging.INFO)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(description="Configure SSID on an Aruba controller")
    parser.add_argument("--host", type=str, help="Controller IP address")
    parser.add_argument("--username", type=str, help="SSH login username")
    parser.add_argument("--password", type=str, help="SSH login password")
    parser.add_argument("--ssid", type=str, help="SSID name to configure")
    parser.add_argument("--vlan", type=int, help="VLAN ID to assign")
    parser.add_argument("--wlan-profile", dest="wlan_profile", type=str, help="WLAN profile name")
    parser.add_argument("--hidden", action="store_true", help="Set SSID as hidden")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--logfile", type=str, help="Optional logfile path")
    parser.add_argument("--verbose", action="store_true", help="Enable debug-level logging")
    return parser.parse_args()

def interactive_input() -> Dict[str, Any]:
    """
    Prompt user for parameters in interactive mode.

    Returns:
        Dict[str, Any]: Parameter dictionary.
    """
    host = input("Controller IP: ")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    ssid = input("SSID Name: ")
    vlan = int(input("VLAN ID: "))
    wlan_profile = input("WLAN Profile: ")
    hidden = input("Hidden SSID? (y/n): ").strip().lower().startswith("y")
    return {
        "host": host,
        "username": username,
        "password": password,
        "ssid": ssid,
        "vlan": vlan,
        "wlan_profile": wlan_profile,
        "hidden": hidden,
    }

def configure_ssid(params: Dict[str, Any]) -> None:
    """
    Connect via SSH and configure the specified SSID.

    Args:
        params (Dict[str, Any]): Parameters including host, username, password, ssid, vlan, wlan_profile, hidden.

    Raises:
        pexpect.exceptions.ExceptionPexpect: On SSH or command failure.
    """
    logging.info("Connecting to %s as %s", params["host"], params["username"])
    session = pexpect.spawn(f"ssh {params['username']}@{params['host']}", encoding="utf-8", timeout=30)
    session.expect("Password:")
    session.sendline(params["password"])
    session.expect(r"#")

    commands = [
        "configure terminal",
        f"wlan ssid-profile {params['ssid']}",
        f"ssid-name {params['ssid']}",
    ]
    if params["hidden"]:
        commands.append("hide-ssid")
    commands += [
        f"vlan {params['vlan']}",
        f"wlan-profile {params['wlan_profile']}",
        "exit",
        "exit",
        "write memory",
    ]

    for cmd in commands:
        session.sendline(cmd)
        session.expect(r"#")

    logging.info("Successfully configured SSID '%s'", params["ssid"])

def main() -> None:
    """
    Main entrypoint: parse args, set up logging, and run configuration.
    """
    args = parse_arguments()
    setup_logging(args.verbose, args.logfile)

    if args.interactive or not all([args.host, args.username, args.password, args.ssid, args.vlan, args.wlan_profile]):
        params = interactive_input()
    else:
        params = {
            "host": args.host,
            "username": args.username,
            "password": args.password,
            "ssid": args.ssid,
            "vlan": args.vlan,
            "wlan_profile": args.wlan_profile,
            "hidden": args.hidden,
        }

    try:
        configure_ssid(params)
    except KeyboardInterrupt:
        logging.info("Operation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        logging.critical("Fatal error configuring SSID: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
