"""Smoke tests for the Aruba SSID Manager package."""

from pathlib import Path


def _project_version() -> str:
    try:
        import tomllib  # Python 3.11+
    except ModuleNotFoundError:
        try:
            import tomli as tomllib
        except ModuleNotFoundError:
            return "0.0.0"
    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    data = tomllib.loads(pyproject.read_text())
    return data["project"]["version"]


def test_version():
    import aruba_ssid_manager as mod

    assert hasattr(mod, "__version__")
    assert mod.__version__ == _project_version()
