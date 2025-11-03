"""Public package interface for Aruba SSID Manager."""

from .configurator import configure_ssid, interactive_input, setup_logging, __version__
from .cli import main, parse_arguments

__all__ = [
    "configure_ssid",
    "interactive_input",
    "setup_logging",
    "parse_arguments",
    "main",
    "__version__",
]
