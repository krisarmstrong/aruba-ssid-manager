"""Smoke tests for the Aruba SSID Manager package."""


def test_version():
    import aruba_ssid_manager as mod

    assert hasattr(mod, "__version__")
    assert mod.__version__ == "1.2.2"
