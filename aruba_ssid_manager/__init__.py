"""Public package interface for Aruba SSID Manager."""

from .cli import main, parse_arguments
from .configurator import __version__, configure_ssid, interactive_input, setup_logging

__all__ = [
    "__version__",
    "configure_ssid",
    "interactive_input",
    "main",
    "parse_arguments",
    "setup_logging",
]
