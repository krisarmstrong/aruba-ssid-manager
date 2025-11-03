"""Allow ``python -m aruba_ssid_manager`` execution."""

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
