"""Core functionality for Aruba SSID Manager's SSH-based configuration."""

from __future__ import annotations

import getpass
import logging
import sys
from typing import Any, Dict

import pexpect

from ._version import version as __version__

__all__ = ["__version__"]


def setup_logging(verbose: bool, logfile: str | None = None) -> None:
    """
    Configure logging to output to console and optional file.

    Args:
        verbose: When True, use DEBUG level; otherwise INFO.
        logfile: Optional filesystem path for a log file.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if logfile:
        file_handler = logging.FileHandler(logfile)
        file_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


def interactive_input() -> Dict[str, Any]:
    """
    Prompt user for parameters in interactive mode.

    Returns:
        Dictionary with CLI-equivalent parameters.
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
        params: Mapping including host, username, password, ssid, vlan, wlan_profile, hidden.

    Raises:
        pexpect.exceptions.ExceptionPexpect: On SSH or command failure.
    """
    logging.info("Connecting to %s as %s", params["host"], params["username"])
    session = pexpect.spawn(
        f"ssh {params['username']}@{params['host']}",
        encoding="utf-8",
        timeout=30,
    )
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
