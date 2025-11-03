"""Command-line interface for Aruba SSID Manager."""

from __future__ import annotations

import argparse
import logging
import sys
from typing import Any, Dict, Sequence

from .configurator import configure_ssid, interactive_input, setup_logging


def parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """
    Parse command-line arguments.

    Args:
        argv: Optional sequence of argument strings; defaults to ``sys.argv[1:]``.

    Returns:
        Namespace with parsed CLI options.
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
    return parser.parse_args(argv)


def _build_params(args: argparse.Namespace) -> Dict[str, Any]:
    """Return parameter mapping from parsed arguments."""
    return {
        "host": args.host,
        "username": args.username,
        "password": args.password,
        "ssid": args.ssid,
        "vlan": args.vlan,
        "wlan_profile": args.wlan_profile,
        "hidden": args.hidden,
    }


def main(argv: Sequence[str] | None = None) -> int:
    """
    CLI entry point.

    Args:
        argv: Optional custom argv sequence.

    Returns:
        Process exit code (0 on success).
    """
    args = parse_arguments(argv)
    setup_logging(args.verbose, args.logfile)

    if args.interactive or not all([args.host, args.username, args.password, args.ssid, args.vlan, args.wlan_profile]):
        params = interactive_input()
    else:
        params = _build_params(args)

    try:
        configure_ssid(params)
    except KeyboardInterrupt:
        logging.info("Operation cancelled by user.")
        return 0
    except Exception as exc:  # noqa: BLE001 broad to surface CLI errors
        logging.critical("Fatal error configuring SSID: %s", exc)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
